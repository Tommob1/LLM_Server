import requests
import json

def send_request():
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "applications/json"}
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "How do I init and update a git submodule?"}
        ],
        "temperature": 0.7,
        "max_tokens": 150,
        "stream": True
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        process_response(response.json())
    else:
        print("Failed to retieve data:", response.status_code)

def process_response(data):
    if 'messages' in data:
        for message in data['messages']:
            print(message['content'])

if __name__ == "__main__":
    send_request()
