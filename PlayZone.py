from dataclasses import dataclass
import arcade

@dataclass
class Background:
    image: str
    width: float
    height: float
    scale: float


"""
 This class is responsible for creating the play zone. The background,
 the edges of the play zone and the objects within it.

 """
class PlayZone():
    def __init__(self, bg_sprite_list: [], background: Background, dimension: (int, int)):
        self.background = background
        self.bg_sprite_list = bg_sprite_list
        self.dimensions = dimension

    def tile_background(self):
        for i in range(0, self.dimensions[0]):
            for j in range(0, self.dimensions[1]):
                tile = arcade.Sprite(self.background.image,
                                    center_x=(i * self.background.width),
                                    center_y=(j * self.background.height))
                self.bg_sprite_list.append(tile)
    
