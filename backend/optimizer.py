import numpy as np
from k_means_constrained import KMeansConstrained
from calculator import calculate_distance_meters

def optimize_route(points):
    if not points:
        return []

    route = [points[0]]
    points_left = points[1:]

    while points_left:
        closest_point = min(
            points_left,
            key=lambda x: min(calculate_distance_meters(p["coords"], x["coords"]) for p in route),
        )

        best_position = 0
        best_distance = float('inf')

        for i in range(len(route)):
            previous_distance = calculate_distance_meters(route[i]["coords"], closest_point["coords"])
            if i + 1 < len(route):
                next_distance = calculate_distance_meters(closest_point["coords"], route[i + 1]["coords"])
                original_distance = calculate_distance_meters(route[i]["coords"], route[i + 1]["coords"])
                distance_increase = previous_distance + next_distance - original_distance
            else:
                distance_increase = previous_distance

            if distance_increase < best_distance:
                best_distance = distance_increase
                best_position = i + 1

        route.insert(best_position, closest_point)
        points_left.remove(closest_point)

    return route

def group_points(points, num_days):
    points = [p for p in points if p["coords"] is not None]

    coordinates = np.array([p["coords"] for p in points], dtype=float)
    
    min_size = len(points) // num_days
    max_size = min_size + 1 if len(points) % num_days != 0 else min_size

    kmeans = KMeansConstrained(n_clusters=num_days, size_min=min_size, size_max=max_size, random_state=0)
    kmeans.fit(coordinates)
    
    groups = [[] for _ in range(num_days)]
    for i, label in enumerate(kmeans.labels_):
        groups[label].append(points[i])
    
    return groups