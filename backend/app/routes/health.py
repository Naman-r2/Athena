from fastapi import APIRouter
from app.database import engine
from vector.chroma_client import client as chroma_client
from elasticsearch import Elasticsearch
from app.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    status = {"status": "ok", "services": {}}
    
    # Check Postgres
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
            status["services"]["postgres"] = "ok"
    except Exception as e:
        status["services"]["postgres"] = f"failed: {str(e)}"
        status["status"] = "degraded"
        
    # Check Chroma
    try:
        chroma_client.heartbeat()
        status["services"]["chroma"] = "ok"
    except Exception as e:
        status["services"]["chroma"] = f"failed: {str(e)}"
        status["status"] = "degraded"
        
    # Check Elasticsearch
    try:
        es_client = Elasticsearch([settings.ELASTICSEARCH_HOST])
        es_client.cluster.health(wait_for_status='yellow', timeout='5s')
        status["services"]["elasticsearch"] = "ok"
    except Exception as e:
        status["services"]["elasticsearch"] = f"failed: {str(e)}"
        status["status"] = "degraded"
        
    return status
