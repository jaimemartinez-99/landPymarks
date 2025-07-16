import os
import uuid
from pymongo import MongoClient
from typing import List
from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
from optimizer import group_points
from deepseek import get_deepseek_recomendations
from places import update_coordinates, delete_duplicates
from nx import solve_tsp_and_create_map
from osrm import get_osrm_trip_route, create_map_with_route

class Place(BaseModel):
    nombre: str
    coords: List[float]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
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


@app.post("/generate-route/")
async def generate_route(city: str, num_days: int):
    logger.info("Starting route generation")
    try:
        places = get_deepseek_recomendations(city, num_days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    unique_places = delete_duplicates(places)
    final_places = update_coordinates(unique_places, city)
    groups = group_points(final_places, num_days)
    logger.info("Correctly divided places into groups depending in the number of days")
    
    html_maps = []
    uuid_str = str(uuid.uuid4())
    for i, group in enumerate(groups, 1):
        coords = [place['coords'] for place in group]
        names = [place['nombre'] for place in group]

        try:
            ordered_locations, geometry = get_osrm_trip_route(coords)
            ordered_names = [names[coords.index(loc)] for loc in ordered_locations]

            mapa = create_map_with_route(ordered_locations, geometry, ordered_names)
            mapa_html = mapa._repr_html_()
            html_maps.append(mapa_html)

            filename = f"{uuid_str}_grupo_{i}.html"
            mapa.save(filename)
            logger.info(f"Mapa guardado como {filename}")

        except Exception as e:
            logger.error(f"Error al procesar el grupo {i}: {e}")
            continue

    mongo_document = {
        "uuid": uuid_str,
        "city": city,
        "num_days": num_days,
        "maps": html_maps,
        "creation_date": datetime.utcnow(),
    } 
    try:
        result = collection.insert_one(mongo_document)
        logger.info(f"Document inserted with _id: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Error inserting document into MongoDB: {str(e)}")
        raise HTTPException(status_code=500, detail="Error saving to database")
        
    return {"maps": html_maps, "link":uuid_str }


@app.get("/retrieve_existing_map/{uuid}")
async def get_map(uuid: str):
    document = collection.find_one({"uuid": uuid})
    if document:
        return {
            "maps": document["maps"], "city": document["city"], "num_days": document["num_days"]
        }
    else:
        raise HTTPException(status_code=404, detail="Map not found")
# Ejecutar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)