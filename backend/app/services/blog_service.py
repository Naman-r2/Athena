import logging
import requests
from sqlalchemy.orm import Session
from app.models.blog import Blog
from app.schemas.blog import BlogOut
from app.services.llm import generate_blog
from vector.chroma_client import add_blog_chunks

logger = logging.getLogger(__name__)

def generate_image_url(topic: str) -> str:
    """Generate an image URL using multiple fallback strategies."""
    try:
        # Extract first meaningful word from topic for better search results
        words = topic.split()
        search_term = words[0].lower() if words else "technology"
        
        # Strategy 1: Direct Unsplash API with size (most reliable)
        # https://source.unsplash.com/{width}x{height}/?{query}
        urls_to_try = [
            f"https://source.unsplash.com/featured/800x600/?{search_term}",
            f"https://source.unsplash.com/800x600/?{search_term},tech",
            "https://source.unsplash.com/800x600/?technology,code,programming",
        ]
        
        for url in urls_to_try:
            try:
                # Test if URL is accessible with a quick request
                response = requests.head(url, timeout=3, allow_redirects=False)
                if response.status_code in [200, 301, 302]:
                    # Return the URL if it resolves (Unsplash redirects are normal)
                    logger.info(f"Generated image URL: {url}")
                    return url
            except requests.RequestException:
                continue
        
        # Strategy 2: Fallback to picsum (placeholder images service)
        # This will definitely work as it's just a placeholder service
        import random
        seed = random.randint(1, 10000)
        fallback_url = f"https://picsum.photos/800/600?random={seed}"
        logger.info(f"Using picsum fallback URL: {fallback_url}")
        return fallback_url
        
    except Exception as e:
        logger.warning(f"Failed to generate image URL for topic '{topic}': {e}")
        # Ultimate fallback - a generic tech image
        return "https://picsum.photos/800/600?random=default"

def create_and_store_blog(db: Session, topic: str):
    logger.info(f"Starting blog generation pipeline for topic: {topic}")
    
    # 1. Generate Blog via LLM
    logger.info("Generating content...")
    blog_data = generate_blog(topic)
    
    # 2. Generate image URL
    logger.info("Generating image URL...")
    image_url = generate_image_url(topic)
    
    # 3. Store in PostgreSQL
    logger.info("Saving to PostgreSQL...")
    db_blog = Blog(
        title=blog_data["title"],
        content=blog_data["content"],
        tags=blog_data["tags"],
        topic=topic,
        image_url=image_url
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    
    # 4. Embed chunks to ChromaDB for semantic search
    logger.info("Embedding to ChromaDB...")
    try:
        add_blog_chunks(str(db_blog.id), db_blog.title, db_blog.content)
    except Exception as e:
        logger.error(f"Failed to embed in Chroma: {e}", exc_info=True)
        
    logger.info(f"Pipeline complete for blog {db_blog.id}")
    return db_blog
