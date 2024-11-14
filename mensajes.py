from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Clase para recibir la clave de API de Groq
class APIKeyRequest(BaseModel):
    api_key: str

# Variable global para almacenar la clave de API de Groq
global_groq_api_key = os.getenv("GROQ_API_KEY")

# Ruta para verificar si el servicio está activo
@app.get("/")
def read_root():
    return {"message": "API de FastAPI con Groq está en funcionamiento"}

# Ruta para configurar la clave de API de Groq
@app.post("/set-api-key")
def set_api_key(api_key_request: APIKeyRequest):
    global global_groq_api_key
    global_groq_api_key = api_key_request.api_key
    return {"message": "Clave de API de Groq configurada exitosamente"}

# Ruta para interactuar con Groq
@app.post("/groq")
def interact_with_groq(query: str):
    if not global_groq_api_key:
        raise HTTPException(status_code=500, detail="Clave de API de Groq no configurada.")
    
    try:
        # Configurar la URL y los encabezados de la API de Groq
        headers = {"Authorization": f"Bearer {global_groq_api_key}"}
        groq_api_url = "https://api.groq.com/v1/query"  # Cambia esta URL según la documentación de Groq
        response = requests.post(groq_api_url, json={"query": query}, headers=headers)
        
        if response.status_code != 200:
            detail_message = response.json().get("error", "Error desconocido")
            raise HTTPException(status_code=response.status_code, detail=f"Error al conectar con Groq: {detail_message}")
        
        response_data = response.json()
        return {"response": response_data.get("result", "No hay respuesta disponible")}
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con Groq: {str(e)}")
