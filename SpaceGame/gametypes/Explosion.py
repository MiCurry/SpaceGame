import os
from typing import Tuple
from enum import Enum

import arcade


class ExplosionSize(Enum):
    BIG = 2.0
    NORMAL = 1.0
    SMALL = 0.5


explosion_cols = 16
explosion_count = 60
explosion_width = 256
explosion_height = 256
sprite = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "resources/spritesheet/explosion.png")
expolosion_spritesheet = arcade.load_spritesheet(sprite)
explosion_texture_list = expolosion_spritesheet.get_texture_grid(
    size=(explosion_width, explosion_height),
    columns=explosion_cols,
    count=explosion_count
)

"""
explosion_texture = arcade.load_spritesheet(sprite,
                                            256,
                                            256,
                                            16,
                                            60)
"""


class Explosion(arcade.Sprite):
    def __init__(self, position: Tuple, scale: ExplosionSize):
        super().__init__(explosion_texture_list[0])
        self.textures = explosion_texture_list
        self.current_texture = 0
        self.center_x = position[0]
        self.center_y = position[1]
        self.scale = scale.value

    def update(self, dleta):
        self.current_texture += 1
        if self.current_texture < len(explosion_texture_list):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()
