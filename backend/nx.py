import osmnx as ox
import networkx as nx
import folium
import itertools
import time

# Iniciar temporizador para todo el proceso
start_time = time.time()

# Define la ciudad
city = "New York City, USA"

# Temporizador para la descarga del grafo
download_start = time.time()
G = ox.graph_from_place(city, network_type="walk", simplify=True)
download_end = time.time()
print(f"Tiempo de descarga del grafo: {download_end - download_start:.2f} segundos")

# Lista de coordenadas (puedes cambiarlas)
coordinates = [
    (40.748817, -73.985428),  # Empire State Building
    (40.720562, -73.951861),  # Williamsburg
    (40.730610, -73.935242),  # Queens
    (40.712776, -74.005974),  # One World Trade Center
    (40.785091, -73.968285),  # Central Park
    (40.758896, -73.985130),  # Times Square
    (40.706192, -74.008874),  # Wall Street
    (40.742054, -74.004776),  # Chelsea Market
    (40.721319, -73.987130)   # Lower East Side
]

node_conversion_start = time.time()
nodes = [ox.distance.nearest_nodes(G, X=lon, Y=lat) for lat, lon in coordinates]
node_conversion_end = time.time()
print(f"Tiempo de conversión de coordenadas a nodos: {node_conversion_end - node_conversion_start:.2f} segundos")

graph_creation_start = time.time()
complete_graph = nx.Graph()
for i, j in itertools.combinations(range(len(nodes)), 2):
    length = nx.shortest_path_length(G, nodes[i], nodes[j], weight="length")
    complete_graph.add_edge(i, j, weight=length)
graph_creation_end = time.time()
print(f"Tiempo de creación del grafo completo: {graph_creation_end - graph_creation_start:.2f} segundos")


tsp_start = time.time()
tsp_path = nx.approximation.traveling_salesman_problem(complete_graph, cycle=False)
tsp_end = time.time()
print(f"Tiempo de solución del problema del viajante de comercio (TSP): {tsp_end - tsp_start:.2f} segundos")

# Convertir el camino en nodos del grafo original
optimized_route = [nodes[i] for i in tsp_path]

# Crear un mapa centrado en el primer punto
map_creation_start = time.time()
m = folium.Map(location=coordinates[0], zoom_start=14)

# Agregar marcadores para cada punto en el orden optimizado
for i, idx in enumerate(tsp_path):  # Usar el orden de la ruta optimizada
    coord = coordinates[idx]
    folium.Marker(
        location=coord,
        popup=f"Point {i+1}: {coord}",
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

# Lista de colores para diferenciar los tramos
colors = ["red", "blue", "green", "purple", "orange", "darkred", "darkblue", "darkgreen", "cadetblue", "pink"]

# Dibujar la ruta óptima en el mapa
for i in range(len(optimized_route) - 1):
    origin_node, destination_node = optimized_route[i], optimized_route[i + 1]

    # Encuentra la ruta óptima entre estos dos puntos
    shortest_path_start = time.time()
    shortest_path = nx.shortest_path(G, origin_node, destination_node, weight="length")
    shortest_path_end = time.time()
    print(f"Tiempo de cálculo de la ruta óptima entre puntos {i+1} y {i+2}: {shortest_path_end - shortest_path_start:.2f} segundos")

    # Extrae las coordenadas de la ruta
    route_coords = [[G.nodes[node]["y"], G.nodes[node]["x"]] for node in shortest_path]

    # Selecciona un color diferente para cada tramo
    route_color = colors[i % len(colors)]  

    # Dibuja la línea en el mapa
    folium.PolyLine(route_coords, color=route_color, weight=4, opacity=0.7).add_to(m)

# Guardar el mapa en un archivo HTML
map_creation_end = time.time()
m.save("optimized_tsp_route.html")
print(f"Tiempo de creación del mapa: {map_creation_end - map_creation_start:.2f} segundos")

