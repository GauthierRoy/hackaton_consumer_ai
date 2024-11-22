import requests
import json

# Replace these values with your actual IAM API key and Deployment UUID
#IAM_API_KEY = "SCW3PM6J847263SR4RBX"
IAM_API_KEY = "334d920a-dfb3-4aea-ab17-c8a37b58423a"
DEPLOYMENT_UUID = "38ed1927-8685-4925-a3f6-de02fb09bf3b"


URL = f"https://api.scaleway.ai/{DEPLOYMENT_UUID}/v1/chat/completions"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {IAM_API_KEY}" # Replace $SCW_API_KEY with your IAM API key
}

PAYLOAD = {
  "model": "llama-3.1-70b-instruct",
  "messages": [
        { "role": "system", "content": "You are a helpful assistant" },
		{ "role": "user", "content": "there is a llama in my garden, tell me in a few words what i should do" },
    ],
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.7,
    "presence_penalty": 0,
    "stream": True,
}

response = requests.post(URL, headers=HEADERS, data=json.dumps(PAYLOAD), stream=True)

for line in response.iter_lines():
    if line:
        decoded_line = line.decode('utf-8').strip()
        if decoded_line == "data: [DONE]":
            break
        if decoded_line.startswith("data: "):
            try:
                data = json.loads(decoded_line[len("data: "):])
                content = data["choices"][0]["delta"].get("content")
                if content:
                    print(content, end="")
            except json.JSONDecodeError:
                continue