from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Asignar la clave de API de Groq desde el entorno
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Ruta para verificar si el servicio está activo
@app.get("/")
def read_root():
    return {"message": "API de FastAPI con Groq está en funcionamiento"}

# Ruta para interactuar con Groq
@app.post("/groq")
def interact_with_groq(query: str):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Clave de API de Groq no configurada.")
    
    try:
        # Configurar la URL y los encabezados de la API de Groq
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        groq_api_url = "https://api.groq.com/v1/query"  # Cambia esta URL según la documentación de Groq
        response = requests.post(groq_api_url, json={"query": query}, headers=headers)
        
        if response.status_code != 200:
            detail_message = response.json().get("error", "Error desconocido")
            raise HTTPException(status_code=response.status_code, detail=f"Error al conectar con Groq: {detail_message}")
        
        response_data = response.json()
        return {"response": response_data.get("result", "No hay respuesta disponible")}
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con Groq: {str(e)}")
