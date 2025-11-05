import math

import arcade
from pymunk.vec2d import Vec2d

def squared_distance_sprite(a: arcade.Sprite, b: arcade.Sprite) -> float:
    return (a.center_x - b.center_x) ** 2 + (a.center_y - b.center_y) ** 2


def distance_sprite(a: arcade.Sprite, b: arcade.Sprite) -> float:
    return math.sqrt(squared_distance_sprite(a, b))


def x_y_distance_sprite(a: arcade.Sprite, b: arcade.Sprite):
    return (a.center_x - b.center_x), (a.center_y - b.center_y)
