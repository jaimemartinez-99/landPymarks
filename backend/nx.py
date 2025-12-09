import folium
from folium.plugins import BeautifyIcon
import numpy as np
import networkx as nx
import time
from calculator import calculate_distance_kilometers
from loguru import logger


def compute_distance_matrix(coordinates):
    num_points = len(coordinates)
    distance_matrix = np.zeros((num_points, num_points))

    for i in range(num_points):
        for j in range(i + 1, num_points):
            dist = calculate_distance_kilometers(coordinates[i], coordinates[j])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist

    return distance_matrix


def solve_tsp_optimized(distance_matrix):
    G = nx.Graph()
    for i in range(len(distance_matrix)):
        for j in range(i + 1, len(distance_matrix)):
            G.add_edge(i, j, weight=distance_matrix[i, j])

    return nx.approximation.traveling_salesman_problem(G, cycle=False)


def solve_tsp_and_create_map(coordinates, names):
    start_time = time.time()

    distance_matrix = compute_distance_matrix(coordinates)
    tsp_start = time.time()

    best_path = solve_tsp_optimized(distance_matrix)

    tsp_end = time.time()
    logger.info(f"Time for TSP problem: {tsp_end - tsp_start:.2f} seconds")

    optimized_route = [coordinates[i] for i in best_path]

    map_creation_start = time.time()
    m = folium.Map(location=coordinates[0], zoom_start=14)

    marker_group = folium.FeatureGroup(name="Markers")
    for i, idx in enumerate(best_path):
        folium.Marker(
            location=coordinates[idx],
            popup=f"Point {i + 1}: {names[idx]}",
            icon=BeautifyIcon(
                icon="arrow-down",
                icon_shape="marker",
                number=i + 1,
                border_color="blue",
                background_color="white",
                text_color="blue"
            ),
        ).add_to(marker_group)

    marker_group.add_to(m)

    colors = ["red", "blue", "green", "purple", "orange", "darkred", "darkblue", "darkgreen", "cadetblue", "pink"]

    for i in range(len(optimized_route) - 1):
        folium.PolyLine([optimized_route[i], optimized_route[i + 1]],
                        color=colors[i % len(colors)],
                        weight=4, opacity=0.7).add_to(m)

    map_creation_end = time.time()
    logger.info(f"Map creation time: {map_creation_end - map_creation_start:.2f} seconds")

    total_time = time.time() - start_time
    logger.info(f"Total execution time: {total_time:.2f} seconds")
    return m