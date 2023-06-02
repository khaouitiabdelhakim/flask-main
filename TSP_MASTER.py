from math import  sqrt
from sys import maxsize
from itertools import permutations


 
def calculate_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def calculate_distance_matrix(points):
    num_points = len(points)
    distance_matrix = [[0] * num_points for _ in range(num_points)]

    for i in range(num_points):
        for j in range(num_points):
            distance_matrix[i][j] = calculate_distance(points[i], points[j])

    return distance_matrix



def TSP_Solver(pharmacies, s):
    graph = calculate_distance_matrix(pharmacies)
    vertex = []
    V = len(graph)
    for i in range(V):
        if i != s:
            vertex.append(i)

    min_path = maxsize
    next_permutation = permutations(vertex)
        
    
    for i in next_permutation:
        current_pathweight = 0
        k = s
        for j in i:
            current_pathweight += graph[k][j]
            k = j
        current_pathweight += graph[k][s]

        if current_pathweight < min_path:
            min_path = current_pathweight
            trajectory = i
    optimal = [s]
    for l in trajectory:
        optimal.append(l)
    optimal.append(s)   
    return min_path,optimal



