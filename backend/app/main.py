import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
from sqlalchemy import text

from app.database import engine, Base, SessionLocal
from app.routes import blogs, search, chat, health
from app.models.blog import Blog
from app.services.blog_service import create_and_store_blog
from workers.scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SAMPLE_TOPICS = [
    "Introduction to Docker Containers",
    "Building Microservices with FastAPI",
    "PostgreSQL Advanced Features"
]

def wait_for_services():
    """Wait for external services to be ready."""
    logger.info("Waiting for services to be ready...")
    
    # Wait for PostgreSQL
    max_retries = 30
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("PostgreSQL is ready")
                break
        except Exception as e:
            if i == max_retries - 1:
                logger.error(f"PostgreSQL not ready after {max_retries} attempts: {e}")
                raise
            logger.warning(f"PostgreSQL not ready, attempt {i+1}/{max_retries}: {e}")
            time.sleep(2)
    
    # Wait for Chroma (optional, don't fail if not ready)
    try:
        from vector.chroma_client import client as chroma_client
        chroma_client.heartbeat()
        logger.info("ChromaDB is ready")
    except Exception as e:
        logger.warning(f"ChromaDB not ready: {e}")
    
    # Wait for Elasticsearch (optional, don't fail if not ready)
    try:
        from elasticsearch import Elasticsearch
        from app.config import settings
        es_client = Elasticsearch([settings.ELASTICSEARCH_HOST])
        es_client.cluster.health(wait_for_status='yellow', timeout='5s')
        logger.info("Elasticsearch is ready")
    except Exception as e:
        logger.warning(f"Elasticsearch not ready: {e}")

def seed_database():
    """Idempotent function to seed 3 sample blogs if none exist."""
    db = SessionLocal()
    try:
        count = db.query(Blog).count()
        if count == 0:
            logger.info("Database is empty. Seeding with 3 sample blogs...")
            for topic in SAMPLE_TOPICS:
                try:
                    create_and_store_blog(db, topic)
                except Exception as e:
                    logger.error(f"Failed to seed blog for topic '{topic}': {e}", exc_info=True)
            logger.info("Seeding complete.")
        else:
            logger.info(f"Database already contains {count} blogs. Skipping seeding.")
    except Exception as e:
        logger.error(f"Error during database seeding: {e}", exc_info=True)
    finally:
        try:
            db.close()
        except Exception as e:
            logger.warning(f"Error closing database session: {e}. Connection may have been interrupted.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Athena backend...")
    
    # 1. Wait for services
    wait_for_services()
    
    # 2. Create PostgreSQL tables
    Base.metadata.create_all(bind=engine)

    # 3. Seed Database & Chroma
    seed_database()
    
    # 4. Start Scheduler
    start_scheduler()
    
    yield
    
    # Shutdown
    logger.info("Shutting down Athena backend...")

app = FastAPI(title="Athena AI Knowledge Engine", lifespan=lifespan)

# CORS
origins = [
    "http://localhost:5173",  # Vite frontend default port
    "http://127.0.0.1:5173",  # Vite frontend with localhost IP
    "http://localhost:8080",  # Vite frontend custom port
    "http://127.0.0.1:8080",  # Localhost IP variant
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(blogs.router, tags=["Blogs"])
app.include_router(search.router, tags=["Search"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(health.router, tags=["Health"])

@app.get("/test")
def test_endpoint():
    """Simple test endpoint to verify server is responding"""
    logger.info("Test endpoint called")
    return {"status": "ok", "message": "Server is responding"}
