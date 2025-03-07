import numpy as np
from k_means_constrained import KMeansConstrained
from calculator import calcular_distancia

def optimizar_ruta(puntos):
    if not puntos:
        return []

    # Iniciar con el primer punto
    ruta = [puntos[0]]
    puntos_restantes = puntos[1:]

    while puntos_restantes:
        # Encontrar el punto no visitado más cercano a cualquier punto de la ruta
        punto_mas_cercano = min(
            puntos_restantes,
            key=lambda x: min(calcular_distancia(p["coords"], x["coords"]) for p in ruta),
        )

        # Encontrar la posición óptima para insertar el punto
        mejor_posicion = 0
        mejor_distancia = float('inf')

        for i in range(len(ruta)):
            # Calcular la distancia si se inserta el punto entre ruta[i] y ruta[i+1]
            distancia_antes = calcular_distancia(ruta[i]["coords"], punto_mas_cercano["coords"])
            if i + 1 < len(ruta):
                distancia_despues = calcular_distancia(punto_mas_cercano["coords"], ruta[i + 1]["coords"])
                distancia_original = calcular_distancia(ruta[i]["coords"], ruta[i + 1]["coords"])
                aumento_distancia = distancia_antes + distancia_despues - distancia_original
            else:
                aumento_distancia = distancia_antes

            # Actualizar la mejor posición
            if aumento_distancia < mejor_distancia:
                mejor_distancia = aumento_distancia
                mejor_posicion = i + 1

        # Insertar el punto en la posición óptima
        ruta.insert(mejor_posicion, punto_mas_cercano)
        puntos_restantes.remove(punto_mas_cercano)

    return ruta

# Función para agrupar los puntos en clusters equilibrados
def agrupar_puntos(puntos, num_dias):
    # Extraer las coordenadas
    puntos = [p for p in puntos if p["coords"] is not None]

    # Extraer las coordenadas
    coordenadas = np.array([p["coords"] for p in puntos], dtype=float)
    
    # Calcular el tamaño mínimo y máximo de cada cluster
    min_size = len(puntos) // num_dias
    max_size = min_size + 1 if len(puntos) % num_dias != 0 else min_size

    # Aplicar K-Means con restricciones de tamaño
    kmeans = KMeansConstrained(n_clusters=num_dias, size_min=min_size, size_max=max_size, random_state=0)
    kmeans.fit(coordenadas)
    
    # Asignar cada punto a un cluster
    grupos = [[] for _ in range(num_dias)]
    for i, etiqueta in enumerate(kmeans.labels_):
        grupos[etiqueta].append(puntos[i])
    
    return grupos