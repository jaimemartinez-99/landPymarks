import os
import requests

def get_osm_coordinates(place_name, city):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{place_name}, {city}",
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "OptiMapper/1.0 (ermabe31@gmail.com)"}

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

def get_geoapify_coordinates(place_name, city):
    api_key= os.environ["GEOAPIFY_API_KEY"]
    url = "https://api.geoapify.com/v1/geocode/search"
    params = {
        "text": f"{place_name}, {city}",
        "format": "json",
        "apiKey": api_key,
        "limit": 1
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data["results"]:
        lat = data["results"][0]["lat"]
        lon = data["results"][0]["lon"]
        return [lat, lon] # Devolver [lat, lon]

    return None

def update_coordinates(places, city):
    updated_places = []
    
    for place in places:
        coords_osm = get_geoapify_coordinates(place["nombre"], city)
        
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