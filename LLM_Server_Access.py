import requests
import json

def send_request():
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "How do I init and update a git submodule?"}
        ],
        "temperature": 0.7,
        "max_tokens": 150,
        "stream": True
    }
    try:
        with requests.post(url, headers=headers, json=data, stream=True) as response:
            response.raise_for_status()  # This will raise an exception for HTTP errors
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data:'):
                        json_str = decoded_line[5:]  # Remove 'data:' prefix
                        process_response(json_str)
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)

def process_response(json_str):
    try:
        data = json.loads(json_str)
        if 'choices' in data and data['choices']:
            for choice in data['choices']:
                if 'delta' in choice and 'content' in choice['delta']:
                    print(choice['delta']['content'])
    except json.JSONDecodeError:
        print("Failed to decode JSON:", json_str)

if __name__ == "__main__":
    send_request()
