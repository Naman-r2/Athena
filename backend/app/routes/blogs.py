import markdown
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from elasticsearch import Elasticsearch

from app.database import get_db
from app.models.blog import Blog
from app.schemas.blog import GenerateRequest
from app.services.blog_service import create_and_store_blog
from app.config import settings
from vector.chroma_client import collection

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/blogs")
def get_blogs(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    try:
        logger.info(f"Fetching blogs with skip={skip}, limit={limit}")
        blogs = db.query(Blog).order_by(Blog.created_at.desc()).offset(skip).limit(limit).all()
        logger.info(f"Found {len(blogs)} blogs")
        
        results = []
        for b in blogs:
            preview = (b.content[:150] + "...") if len(b.content) > 150 else b.content
            results.append({
                "id": str(b.id),
                "title": b.title,
                "preview": preview,
                "tags": b.tags,
                "image_url": b.image_url,
                "created_at": b.created_at.isoformat() if b.created_at else None
            })
        logger.info(f"Returning {len(results)} formatted blogs")
        return results
    except Exception as e:
        logger.error(f"Error fetching blogs: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/blogs/{id}")
def get_blog(id: UUID, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching blog {id}")
        blog = db.query(Blog).filter(Blog.id == id).first()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
            
        html_content = markdown.markdown(
            blog.content,
            extensions=['fenced_code', 'tables']
        )
        
        return {
            "id": str(blog.id),
            "title": blog.title,
            "content": html_content,
            "tags": blog.tags,
            "topic": blog.topic,
            "image_url": blog.image_url,
            "created_at": blog.created_at.isoformat() if blog.created_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching blog {id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-blog")
def generate_new_blog(request: GenerateRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received generate blog request for topic: {request.topic}")
        new_blog = create_and_store_blog(db, request.topic)
        logger.info(f"Blog generated successfully: {new_blog.id}")
        
        html_content = markdown.markdown(
            new_blog.content,
            extensions=['fenced_code', 'tables']
        )
        
        return {
            "id": str(new_blog.id),
            "title": new_blog.title,
            "content": html_content,
            "tags": new_blog.tags,
            "topic": new_blog.topic,
            "image_url": new_blog.image_url,
            "created_at": new_blog.created_at.isoformat() if new_blog.created_at else None
        }
    except Exception as e:
        logger.error(f"Error generating blog: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Blog generation failed: {str(e)}")

@router.delete("/admin/delete-all")
def delete_all_blogs(db: Session = Depends(get_db)):
    try:
        logger.info("Starting admin delete all operation")
        
        # 1. Delete all blogs from PostgreSQL
        deleted_count = db.query(Blog).delete()
        db.commit()
        logger.info(f"Deleted {deleted_count} blogs from PostgreSQL")
        
        # 2. Delete all documents from Elasticsearch
        try:
            es_client = Elasticsearch([settings.ELASTICSEARCH_HOST])
            es_client.delete_by_query(
                index="blogs",
                body={"query": {"match_all": {}}}
            )
            logger.info("Deleted all documents from Elasticsearch")
        except Exception as e:
            logger.warning(f"Failed to delete from Elasticsearch: {e}")
        
        # 3. Delete all embeddings from Chroma
        try:
            collection.delete(where={})  # Delete all
            logger.info("Deleted all embeddings from Chroma")
        except Exception as e:
            logger.warning(f"Failed to delete from Chroma: {e}")
        
        return {"message": "All blogs deleted"}
        
    except Exception as e:
        logger.error(f"Error in admin delete all: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/blogs/{id}/related")
def get_related_blogs(id: UUID, db: Session = Depends(get_db)):
    try:
        logger.info(f"Getting related blogs for {id}")
        
        # Get the target blog
        target_blog = db.query(Blog).filter(Blog.id == id).first()
        if not target_blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        # Use Chroma similarity search
        from vector.chroma_client import query_chunks
        related_chunks = query_chunks(target_blog.title + " " + " ".join(target_blog.tags), n_results=10)
        
        # Extract unique blog_ids from chunks (excluding the current blog)
        related_blog_ids = set()
        for chunk in related_chunks:
            # Parse blog_id from chunk ID (format: "blog_id-chunk-X")
            if "-chunk-" in chunk:
                blog_id = chunk.split("-chunk-")[0]
                if blog_id != str(id):
                    related_blog_ids.add(blog_id)
        
        # Fetch related blogs
        related_blogs = []
        for blog_id in list(related_blog_ids)[:5]:  # Limit to 5
            try:
                blog = db.query(Blog).filter(Blog.id == blog_id).first()
                if blog:
                    preview = (blog.content[:150] + "...") if len(blog.content) > 150 else blog.content
                    related_blogs.append({
                        "id": str(blog.id),
                        "title": blog.title,
                        "preview": preview,
                        "tags": blog.tags,
                        "created_at": blog.created_at.isoformat() if blog.created_at else None
                    })
            except Exception as e:
                logger.warning(f"Error fetching related blog {blog_id}: {e}")
        
        logger.info(f"Found {len(related_blogs)} related blogs")
        return related_blogs
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting related blogs for {id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
