import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout, RequestException
import yaml
import os
from utils.config import get_config

# Load config
config = get_config()

# Extract Ollama config with defaults
OLLAMA_HOST = config.get("ollama", {}).get("host", "localhost")
OLLAMA_PORT = config.get("ollama", {}).get("port", 11434)
OLLAMA_MODEL = config.get("ollama", {}).get("model", "llama3")

def ask_llm(context: str, question: str) -> str:
    try:
        response = requests.post(
            f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant answering based on the context."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
                ],
                "stream": False  
            },
            timeout=60
        )
        response.raise_for_status()

        return response.json()['message']['content'].strip()

    except ConnectionError:
        raise RuntimeError("Cannot connect to Ollama LLM server. Make sure Ollama is running.")
    except Timeout:
        raise RuntimeError("Request to Ollama LLM timed out.")
    except HTTPError as e:
        raise RuntimeError(f"Ollama LLM HTTP error: {e.response.status_code} - {e.response.text}")
    except RequestException as e:
        raise RuntimeError(f"Unexpected error when querying Ollama LLM: {str(e)}")
