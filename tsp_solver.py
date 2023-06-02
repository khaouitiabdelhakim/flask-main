import sqlite3
from docplex.mp.model import Model
from scipy.spatial import distance_matrix
from math import radians, sin, cos, sqrt, atan2

def calculate_distance(coord1, coord2):
    # approximate radius of Earth in km
    R = 6371.0

    # Convert coordinates from degrees to radians
    lon1 = radians(coord1[0])
    lat1 = radians(coord1[1])
    lon2 = radians(coord2[0])
    lat2 = radians(coord2[1])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def calculate_distance_last(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Haversine formula to calculate distance between two points on a sphere
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = 6371 * c  # 6371 is the approximate radius of the Earth in kilometers

    return distance * 1000



def tsp_solver(pharmacies):
    num_pharmacies = len(pharmacies)

    # Calculate distance matrix
    distances = distance_matrix(pharmacies, pharmacies)

    print("1st print")
    print(distances)

    # Create a CPLEX model
    model = Model(name='TSP')

    # Create binary variables: decision variables
    x = {(i, j): model.binary_var(name='x_{0}_{1}'.format(i, j)) for i in range(num_pharmacies) for j in range(num_pharmacies)}

    # Objective function
    model.minimize(model.sum(distances[i][j] * x[i, j] for i in range(num_pharmacies) for j in range(num_pharmacies)))

    # Constraints
    for i in range(num_pharmacies):
        model.add_constraint(model.sum(x[i, j] for j in range(num_pharmacies) if j != i) == 1)
        model.add_constraint(model.sum(x[j, i] for j in range(num_pharmacies) if j != i) == 1)

    # Solve the model
    solution = model.solve()
    print(solution)


    # Extract the optimal trajectory
    optimal_trajectory = []
    current = 0

    for _ in range(num_pharmacies):
        optimal_trajectory.append(current)
        for j in range(num_pharmacies):
            if solution.get_value(x[current, j]) == 1:
                current = j
                break

    return optimal_trajectory

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Retrieve the coordinates of pharmacies from the database
pharmacies = []
cursor.execute("SELECT Latitude, Longitude FROM Pharmacies")
rows = cursor.fetchall()
for row in rows:
    latitude, longitude = row
    pharmacies.append((latitude, longitude))

# Close the database connection
cursor.close()
conn.close()

# Solve TSP using the coordinates
optimal_trajectory = tsp_solver(pharmacies)
print(optimal_trajectory)
