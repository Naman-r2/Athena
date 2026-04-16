import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("Waiting for server to be ready...")
time.sleep(2)

# Test 1: Health endpoint
print("=== TEST 1: GET /health ===")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== TEST 2: GET /blogs ===")
try:
    response = requests.get(f"{BASE_URL}/blogs", timeout=5)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Number of blogs: {len(data) if isinstance(data, list) else 'N/A'}")
    if isinstance(data, list) and len(data) > 0:
        print(f"First blog keys: {list(data[0].keys())}")
        print(f"Has image_url: {'image_url' in data[0]}")
        if 'image_url' in data[0]:
            print(f"image_url value: {data[0]['image_url']}")
    print(f"Response sample: {json.dumps(data[0] if isinstance(data, list) and len(data) > 0 else data, indent=2)[:800]}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== TEST 3: POST /generate-blog ===")
try:
    payload = {"topic": "Kubernetes"}
    response = requests.post(f"{BASE_URL}/generate-blog", json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
    print(f"Has image_url: {'image_url' in data if isinstance(data, dict) else 'N/A'}")
    print(f"Response: {json.dumps(data, indent=2)[:800]}")
except Exception as e:
    print(f"Error: {e}")
