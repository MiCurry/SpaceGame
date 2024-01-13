from typing import Tuple, List
from dataclasses import dataclass
from enum import Enum

import arcade
import pymunk

from SpaceGameTypes.PlayZoneTypes import Wall, SpaceObject, Background
from SpaceGameTypes.SpaceStations import StationSputnik1

"""
 This class is responsible for creating the play zone. The background,
 the edges of the play zone and the objects within it.
 """
class PlayZone:
    def __init__(self,
                 game,
                 background: Background, 
                 dimension: Tuple[int, int]):
        self.main = game
        self.engine = game.physics_engine
        self.space = game.physics_engine.space
        self.background = background
        self.play_zone_wh = dimension
        self.dimensions = self.calculate_dimensions_pixels()
        self.bg_sprite_list = []
        self.walls = []
        self.setup()

    def setup_playzone_boundry(self):
        self.create_playzone_walls()

    def setup(self):
        self.setup_spritelists()
        self.tile_background()
        self.setup_playzone_boundry()
        self.create_spacejunk()

    def setup_spritelists(self):
        self.bg_sprite_list = arcade.SpriteList()
        self.spacejunk = arcade.SpriteList()


    def calculate_dimensions_pixels(self) -> Tuple[float, float]:
        return (self.play_zone_wh[0] * self.background.width,
                self.play_zone_wh[1] * self.background.height)

    def tile_background(self):
        for i in range(0, self.play_zone_wh[0] + 1):
            for j in range(0, self.play_zone_wh[1] + 1):
                tile = arcade.Sprite(self.background.image,
                                    center_x=(i * self.background.width),
                                    center_y=(j * self.background.height))
                self.bg_sprite_list.append(tile)
    
    def create_playzone_walls(self):
        left_wall = Wall((0.0, 0.0),
                        (0.0, self.dimensions[1]))
        right_wall = Wall((self.dimensions[0], 0.0),
                        (self.dimensions[0], self.dimensions[1]))
        top_wall = Wall((0.0, self.dimensions[1]),
                        (self.dimensions[0], self.dimensions[1]))
        bottom_wall = Wall((0.0, 0.0),
                        (self.dimensions[0], 0.0))

        self.walls.append(left_wall)
        self.walls.append(right_wall)
        self.walls.append(top_wall)
        self.walls.append(bottom_wall)

    def add_walls_to_pymunk_space(self):
        for wall in self.walls:
            self.space.add(wall.segment, wall.segment.body)

    def draw_walls(self):
        for wall in self.walls:
            body = wall.segment.body

            pv1 = body.position + wall.segment.a.rotated(body.angle)
            pv2 = body.position + wall.segment.b.rotated(body.angle)
            arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, arcade.color.WHITE, 2)

    def draw_background(self):
        self.bg_sprite_list.draw()

    def draw_spacejunk(self):
        self.spacejunk.draw()

    def draw(self):
        self.draw_background()
        self.draw_walls()
        self.draw_spacejunk()

    def create_spacejunk(self):
        junk = SpaceObject(StationSputnik1)
        junk.position = (200, 200)
        self.main.add_sprite_to_pymunk(junk)
        self.spacejunk.append(junk)

