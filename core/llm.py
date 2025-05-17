import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")
ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def llm(prompt, max_tokens=256, stop=None):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": max_tokens,
    }

    if stop:
        payload["stop"] = stop

    try:
        response = requests.post(ENDPOINT, headers=HEADERS, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return {"choices": [{"message": {"content": "Sorry, I had an error."}}]}
