#!/usr/bin/env python3
"""Test HTTP requests to running server"""
import logging
import requests
import time

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Give server time to start if needed
time.sleep(1)

BASE_URL = "http://localhost:8000"

logger.info(f"Testing {BASE_URL}/test...")
try:
    r = requests.get(f"{BASE_URL}/test", timeout=5)
    logger.info(f"  Status: {r.status_code}")
    logger.info(f"  Response: {r.json()}")
except Exception as e:
    logger.error(f"  Error: {e}")

logger.info(f"\nTesting {BASE_URL}/blogs...")
try:
    r = requests.get(f"{BASE_URL}/blogs", timeout=5)
    logger.info(f"  Status: {r.status_code}")
    logger.info(f"  Response length: {len(r.text)} chars")
    logger.info(f"  Response: {r.json()}")
except Exception as e:
    logger.error(f"  Error: {e}")

logger.info(f"\nTesting {BASE_URL}/generate-blog...")
try:
    r = requests.post(f"{BASE_URL}/generate-blog", json={"topic": "Test Topic"}, timeout=30)
    logger.info(f"  Status: {r.status_code}")
    logger.info(f"  Response: {str(r.json())[:100]}...")
except Exception as e:
    logger.error(f"  Error: {e}")
