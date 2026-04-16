import logging
from fastapi import APIRouter, HTTPException
from app.schemas.blog import ChatRequest, ChatResponse
from app.services.llm import generate_chat_answer
from vector.chroma_client import query_blog_chunks_by_id

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_with_pythia(request: ChatRequest):
    try:
        from app.database import get_db
        from app.models.blog import Blog
        from sqlalchemy.orm import Session
        
        # Get the blog to include as context
        db = next(get_db())
        blog = db.query(Blog).filter(Blog.id == request.blog_id).first()
        db.close()
        
        # 1. Retrieve context chunks from Chroma filtered by blog_id
        logger.info(f"Retrieving context for blog {request.blog_id}: {request.question}")
        chunks = query_blog_chunks_by_id(request.question, request.blog_id)
        
        # Combine semantic search results with blog content
        context_parts = []
        if blog:
            context_parts.append(f"Blog Title: {blog.title}")
            context_parts.append(f"Blog Content:\n{blog.content}")
        
        if chunks:
            context_parts.append(f"Related Context:\n" + "\n\n".join(chunks))
        
        context_text = "\n\n".join(context_parts) if context_parts else ""
        
        # 2. Get answer from Groq
        logger.info("Generating answer from LLM...")
        answer = generate_chat_answer(request.question, context_text)
        
        return {"answer": answer}
        
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
