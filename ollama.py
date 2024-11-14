from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()

# Clase para el modelo de entrada
class Query(BaseModel):
    query: str

# Ruta para verificar si el servicio está activo
@app.get("/")
def read_root():
    return {"message": "API de FastAPI con Ollama está en funcionamiento"}

# Ruta para interactuar con el modelo Qwen2.5:0.5b descargado
@app.post("/ollama")
def interact_with_ollama(query: Query):
    try:
        # Comando para ejecutar el modelo localmente
        command = ["ollama", "run", "qwen2.5:0.5b", "--query", query.query]
        print(f"Ejecutando comando: {' '.join(command)}")  # Imprimir el comando para depuración
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Resultado del comando: {result.stdout}")  # Imprimir el resultado para depuración
        return {"response": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e.stderr}")  # Imprimir el error para depuración
        raise HTTPException(status_code=500, detail=f"Error al ejecutar el modelo de Ollama: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")  # Imprimir cualquier otro error para depuración
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


