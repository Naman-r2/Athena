import logging
import chromadb
from groq import Groq
from app.config import settings

logger = logging.getLogger(__name__)

# Initialize Chroma client
client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
collection = client.get_or_create_collection(name="athena_blogs")

# Initialize Groq client for embeddings
groq_client = Groq(api_key=settings.GROQ_API_KEY)

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100):
    """
    Split text into chunks with minimal overlap to avoid memory issues.
    Reduced overlap and increased chunk size to minimize number of chunks.
    """
    if not text or not text.strip():
        return []
    
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + chunk_size, text_len)
        
        # Only try to find break point if we're not at the end
        if end < text_len:
            # Try to find a sentence boundary (period followed by space)
            break_point = text.rfind('. ', start, end)
            if break_point > start:
                end = break_point + 2
            else:
                # Fall back to finding a space
                break_point = text.rfind(' ', start, end)
                if break_point > start:
                    end = break_point + 1
        
        chunk = text[start:end].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
        
        # Move start position with minimal overlap
        start = end
    
    return chunks

def add_blog_chunks(blog_id: str, title: str, content: str, batch_size: int = 25):
    """
    Add blog chunks to Chroma with embeddings using batch processing.
    Processes chunks in batches to avoid memory exhaustion.
    Gracefully handles missing embeddings.
    """
    logger.info(f"Chunking and embedding blog: {blog_id}")
    full_text = f"Title: {title}\n\n{content}"
    chunks = chunk_text(full_text)
    
    if not chunks:
        logger.info(f"No chunks created for blog {blog_id}")
        return
    
    logger.info(f"Processing {len(chunks)} chunks for blog {blog_id}")
    
    embeddings = []
    use_placeholder = False
    
    # Process chunks in batches to avoid memory issues
    for batch_start in range(0, len(chunks), batch_size):
        batch_end = min(batch_start + batch_size, len(chunks))
        batch_chunks = chunks[batch_start:batch_end]
        
        try:
            response = groq_client.embeddings.create(
                input=batch_chunks,
                model=settings.GROQ_EMBEDDING_MODEL
            )
            batch_embeddings = [each.embedding for each in response.data]
            embeddings.extend(batch_embeddings)
            logger.debug(f"Embedded batch {batch_start}-{batch_end} for blog {blog_id}")
        except Exception as e:
            logger.warning(f"Failed to get embeddings for batch {batch_start}-{batch_end}: {e}. Using placeholder embeddings.")
            use_placeholder = True
            # Use placeholder embeddings for failed batch
            embeddings.extend([[0.0] * 768 for _ in batch_chunks])
    
    # Build metadata
    ids = [f"{blog_id}-chunk-{i}" for i in range(len(chunks))]
    metadatas = [{"blog_id": str(blog_id), "title": title} for _ in chunks]
    
    # Add to Chroma collection
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )
    
    status = "with placeholder embeddings" if use_placeholder else "with Groq embeddings"
    logger.info(f"Added {len(chunks)} chunks to Chroma for blog {blog_id} {status}")

def query_chunks(question: str, n_results: int = 4):
    """Query chunks by similarity (returns documents only if embeddings work)."""
    try:
        response = groq_client.embeddings.create(
            input=[question],
            model=settings.GROQ_EMBEDDING_MODEL
        )
        question_embedding = [response.data[0].embedding]
        results = collection.query(
            query_embeddings=question_embedding,
            n_results=n_results
        )
        
        if not results or not results["documents"] or not results["documents"][0]:
            return []
            
        return results["documents"][0]
    except Exception as e:
        logger.warning(f"Query failed (embeddings unavailable): {e}. Returning empty results.")
        return []


def query_blog_chunks(question: str, n_results: int = 8):
    """Query all chunks (for search) and return with metadata."""
    try:
        response = groq_client.embeddings.create(
            input=[question],
            model=settings.GROQ_EMBEDDING_MODEL
        )
        question_embedding = [response.data[0].embedding]
        results = collection.query(
            query_embeddings=question_embedding,
            n_results=n_results
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        if not documents or not metadatas:
            return []

        return [
            {
                "blog_id": item.get("blog_id"),
                "chunk": doc
            }
            for item, doc in zip(metadatas, documents)
            if item and item.get("blog_id")
        ]
    except Exception as e:
        logger.warning(f"Search query failed (embeddings unavailable): {e}")
        return []


def query_blog_chunks_by_id(question: str, blog_id: str, n_results: int = 8):
    """Query chunks filtered by specific blog_id."""
    try:
        response = groq_client.embeddings.create(
            input=[question],
            model=settings.GROQ_EMBEDDING_MODEL
        )
        question_embedding = [response.data[0].embedding]
        
        # Query with filter for specific blog_id
        results = collection.query(
            query_embeddings=question_embedding,
            n_results=n_results,
            where={"blog_id": str(blog_id)}
        )

        documents = results.get("documents", [[]])[0]
        if not documents:
            return []
            
        return documents
    except Exception as e:
        logger.warning(f"Blog-specific query failed (embeddings unavailable): {e}")
        return []
