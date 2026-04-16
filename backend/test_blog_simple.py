import urllib.request
import json
import socket
import sys

# Test if port is open
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(("127.0.0.1", 8000))
sock.close()

if result == 0:
    print("Port 8000 is open")
else:
    print("Port 8000 is closed")

# Try simple GET first
try:
    print("\nTesting GET /test...")
    req = urllib.request.Request("http://localhost:8000/test")
    with urllib.request.urlopen(req, timeout=10) as response:
        print(f"Status: {response.status}")
        print(f"Response: {response.read().decode()}")
except Exception as e:
    print(f"GET Error: {e}", file=sys.stderr)

# Try /generate-blog POST
try:
    print("\nTesting POST /generate-blog...")
    data = json.dumps({"topic": "Artificial Intelligence"}).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:8000/generate-blog",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        print(f"Status: {response.status}")
        body = json.loads(response.read().decode())
        print(f"Response Status Code: {response.status}")
        print(f"Title: {body.get('title', 'N/A')}")
        print(f"Image URL: {body.get('image_url', 'N/A')}")
        print(f"Topic: {body.get('topic', 'N/A')}")
        print(f"Tags: {body.get('tags', 'N/A')}")
except Exception as e:
    print(f"POST Error: {e}", file=sys.stderr)
