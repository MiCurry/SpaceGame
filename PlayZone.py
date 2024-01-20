import datetime
from typing import Tuple
from dataclasses import dataclass

import arcade

from SpaceGameTypes.PlayZoneTypes import Wall, SpaceObject, Background
from SpaceGameTypes.SpaceStations import stations_small, stations_big

import random

@dataclass
class SpaceJunkGeneratorRanges:
    num_stations_small: Tuple[int, int]
    num_stations_big: Tuple[int, int]
    
    # Range of velocity values in x and y directions
    stations_big_velocity: Tuple[float, float]
    stations_small_velocity: Tuple[float, float]

    
DEFAULT_GEN_RANGES = SpaceJunkGeneratorRanges(
    num_stations_small=(15, 30),
    num_stations_big=(1, 3),
    stations_big_velocity=(-3, 3),
    stations_small_velocity=(-10, 10)
)

"""
 This class is responsible for creating the play zone. The background,
 the edges of the play zone and the objects within it.
 """
class PlayZone:
    def __init__(self,
                 game,
                 background: Background, 
                 dimension: Tuple[int, int],
                 seed='time'):
        self.main = game
        self.engine = game.physics_engine
        self.space = game.physics_engine.space
        self.background = background
        self.play_zone_width_height = dimension
        self.dimensions = self.calculate_dimensions_pixels()
        self.bg_sprite_list = []
        self.walls = []
        self.setup()
        self.seed = seed
        self._seed

    @property
    def width(self) -> float:
        return self.dimensions[0]

    @property
    def height(self) -> float:
        return self.dimensions[1]

    @property
    def seed(self) -> int:
        return self._seed

    @seed.setter
    def seed(self, seed='time'):
        if seed == 'time':
            self._seed = datetime.datetime.now().timestamp()
        else:
            self._seed = seed

    def seed_seed(self):
        random.seed(self._seed)

    def setup_playzone_boundry(self):
        self.create_playzone_walls()

    def setup(self):
        self.setup_spritelists()
        self.tile_background()
        self.setup_playzone_boundry()
        self.generate_spacejunk()

    def setup_spritelists(self):
        self.bg_sprite_list = arcade.SpriteList()
        self.spacejunk = arcade.SpriteList()

    def calculate_dimensions_pixels(self) -> Tuple[float, float]:
        return (self.play_zone_width_height[0] * self.background.width,
                self.play_zone_width_height[1] * self.background.height)

    def tile_background(self):
        for i in range(0, self.play_zone_width_height[0] + 1):
            for j in range(0, self.play_zone_width_height[1] + 1):
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

    def update(self):
        self.spacejunk.update()

    def reset(self):
        pass

    def generate_spacejunk(self):
        generator = SpaceJunkGenerator(self.main, self)
        objects = generator.generate_objects()
        for object in objects:
            self.add_space_object(object)
        
    def add_space_object(self, spaceObject: SpaceObject):
        self.spacejunk.append(spaceObject)
 


@dataclass
class SpaceJunkGenerateData:
    num_stations_big: int
    num_stations_small: int

# Class to randomly select space junk and give it random position and velocity
class SpaceJunkGenerator:
    def __init__(self,
                 main,
                 playzone,
                 seed='random',
                 data=None,
                 ranges=DEFAULT_GEN_RANGES):
        
        self.main = main
        self.playzone = playzone
        self.ranges = ranges
        self.objects = []

        if data:
            self.seed = seed
            self.data = data
        else:
            self.seed = seed
            self.data = self.generateSpaceJunkData()
        
        self.seed_seed()

    def random_x(self):
        return random.randrange(0, self.playzone.width)

    def random_y(self):
        return random.randrange(0, self.playzone.height)

    def random_position(self):
        return (self.random_x(), self.random_y())

    def random_velocity(self, range):
        return (random.randrange(range[0], range[1]),
                random.randrange(range[0], range[1]))

    def _initalize_objects(self, object, velocity_range):
        object.position = self.random_position()
        object.setup()
        object.body.velocity = (self.random_velocity(velocity_range))

    def _generate_objects(self, dataObjects, n_objects, velocity_range) -> []:
        for i in range(0, n_objects):
            dataObject = random.choice(dataObjects)
            obj = SpaceObject(dataObject, self.main)
            self._initalize_objects(obj, velocity_range)
            self.objects.append(obj)

        return self.objects

    def generate_stations_small(self):
        return self._generate_objects(stations_small,
                                      self.data.num_stations_small,
                                      self.ranges.stations_small_velocity)

    def generate_stations_big(self):
        return self._generate_objects(stations_big,
                                      self.data.num_stations_big,
                                      self.ranges.stations_big_velocity)

    def generate_objects(self):
        self.generate_stations_small()
        self.generate_stations_big()
        return self.objects

    @property
    def seed(self) -> int:
        return self._seed

    @seed.setter
    def seed(self, seed='random'):
        if seed == 'random':
            self._seed = datetime.datetime.now().timestamp()
        else:
            self._seed = seed

    def seed_seed(self):
        random.seed(self._seed)

    def generateSpaceJunkData(self):
        return SpaceJunkGenerateData(num_stations_small=self._generate_n_stations_small(),
                                     num_stations_big=self._generate_n_stations_big())

    def _generate_n_stations_small(self):
        return random.randint(self.ranges.num_stations_small[0],
                              self.ranges.num_stations_small[1])

    def _generate_n_stations_big(self):
        return random.randint(self.ranges.num_stations_big[0],
                              self.ranges.num_stations_big[1])

