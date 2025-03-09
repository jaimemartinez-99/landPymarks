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
from optimizer import optimize_route, group_points
from deepseek import get_deepseek_recomendations
from places import update_coordinates, delete_duplicates

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
    try:
        places = get_deepseek_recomendations(city, num_days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    unique_places = delete_duplicates(places)
    final_places = update_coordinates(unique_places, city)
    groups = group_points(final_places, num_days)
    html_maps = []
    uuid_str = str(uuid.uuid4())
    
    for i, group in enumerate(groups):
        optimized_route = optimize_route(group)

        map = folium.Map(location=optimized_route[0]["coords"], zoom_start=14)
        for j, place in enumerate(optimized_route):
            
            icon = folium.DivIcon(
                icon_size=(30, 30),
                icon_anchor=(15, 15),
                html=f'<div style="font-size: 12pt; color: white; background-color: blue; border-radius: 50%; width: 30px; height: 30px; text-align: center; line-height: 30px;">{j+1}</div>'
            )
            folium.Marker(
                location=place["coords"],
                popup=place["nombre"],
                icon=icon,
            ).add_to(map)
            logger.info("Map saved correctly")
            logger.info(f"{j+1}. {place['nombre']}")
        map.save(f"mapa_{uuid_str}_{i+1}.html")
        html_maps.append(map._repr_html_())
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