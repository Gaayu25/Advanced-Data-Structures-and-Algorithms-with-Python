from collections import deque

# --- Metro Map as Graph (Adjacency List) ---
metro = {
    "Central": ["Park", "CityHall"],
    "Park": ["Central", "Museum", "Garden"],
    "CityHall": ["Central", "Harbor"],
    "Museum": ["Park", "Library"],
    "Garden": ["Park", "Stadium"],
    "Harbor": ["CityHall", "Airport"],
    "Library": ["Museum"],
    "Stadium": ["Garden"],
    "Airport": ["Harbor"]
}

# --- BFS Shortest Path Function ---
def shortest_path(graph, start, end):
    visited = set()
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        station = path[-1]

        if station == end:
            return path

        if station not in visited:
            visited.add(station)
            for neighbor in graph[station]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None

# --- USER INPUT & OUTPUT ---
start = input("Enter starting station: ")
dest = input("Enter destination station: ")

if start not in metro or dest not in metro:
    print("Invalid station!")
else:
    result = shortest_path(metro, start, dest)
    if result:
        print("\nShortest Path:")
        print(" → ".join(result))
        print(f"Total Stations: {len(result)}")
    else:
        print("No route found!")
