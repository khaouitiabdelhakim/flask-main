from math import radians, sin, cos, sqrt, atan2

def calculate_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R=6.3781*(10**6)

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
    distance = R * c  # R is the radius of the Earth

    return distance

pharmacy1 = (33.978053, -6.854125)
pharmacy2 = (33.979764, -6.85488)

distance = calculate_distance(pharmacy1, pharmacy2)
print(distance)
