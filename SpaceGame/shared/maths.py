import math


def squared_distance(a, b) -> float:
    return (a.center_x - b.center_x) ** 2 + (a.center_y - b.center_y) ** 2


def distance(a, b) -> float:
    return math.sqrt(squared_distance(a, b))


def x_y_distance(a, b):
    return (a.center_x - b.center_x), (a.center_y - b.center_y)
