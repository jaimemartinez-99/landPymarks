import os
import re
import json
import requests
from loguru import logger
from fastapi import HTTPException

# Obtener la API key de la variable de entorno
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("La variable de entorno DEEPSEEK_API_KEY no está definida.")

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
# Función para llamar a la API de DeepSeek y obtener recomendaciones
def obtener_recomendaciones_deepseek(ciudad, num_dias):
    logger.info(f"Obteniendo recomendaciones de DeepSeek para {num_dias} días en {ciudad}")
    prompt = f"""
    Voy a pasar {num_dias} días en {ciudad}. Quiero que me recomiendes los mejores sitios que visitar y sus coordenadas. Cuanto mas puntos interesantes de la ciudad me recomiendes, mejor. NO DEBE superar los 15 puntos por día ni DEBE ser menor de 10 por dia.
    La respuesta DEBE ser un JSON válido con el siguiente formato. No incluyas mas texto que el JSON:
    [
        {{"nombre": "Nombre del lugar 1", "coords": [latitud, longitud]}},
        {{"nombre": "Nombre del lugar 2", "coords": [latitud, longitud]}}
    ]
    """

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek-chat",  # Ajusta según el modelo de DeepSeek
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al llamar a la API de DeepSeek")
    logger.info("Respuesta de DeepSeek recibida")
    # Extraer la respuesta
    respuesta_raw = response.json()["choices"][0]["message"]["content"]
    print("Respuesta de DeepSeek:", respuesta_raw)

    # Intentar extraer un JSON válido de la respuesta
    try:
        # Buscar un JSON en la respuesta usando una expresión regular
        json_str = re.search(r"\[.*\]", respuesta_raw, re.DOTALL).group(0)
        lugares = json.loads(json_str)
        return lugares
    except (AttributeError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta de DeepSeek: {e}")