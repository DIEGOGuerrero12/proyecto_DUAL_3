from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, File, UploadFile
from typing import Dict
from PIL import Image
import os
import requests

app = FastAPI()

# Asegúrate de que la carpeta 'imagenes' existe
os.makedirs("imagenes", exist_ok=True)

def apply_filter(image_path: str) -> str:
    try:
        with Image.open(image_path) as img:
            img = img.convert("L")  # Convierte a escala de grises
            filtered_image_path = os.path.join("imagenes", "filtered_" + os.path.basename(image_path))
            img.save(filtered_image_path)  # Guarda la imagen filtrada
            return filtered_image_path
    except Exception as e:
        raise Exception(f"Error al aplicar el filtro: {e}")

def analyze_and_describe_image(image_path: str) -> str:
    # URL y clave de API (reemplaza por la URL correcta de tu API)
    url = os.getenv("API_URL", "https://your-ai-api.com/analyze-image")  # URL de tu endpoint de análisis de imagen
    api_key = os.getenv("API_KEY", "")  # Asegúrate de definir esta variable en el entorno

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/octet-stream"
    }
    
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Enviar solicitud a la API
        response = requests.post(url, headers=headers, data=image_data, timeout=10)
        response.raise_for_status()  # Lanza una excepción si la respuesta es de error HTTP

        # Extraer descripción de la respuesta
        return response.json().get("description", "Descripción no disponible")
    except requests.Timeout:
        return "Error: La solicitud ha expirado. Intenta reducir el tamaño de la imagen o verifica tu conexión a internet."
    except requests.RequestException as e:
        return f"Error al comunicarse con la API: {e}"
    except ValueError:
        return "Error: La API no devolvió una respuesta JSON válida."

@app.post("/analyze-image/")
async def upload_image(file: UploadFile = File(...)) -> Dict[str, str]:
    try:
        image_path = os.path.join("imagenes", file.filename)
        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        return {"error": f"Error al guardar la imagen: {e}"}

    try:
        filtered_image_path = apply_filter(image_path)
    except Exception as e:
        return {"error": str(e)}
    
    # Obtener descripción de la imagen
    description = analyze_and_describe_image(filtered_image_path)
    return {"description": description}
