import logging
from elasticsearch import Elasticsearch
from app.config import settings

logger = logging.getLogger(__name__)

# Create Elasticsearch client with better connection settings
es = Elasticsearch(
    settings.ELASTICSEARCH_URL,
    request_timeout=10,
    retry_on_timeout=True,
    max_retries=3
)

INDEX_NAME = "blogs_index"

def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        mapping = {
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "content": {"type": "text"},
                    "tags": {"type": "keyword"}
                }
            }
        }
        es.indices.create(index=INDEX_NAME, body=mapping)
        logger.info(f"Created Elasticsearch index: {INDEX_NAME}")

def index_blog(blog_dict: dict):
    doc = {
        "title": blog_dict["title"],
        "content": blog_dict["content"],
        "tags": blog_dict["tags"]
    }
    es.index(index=INDEX_NAME, id=str(blog_dict["id"]), document=doc)
    logger.info(f"Indexed blog: {blog_dict['id']}")

def search_blogs(query: str):
    if not query:
        return []
        
    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^2", "content", "tags"]
            }
        },
        "_source": ["title", "content", "tags"]
    }
    
    res = es.search(index=INDEX_NAME, body=search_body)
    
    results = []
    for hit in res["hits"]["hits"]:
        source = hit["_source"]
        content = source.get("content", "")
        # Create a preview
        preview = (content[:150] + "...") if len(content) > 150 else content
        results.append({
            "id": hit["_id"],
            "title": source.get("title", ""),
            "preview": preview,
            "tags": source.get("tags", [])
        })
    return results
