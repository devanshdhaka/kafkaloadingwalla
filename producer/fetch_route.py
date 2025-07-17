import requests
import polyline

HEADERS = {"User-Agent": "kafka-gps-simulator/1.0 (devansh@example.com)"}  

def get_coords(place):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={place}"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        raise Exception(f"Nominatim error: {res.status_code} -> {res.text}")

    data = res.json()
    if not data:
        raise Exception(f"No results for {place}")

    return float(data[0]["lat"]), float(data[0]["lon"])


start_place = "Sector 55, Faridabad, Haryana"
end_place = "Saket Metro Station, Delhi"

# ✅ Fetch start & end coordinates
start_lat, start_lon = get_coords(start_place)
end_lat, end_lon = get_coords(end_place)

print(f"Start: {start_lat},{start_lon} → End: {end_lat},{end_lon}")

# ✅ Get driving route via OSRM (free)
route_url = f"https://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=full"
route_res = requests.get(route_url, headers=HEADERS).json()

if "routes" not in route_res:
    raise Exception("OSRM route API failed:", route_res)

polyline_str = route_res["routes"][0]["geometry"]
route_points = polyline.decode(polyline_str)

print(f"Total points: {len(route_points)}")
print("First 5 points:", route_points[:5])
