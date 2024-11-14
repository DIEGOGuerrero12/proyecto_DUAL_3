# proyecto_DUAL_3

#  Endpoint que reciba un promt, genere una respuesta y la envie al usuario
Endpoint para preguntar (usuario) y responder(ia)
`bash
@app.get("/v1/{chat}")
def mostrar_chat(chat:str):
`
Llama a la función 'respuesta_ia' pasando el mensaje del usuario que se envió como parámetro 'chat'
`bash
    respuesta = respuesta_ia(chat)
`
Devuelve la respuesta generada en formato JSON, dentro de un diccionario con la clave "Respuesta"
`bash
    return {"Respuesta": respuesta}

from [no del archivo de la ia] import respuesta_ia
`

#  Endpoint que reciba una imagen de (128px 128px), genere una descripcion de la imagen y la envie al usuario.

## Importaciones y Configuración Inicial
Carga las variables de entorno desde un archivo .env para su uso en la aplicación. Aquí se usa para cargar API_URL y API_KEY de un archivo .env.
`bash
from dotenv import load_dotenv
load_dotenv()
`

FastAPI: Framework usado para crear la API.
File y UploadFile: Permiten manejar archivos subidos en las solicitudes.
Dict: Define el tipo de retorno en el endpoint.
Image: Librería de PIL para manipular y transformar imágenes.
os: Gestiona rutas de archivos y variables de entorno.
requests: Hace solicitudes HTTP a la API externa de análisis de imágenes.
`bash
from fastapi import FastAPI, File, UploadFile
from typing import Dict
from PIL import Image
import os
import requests
`

## Creación de la Aplicación y Configuración de la Carpeta
Inicializa una instancia de FastAPI.
`bash
app = FastAPI()
`

Asegura que exista una carpeta imagenes para guardar las imágenes cargadas.
`bash
os.makedirs("imagenes", exist_ok=True)
`

## Función para Aplicar el Filtro en Escala de Grises
apply_filter: Toma la ruta de una imagen, la abre, convierte a escala de grises (convert("L")), y la guarda en la carpeta imagenes con un prefijo filtered_. Devuelve la ruta de la imagen filtrada.
`bash
def apply_filter(image_path: str) -> str:
    try:
        with Image.open(image_path) as img:
            img = img.convert("L")  # Convierte a escala de grises
            filtered_image_path = os.path.join("imagenes", "filtered_" + os.path.basename(image_path))
            img.save(filtered_image_path)  # Guarda la imagen filtrada
            return filtered_image_path
    except Exception as e:
        raise Exception(f"Error al aplicar el filtro: {e}")
`
## Analizar y Describir la Imagen
Envía la imagen filtrada a una API externa para obtener una descripción. Obtiene la URL del endpoint de la API desde una variable de entorno. Obtiene la clave API desde el entorno para autenticación. Configura la autorización y el tipo de contenido para la solicitud. Envía la imagen como bytes a la API usando requests.post. Devuelve la descripción de la imagen, o un mensaje de error en caso de problemas.
`bash
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
`

## Endpoint para Cargar y Analizar Imágenes
Guarda la imagen en la carpeta imagenes y maneja errores de almacenamiento.
`bash
@app.post("/analyze-image/")
async def upload_image(file: UploadFile = File(...)) -> Dict[str, str]:
    try:
        image_path = os.path.join("imagenes", file.filename)
        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        return {"error": f"Error al guardar la imagen: {e}"}
`

Llama a apply_filter para convertir la imagen a escala de grises y captura cualquier error en el proceso.
`bash
    try:
        filtered_image_path = apply_filter(image_path)
    except Exception as e:
        return {"error": str(e)}
`
    
Obtener descripción de la imagen
`bash
    description = analyze_and_describe_image(filtered_image_path)
    return {"description": description} documenta cada linea para un readme
`