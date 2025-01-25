from geopy.distance import geodesic

# Función para calcular la distancia entre dos puntos
def calcular_distancia(coord1, coord2):
    return geodesic(coord1, coord2).meters