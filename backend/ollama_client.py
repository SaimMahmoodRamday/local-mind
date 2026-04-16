import json
from typing import Generator

import requests

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "mistral"  # change if your tag is different, e.g. "mistral:latest"


def generate_stream(prompt: str, temperature: float = 0.7) -> Generator[str, None, None]:
    """Stream tokens from Ollama's /api/generate endpoint."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": temperature,
        },
    }
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        stream=True,
        timeout=600,
    )
    response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue
        data = json.loads(line.decode("utf-8"))
        chunk = data.get("response")
        if chunk:
            yield chunk
        if data.get("done"):
            break
