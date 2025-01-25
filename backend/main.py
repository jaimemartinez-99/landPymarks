import os
import folium
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

from divider import dividir_en_dias
from optimizer import optimizar_ruta, agrupar_puntos
from deepseek import obtener_recomendaciones_deepseek

# Definir el modelo de datos para los lugares
class Lugar(BaseModel):
    nombre: str
    coords: List[float]

# Crear la aplicación FastAPI
app = FastAPI()

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
        # Guardar el mapa en un archivo HTML
        mapa.save(f"mapa_dia_{i+1}.html")

    return {"message": f"Mapas guardados correctamente en {os.getcwd()}"}

# Ejecutar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)