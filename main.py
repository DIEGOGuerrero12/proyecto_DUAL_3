#Endpoint para preguntar (usuario) y responder(ia)
@app.get("/v1/{chat}")
def mostrar_chat(chat:str):
    # Llama a la función 'respuesta_ia' pasando el mensaje del usuario que se envió como parámetro 'chat'
    respuesta = respuesta_ia(chat)
    # Devuelve la respuesta generada en formato JSON, dentro de un diccionario con la clave "Respuesta"
    return {"Respuesta": respuesta}

from [no del archivo de la ia] import respuesta_ia