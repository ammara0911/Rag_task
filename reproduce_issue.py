import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def wait_for_server(url, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(url)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    return False

def chat(query, session_id="test_session"):
    url = f"{BASE_URL}/chat"
    headers = {"Content-Type": "application/json"}
    payload = {"query": query, "session_id": session_id}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    print("Waiting for server...")
    if not wait_for_server(BASE_URL):
        print("Server failed to start.")
        sys.exit(1)
        
    print("--- Verifying Fix ---")
    
    # 1. Ask about Codex
    q1 = "Tell me about OpenAI Codex."
    print(f"\nQ1: {q1}")
    res1 = chat(q1)
    print(f"A1: {res1.get('answer', 'Error')}")
    print(f"Sources: {res1.get('sources', [])}")
    
    # 2. Ask follow-up
    q2 = "Describe its theme."
    print(f"\nQ2: {q2}")
    res2 = chat(q2)
    print(f"A2: {res2.get('answer', 'Error')}")
    print(f"Sources: {res2.get('sources', [])}")

if __name__ == "__main__":
    main()
