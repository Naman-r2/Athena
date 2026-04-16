from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.blog import SearchResult
from app.database import get_db
from app.models.blog import Blog
from vector.chroma_client import query_blog_chunks

router = APIRouter()

@router.get("/search", response_model=list[SearchResult])
def search(q: str = "", db: Session = Depends(get_db)):
    if not q:
        return []

    chunks = query_blog_chunks(q, n_results=12)
    results = []
    seen_blog_ids = set()

    for item in chunks:
        blog_id = item.get("blog_id")
        if not blog_id or blog_id in seen_blog_ids:
            continue

        blog = db.get(Blog, blog_id)
        if not blog:
            continue

        seen_blog_ids.add(blog_id)
        chunk_text = item.get("chunk", "")
        preview = (chunk_text[:150] + "...") if len(chunk_text) > 150 else chunk_text

        results.append({
            "id": str(blog.id),
            "title": blog.title,
            "preview": preview,
            "tags": blog.tags or []
        })

    return results
