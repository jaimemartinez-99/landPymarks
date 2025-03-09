from geopy.distance import geodesic

def calculate_distance_meters(coord1, coord2):
    return geodesic(coord1, coord2).meters

# Calcula la distancia geodésica entre dos coordenadas
def calculate_distance_kilometers(coord1, coord2):
    return geodesic(coord1, coord2).kilometers 