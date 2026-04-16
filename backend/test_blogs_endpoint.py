#!/usr/bin/env python3
"""Test script to debug /blogs endpoint"""
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Test 1: Import and run the app directly
logger.info("Test 1: Importing app...")
try:
    from app.main import app
    logger.info("✓ App imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import app: {e}")
    sys.exit(1)

# Test 2: Check if blogs router is registered
logger.info("Test 2: Checking if routes are registered...")
try:
    from fastapi.routing import APIRoute
    routes = [r for r in app.routes if isinstance(r, APIRoute)]
    blogs_routes = [r for r in routes if "/blogs" in r.path]
    logger.info(f"Total routes: {len(routes)}")
    logger.info(f"Blog routes: {len(blogs_routes)}")
    for r in blogs_routes:
        logger.info(f"  - {r.methods} {r.path}")
except Exception as e:
    logger.error(f"✗ Failed to check routes: {e}")

# Test 3: Try to query database directly
logger.info("Test 3: Testing database connection...")
try:
    from app.database import SessionLocal
    from app.models.blog import Blog
    
    db = SessionLocal()
    logger.info("✓ Database session created")
    
    count = db.query(Blog).count()
    logger.info(f"✓ Database query succeeded. Blog count: {count}")
    
    blogs = db.query(Blog).all()
    logger.info(f"✓ Retrieved {len(blogs)} blogs")
    for blog in blogs:
        logger.info(f"  - {blog.id}: {blog.title}")
    
    db.close()
except Exception as e:
    logger.error(f"✗ Database test failed: {e}", exc_info=True)

# Test 4: Make a test HTTP request to the app
logger.info("Test 4: Testing endpoint via TestClient...")
try:
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Test /test endpoint first
    logger.info("Testing /test endpoint...")
    response = client.get("/test")
    logger.info(f"  Status: {response.status_code}")
    logger.info(f"  Response: {response.json()}")
    
    # Test /blogs endpoint
    logger.info("Testing /blogs endpoint...")
    response = client.get("/blogs")
    logger.info(f"  Status: {response.status_code}")
    logger.info(f"  Response: {response.json()[:100]}...")  # Show first 100 chars
    
except Exception as e:
    logger.error(f"✗ HTTP test failed: {e}", exc_info=True)

logger.info("Test complete!")
