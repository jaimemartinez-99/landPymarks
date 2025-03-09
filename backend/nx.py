import folium
import itertools
import time
from calculator import calculate_distance_kilometers
from loguru import logger


def solve_tsp_and_create_map(coordinates, names):
    start_time = time.time()

    distance_matrix = {}
    for i, j in itertools.combinations(range(len(coordinates)), 2):
        dist = calculate_distance_kilometers(coordinates[i], coordinates[j]) 
        distance_matrix[(i, j)] = dist
        distance_matrix[(j, i)] = dist  

    tsp_start = time.time()
    tsp_path = list(itertools.permutations(range(len(coordinates))))
    shortest_distance = float("inf")
    best_path = None
    for path in tsp_path:
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += distance_matrix.get((path[i], path[i+1]), float("inf"))
        if total_distance < shortest_distance:
            shortest_distance = total_distance
            best_path = path

    tsp_end = time.time()
    logger.info(f"Time for TSP problem: {tsp_end - tsp_start:.2f} seconds")

    optimized_route = [coordinates[i] for i in best_path]

    map_creation_start = time.time()
    m = folium.Map(location=coordinates[0], zoom_start=14)

   
    for i, idx in enumerate(best_path): 
        coord = coordinates[idx]
        name = names[idx]  
        folium.Marker(
            location=coord,
            popup=f"Point {i+1}: {name}",  
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)

    colors = ["red", "blue", "green", "purple", "orange", "darkred", "darkblue", "darkgreen", "cadetblue", "pink"]

    for i in range(len(optimized_route) - 1):
        origin_coord, destination_coord = optimized_route[i], optimized_route[i + 1]

        route_coords = [origin_coord, destination_coord]
        route_color = colors[i % len(colors)]  
        folium.PolyLine(route_coords, color=route_color, weight=4, opacity=0.7).add_to(m)

    map_creation_end = time.time()
    logger.info(f"Map creation time: {map_creation_end - map_creation_start:.2f} seconds")

    total_time = time.time() - start_time
    logger.info(f"Total execution time: {total_time:.2f} seconds")
    return m
 
