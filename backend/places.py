import requests 

def get_osm_coordinates(place_name, city):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{place_name}, {city}",
        "format": "json",
        "limit": 1
    }
    
    headers = {
        "User-Agent": "MiAplicacion/1.0 (contact@example.com)"}  

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data:
            return [float(data[0]["lat"]), float(data[0]["lon"])]  
        return None

    except requests.exceptions.RequestException as e:
        print(f"🚨 Error in request for {place_name}: {e}")
        return None

def update_coordinates(places, city):
    updated_places = []
    
    for place in places:
        coords_osm = get_osm_coordinates(place["nombre"], city)
        
        if coords_osm is not None:
            place["coords"] = coords_osm  
        
        updated_places.append(place)
    
    return updated_places

def delete_duplicates(places):
    unique_places = {}
    
    for place in places:
        name = place["nombre"]
        
        if name not in unique_places:
            unique_places[name] = place 
    
    return list(unique_places.values())