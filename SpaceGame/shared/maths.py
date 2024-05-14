import math


def squared_distance(a, b) -> float:
    return (a.center_x - b.center_x) ** 2 + (a.center_y - b.center_y) ** 2


def distance(a, b) -> float:
    return math.sqrt(squared_distance(a, b))