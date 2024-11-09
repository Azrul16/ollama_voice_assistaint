import requests
import json
import time

def main():
    url = "http://127.0.0.1:11434/api/generate"
    payload = {
        "model": "llama2",
        "prompt": "What is the full FOrm of RGB, in very short"
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, data=json.dumps(payload), headers=headers, stream=True)
    
    if response.status_code == 200:
        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = json.loads(line.decode('utf-8'))
                full_response += decoded_line.get("response", "")
                print(decoded_line)
                if decoded_line.get("done", False):
                    break
        print("\nFinal Compiled Response:")
        print(full_response.strip())
    else:
        print(f"Failed to connect. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
