import requests
import json

from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/llama3/{pregunta}")
def preguntas(pregunta: str):
    uri = 'https://api.groq.com/openai/v1/chat/completions'
    API_KEY = "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"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "messages": [
            {
                "role": "system",
                "content": "Eres un asistente de gym, eres mi gymbro"
            },
            {
                "role": "user",
                "content": f"{pregunta}"
            }
        ],
        "model": "llama3-8b-8192",
        "temperature": 0.7,  # 0 más formal - 1 más creativo
        "max_tokens": 200,
        "stream": False,
        "stop": None
    }

    response = requests.post(uri, json=data, headers=headers)
    response = json.loads(response.text)

    return {
        "Pregunta 🤔": pregunta,
        "Respuesta 🤖": response['choices'][0]['message']['content'].replace("\n", " ")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)