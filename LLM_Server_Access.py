import requests
import json
import sys

def send_request():
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    while True:  # Keep running until the user decides to quit
        user_input = input("Please enter your question (type 'QUIT' to exit): ")
        if user_input.strip().upper() == "QUIT":  # Check if the user wants to quit
            print("Exiting program.")
            sys.exit(0)

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
                        print(f"Received line: {decoded_line}")  # Debug print for each line received
                        if decoded_line.startswith('data:'):
                            json_str = decoded_line[5:].strip()
                            print(f"Extracted JSON: {json_str}")  # Debug print for the extracted JSON
                            if json_str == "[DONE]":
                                print("Stream ended by server.")
                                break
                            message_part = process_response(json_str)
                            print(f"Processed message part: {message_part}")  # Debug print for processed part
                            if message_part:
                                message_buffer += message_part + " "
                                if message_part.endswith('.'):
                                    print(f"Complete sentence: {message_buffer.strip()}")
                                    message_buffer = ""
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
            content = ' '.join(choice['delta']['content'] for choice in data['choices'] if 'delta' in choice and 'content' in choice['delta'])
            return content
    except json.JSONDecodeError:
        print("Failed to decode JSON:", json_str)
        return None

if __name__ == "__main__":
    send_request()
