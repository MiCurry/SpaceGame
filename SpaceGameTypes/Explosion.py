from typing import Tuple
import arcade

explosion_texture = arcade.load_spritesheet(":resources:images/spritesheets/explosion.png",
                                256, 
                                256,
                                16,
                                60)

class Explosion(arcade.Sprite):
    BIG = 2.0
    NORMAL = 1.0
    SMALL = 0.5

    def __init__(self, position: Tuple, scale: int):
        super().__init__()
        self.center_x = position[0]
        self.center_y = position[1]
        self.scale = scale
        self.current_texture = 0
        self.textures = explosion_texture

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(explosion_texture):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()