import requests 

def get_osm_coordinates(place_name, city):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{place_name}, {city}",
        "format": "json",
        "limit": 1
    }
    
    headers = {
        "User-Agent": "MiAplicacion/1.0 (contacto@ejemplo.com)"}  

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data:
            return [float(data[0]["lat"]), float(data[0]["lon"])]  # ✅ Solo devuelve la lista
        return None

    except requests.exceptions.RequestException as e:
        print(f"🚨 Error en la petición para {place_name}: {e}")
        return None

def update_coordinates(lugares, ciudad):
    lugares_actualizados = []
    
    for lugar in lugares:
        coords_osm = get_osm_coordinates(lugar["nombre"], ciudad)
        
        if coords_osm is not None:
            lugar["coords"] = coords_osm  # Usar las coordenadas de OSM si están disponibles
        # Si no, se mantienen las originales de DeepSeek
        
        lugares_actualizados.append(lugar)
    
    return lugares_actualizados

def delete_duplicates(lugares):
    lugares_unicos = {}
    
    for lugar in lugares:
        nombre = lugar["nombre"]
        
        if nombre not in lugares_unicos:
            lugares_unicos[nombre] = lugar  # ✅ Guarda el primer lugar con ese nombre
    
    return list(lugares_unicos.values())