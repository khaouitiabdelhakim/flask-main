import itertools

def calculate_distance(point1, point2):
    # Calculer la distance entre deux points en utilisant la formule de distance euclidienne
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def tsp_solver(points):
    # Générer toutes les permutations possibles des points
    permutations = list(itertools.permutations(points))

    shortest_distance = float('inf')
    shortest_path = None

    # Parcourir toutes les permutations et trouver la plus courte distance
    for path in permutations:
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += calculate_distance(path[i], path[i+1])

        # Vérifier si cette permutation a une distance plus courte
        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_path = path

    return shortest_path, shortest_distance

# Exemple d'utilisation
n_stops = 4
points = [(0, 7), (3, 1), (6, 2), (3, 4)]

shortest_path, shortest_distance = tsp_solver(points[:n_stops])
print("Plus court chemin:", shortest_path)
print("Distance minimale:", shortest_distance)
