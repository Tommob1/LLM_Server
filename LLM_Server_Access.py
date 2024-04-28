import requests
import json

def send_request(user_input):
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 150,
        "stream": True
    }
    message_buffer = ""
    try:
        with requests.post(url, headers=headers, json=data, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith('data:'):
                        json_str = decoded_line[5:].strip()
                        if json_str == "[DONE]":
                            return message_buffer.strip()
                        message_part = process_response(json_str)
                        if message_part:
                            message_buffer += (' ' if message_buffer and not message_buffer.endswith(' ') else '') + message_part
                            if any(message_part.endswith(punc) for punc in '.?!'):
                                return message_buffer.strip()
    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return "Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return "Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Oops: Something Else {err}"

def process_response(json_str):
    try:
        data = json.loads(json_str)
        if 'choices' in data and data['choices']:
            return ''.join(choice['delta']['content'] for choice in data['choices'] if 'delta' in choice and 'content' in choice['delta'])
    except json.JSONDecodeError:
        return "Failed to decode JSON"

def query_server(message):
    return send_request(message)
