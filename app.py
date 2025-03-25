from flask import Flask, request, jsonify
from flask_cors import CORS
import itertools

app = Flask(__name__)
CORS(app)  # Allows frontend to make API requests


import httpx
import asyncio
from geopy.distance import geodesic


async def get_coordinates(place):
    api_key = '9a921f555eac4c8cbd4bb4ff9af0542a'  # Replace with your actual API key
    url = f"https://api.opencagedata.com/geocode/v1/json?q={place}&key={api_key}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200 and response.text.strip():
        data = response.json()
        if data['results']:
            lat = data['results'][0]['geometry']['lat']
            lon = data['results'][0]['geometry']['lng']
            return float(lat), float(lon)  # Selecting the first result
    return None

def compute_distances(locations):
    graph = {}
    for city1, coord1 in locations.items():
        graph[city1] = {}
        for city2, coord2 in locations.items():
            if city1 != city2:
                graph[city1][city2] = round(geodesic(coord1, coord2).km, 2)
    return graph

async def main(places):
    
    # Get locations asynchronously
    locations = {place["name"]: await get_coordinates(place["name"]) for place in places}


    # Compute distances
    distances = compute_distances(locations)
    cities = list(distances.keys())
    city_index = {city: i for i, city in enumerate(cities)}
    n = len(cities)

    # Create adjacency matrix
    adj_matrix = [[float('inf')] * n for _ in range(n)]
    for city1 in distances:
        for city2 in distances[city1]:
            i, j = city_index[city1], city_index[city2]
            adj_matrix[i][j] = distances[city1][city2]

    # DP + Bitmasking (Held-Karp Algorithm)
    dp = [[float('inf')] * n for _ in range(1 << n)]
    path = [[-1] * n for _ in range(1 << n)]

    # Base case: starting from each city
    for i in range(n):
        dp[1 << i][i] = 0
    
    # Iterate over subsets of visited cities
    for mask in range(1 << n):
        for last in range(n):
            if (mask & (1 << last)) == 0:
                continue  # Skip if city `last` is not in subset
            
            for prev in range(n):
                if last == prev or (mask & (1 << prev)) == 0:
                    continue  # Skip if `prev` is not in subset
                
                new_cost = dp[mask ^ (1 << last)][prev] + adj_matrix[prev][last]
                if new_cost < dp[mask][last]:
                    dp[mask][last] = new_cost
                    path[mask][last] = prev
    
    # Find the minimum cost path
    # Ensure the route returns to the start city
    full_mask = (1 << n) - 1

    start_city = 0  # Assuming the first city in input is the starting city
    min_cost = float('inf')
    end_city = -1

    for last in range(n):
        cost_with_return = dp[full_mask][last] + adj_matrix[last][start_city]  # Add cost to return to start
        if cost_with_return < min_cost:
            min_cost = cost_with_return
            end_city = last

    # min_cost = float('inf')
    # end_city = -1
    
    # for last in range(n):
    #     if dp[full_mask][last] < min_cost:
    #         min_cost = dp[full_mask][last]
    #         end_city = last
    
    # Reconstruct the path
    route = []
    mask = full_mask
    while end_city != -1:
        route.append({
            "name": cities[end_city],
            "coords": list(locations[cities[end_city]])
        })
        next_city = path[mask][end_city]
        mask ^= (1 << end_city)
        end_city = next_city
    
    if route:
        route.append({
            "name": route[0]["name"],  # Add starting city at the end
            "coords": route[0]["coords"]
    })
    
    # Output the result
    return {
        "path": route,
        "total_distance": round(min_cost, 2)
    }



@app.route("/shortest-path", methods=["POST"])
def shortest_path():
    data = request.json
    places = data.get("places", [])
    if not places:
        return jsonify({"error": "No places provided"}), 400
    
    result = asyncio.run(main(places))
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)