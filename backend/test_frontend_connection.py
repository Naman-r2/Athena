#!/usr/bin/env python3
"""Test frontend connectivity to backend"""
import requests
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

time.sleep(1)

BASE_URL = "http://127.0.0.1:8000"

logger.info(f"Testing {BASE_URL}/blogs...")
try:
    r = requests.get(f"{BASE_URL}/blogs", timeout=5)
    logger.info(f"✓ Status: {r.status_code}")
    data = r.json()
    logger.info(f"✓ Retrieved {len(data)} blogs")
    if data:
        logger.info(f"  First blog: {data[0]['title']}")
except Exception as e:
    logger.error(f"✗ Error: {e}")

logger.info("\nFrontend should now be able to fetch blogs!")
