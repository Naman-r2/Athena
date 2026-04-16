#!/usr/bin/env python3
"""Test database connectivity for local development."""

import sys
import logging
from sqlalchemy import text

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_postgres():
    """Test PostgreSQL connection."""
    try:
        from app.config import settings
        from app.database import engine
        
        logger.info(f"Testing PostgreSQL connection: {settings.DATABASE_URL}")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("✓ PostgreSQL connection successful!")
            return True
    except Exception as e:
        logger.error(f"✗ PostgreSQL connection failed: {e}")
        return False

def test_chroma():
    """Test ChromaDB connection."""
    try:
        from app.config import settings
        import chromadb
        
        logger.info(f"Testing Chroma connection: {settings.CHROMA_HOST}:{settings.CHROMA_PORT}")
        client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
        # Try to get collections
        collections = client.list_collections()
        logger.info(f"✓ Chroma connection successful! Found {len(collections)} collections")
        return True
    except Exception as e:
        logger.error(f"✗ Chroma connection failed: {e}")
        return False

def test_elasticsearch():
    """Test Elasticsearch connection."""
    try:
        from app.config import settings
        from elasticsearch import Elasticsearch
        
        logger.info(f"Testing Elasticsearch connection: {settings.ELASTICSEARCH_URL}")
        es = Elasticsearch([settings.ELASTICSEARCH_URL])
        info = es.info()
        logger.info(f"✓ Elasticsearch connection successful!")
        return True
    except Exception as e:
        logger.error(f"✗ Elasticsearch connection failed: {e}")
        logger.info("   Note: Elasticsearch may not be required if not used in your app")
        return False

def main():
    """Run all connectivity tests."""
    logger.info("=" * 60)
    logger.info("Database Connectivity Test")
    logger.info("=" * 60)
    
    results = {
        "PostgreSQL": test_postgres(),
        "Chroma": test_chroma(),
        "Elasticsearch": test_elasticsearch(),
    }
    
    logger.info("=" * 60)
    logger.info("Test Results Summary:")
    logger.info("=" * 60)
    
    for service, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{service}: {status}")
    
    required_passed = results["PostgreSQL"] and results["Chroma"]
    
    if required_passed:
        logger.info("=" * 60)
        logger.info("✓ All required databases are connected!")
        logger.info("=" * 60)
        return 0
    else:
        logger.info("=" * 60)
        logger.info("✗ Some required databases are not connected.")
        logger.info("Please ensure Docker containers are running with: docker compose up")
        logger.info("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
