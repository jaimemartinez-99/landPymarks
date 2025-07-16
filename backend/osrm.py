import requests
import folium

def get_osrm_trip_route(locations, profile='foot'):
    coords_str = ";".join([f"{lon},{lat}" for lat, lon in locations])
    url = f"http://router.project-osrm.org/trip/v1/{profile}/{coords_str}?roundtrip=false&overview=full&geometries=geojson"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error en OSMR: {response.text}")

    data = response.json()
    trip = data['trips'][0]
    waypoints = data['waypoints']
    ordered_indices = [w['waypoint_index'] for w in sorted(waypoints, key=lambda x: x['trips_index'])]

    ordered_locations = [locations[i] for i in ordered_indices]

    return ordered_locations, trip['geometry']

def create_map_with_route(locations, geometry, ordered_names):
    m = folium.Map(location=locations[0], zoom_start=14)
    for i, ((lat, lon), name) in enumerate(zip(locations, ordered_names)):
        folium.Marker(
            location=[lat, lon],
            tooltip=f"{i + 1}. {name}",
            popup=name,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    raw_geometry = geometry['coordinates']

    geometry_latlon = [[lat, lon] for lon, lat in raw_geometry]

    folium.PolyLine(locations=geometry_latlon, color='red', weight=4.5, opacity=0.8).add_to(m)

    return m