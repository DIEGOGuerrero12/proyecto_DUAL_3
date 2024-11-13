from fastapi import FastAPI, HTTPException, File, UploadFile
from typing import Annotated
import os

# Configura la ruta de la carpeta donde se guardarán las imágenes
IMAGE_FOLDER = "imagenes"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    
    # Ruta completa para guardar la imagen
    file_path = os.path.join(IMAGE_FOLDER, file.filename)

    try:
        # Lee el contenido de la imagen subida y guárdalo en la carpeta
        with open(file_path, "wb") as image_file:
            image_file.write(await file.read())
        return {"filename": file.filename, "path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {str(e)}")