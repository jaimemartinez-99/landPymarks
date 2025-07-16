import os
import re
import json
import requests
from loguru import logger
from fastapi import HTTPException

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
if not DEEPSEEK_API_KEY:
    raise ValueError("Deepseek key is not defined.")

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def get_deepseek_recomendations(city, num_days):
    logger.info(f"Obteniendo recomendaciones de DeepSeek para {num_days} días en {city}")
    prompt = f"""
    Voy a pasar {num_days} días en {city}. Quiero que me recomiendes los mejores sitios que visitar y sus coordenadas. Cuanto mas puntos interesantes de la ciudad me recomiendes, mejor. NO DEBE superar los 15 puntos por día ni DEBE ser menor de 10 por dia.
    La respuesta DEBE ser un JSON válido con el siguiente formato. Aunque las instrucciones hayan sido en espanol debes darme la respuesta con el nombre de los sitios en ingles. No incluyas mas texto que el JSON. :
    [
        {{"nombre": "Name of the place 1", "coords": [latitud, longitud]}},
        {{"nombre": "Name of the place 2", "coords": [latitud, longitud]}}
    ]
    """

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek-chat",  
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error with DeepSeek API")
    logger.info("Received response from DeepSeek")

    raw_response = response.json()["choices"][0]["message"]["content"]
    print("Respuesta de DeepSeek:", raw_response)

    try:
        json_str = re.search(r"\[.*\]", raw_response, re.DOTALL).group(0)
        places = json.loads(json_str)
        return places
    except (AttributeError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Error processing Deepseek response: {e}")