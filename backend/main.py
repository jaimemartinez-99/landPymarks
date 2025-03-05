import os
import uuid
from pymongo import MongoClient
import folium
from typing import List
from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
from optimizer import optimizar_ruta, agrupar_puntos
from deepseek import obtener_recomendaciones_deepseek

# Definir el modelo de datos para los lugares
class Lugar(BaseModel):
    nombre: str
    coords: List[float]

# Crear la aplicación FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (en producción, cambia esto a tu dominio)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

db_user= os.environ.get("DB_USER")
db_password= os.environ.get("DB_PASSWORD")
db = os.environ.get("DB")
db_collection = os.environ.get("DB_COLLECTION")

client = MongoClient(
    f"mongodb+srv://{db_user}:{db_password}@cluster0.2ocgo.mongodb.net/optimapper?retryWrites=true&w=majority&appName=Cluster0"
)
db = client[db]
collection = db[db_collection]

# Endpoint para generar y guardar los mapas
@app.post("/generar-ruta/")
async def generar_ruta(ciudad: str, num_dias: int):
    # Obtener recomendaciones de DeepSeek
    try:
        lugares = obtener_recomendaciones_deepseek(ciudad, num_dias)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Agrupar los puntos en clusters
    grupos = agrupar_puntos(lugares, num_dias)
    mapas_html = []
    uuid_str = str(uuid.uuid4())
    
    # Crear un mapa para cada día y guardarlo en un archivo HTML
    for i, grupo in enumerate(grupos):
        # Optimizar la ruta dentro de cada grupo
        ruta_optimizada = optimizar_ruta(grupo)

        # Crear el mapa
        mapa = folium.Map(location=ruta_optimizada[0]["coords"], zoom_start=14)
        for j, lugar in enumerate(ruta_optimizada):
            # Crear un ícono personalizado con un número
            icono = folium.DivIcon(
                icon_size=(30, 30),
                icon_anchor=(15, 15),
                html=f'<div style="font-size: 12pt; color: white; background-color: blue; border-radius: 50%; width: 30px; height: 30px; text-align: center; line-height: 30px;">{j+1}</div>'
            )
            folium.Marker(
                location=lugar["coords"],
                popup=lugar["nombre"],
                icon=icono,
            ).add_to(mapa)
            logger.info("Mapa guardado correctamente")
            logger.info(f"{j+1}. {lugar['nombre']}")
        # Guardar el mapa en un archivo HTML
        mapas_html.append(mapa._repr_html_())
    mongo_document = {
        "uuid": uuid_str,
        "ciudad": ciudad,
        "num_dias": num_dias,
        "mapas": mapas_html,
        "fecha_creacion": datetime.utcnow(),
    } 
    try:
        result = collection.insert_one(mongo_document)
        logger.info(f"Document inserted with _id: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Error inserting document into MongoDB: {str(e)}")
        raise HTTPException(status_code=500, detail="Error saving to database")
    
    return {"mapas": mapas_html, "link":uuid_str }


@app.get("/recuperar_mapa_existente/{uuid}")
async def get_map(uuid: str):
    document = collection.find_one({"uuid": uuid})
    if document:
        return {
            "mapas": document["mapas"], "ciudad": document["ciudad"], "num_dias": document["num_dias"]
        }
    else:
        raise HTTPException(status_code=404, detail="Map not found")
# Ejecutar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)