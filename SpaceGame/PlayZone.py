import datetime
from typing import Optional, Tuple
from dataclasses import dataclass

import arcade

from SpaceGame.gametypes.PlayZoneTypes import Wall, SpaceObject, Background
from SpaceGame.gametypes.SpaceStations import stations_small, stations_big

from SpaceGame.gametypes.UFOs import DEFAULT_UFO_GEN_RANGES, UFO, UFOS, UFOGeneratorData

import random

from SpaceGame.gametypes.enemies.Bug import Bug


@dataclass
class SpaceJunkGeneratorRanges:
    num_stations_small: Tuple[int, int]
    num_stations_big: Tuple[int, int]

    # Range of velocity values in x and y directions
    stations_big_velocity: Tuple[float, float]
    stations_small_velocity: Tuple[float, float]

    stations_small_angular_velocity: Tuple[float, float]
    stations_big_angular_velocity: Tuple[float, float]


DEFAULT_SPACEJUNK_GEN_RANGES = SpaceJunkGeneratorRanges(
    num_stations_small=(5, 20),
    num_stations_big=(5, 15),
    stations_big_velocity=(-10, 10),
    stations_small_velocity=(-20, 20),
    stations_small_angular_velocity=(-2, 2),
    stations_big_angular_velocity=(-1, 1)
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
        self.generator = None
        self.main = game
        self.engine = game.physics_engine
        self.space = game.physics_engine.space
        self.background = background
        self.spacejunk: Optional[SpaceObject] = None
        self.ufos: Optional[SpaceObject] = None
        self.play_zone_width_height = dimension
        self.dimensions = self.calculate_dimensions_pixels()
        self.bg_sprite_list = []
        self.walls = []
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
        self.add_walls_to_pymunk_space()

    def setup_ufo(self):
        ufos = self.generator.generate_ufos()
        if ufos is not None:
            for ufo in ufos:
                self.ufos.append(ufo)

    def setup(self, background=True,
              boundry=True,
              spacejunk=True,
              ufo=True,
              bugs=True):
        self.generator = SpaceJunkGenerator(self.main, self)

        self.setup_spritelists()
        if background:
            self.tile_background()

        if boundry:
            self.setup_playzone_boundry()

        if spacejunk:
            self.generate_spacejunk()

        if ufo:
            self.setup_ufo()

        if bugs:
            self.setup_bugs()

    def setup_bugs(self):
        for i in range(0, 1):
            bug = Bug(self.main)
            bug.position = ((self.width / 2.0) + i * 5.0, (self.height / 2.0) + i * 5.0)
            bug.setup()
            bug.shape.sensor = False
            self.bugs.append(bug)


    def setup_spritelists(self):
        self.bg_sprite_list = arcade.SpriteList()
        self.spacejunk = arcade.SpriteList()
        self.ufos = arcade.SpriteList()
        self.bugs = arcade.SpriteList()

    def calculate_dimensions_pixels(self) -> Tuple[float, float]:
        return (self.play_zone_width_height[0] * self.background.width,
                self.play_zone_width_height[1] * self.background.height)

    def tile_background(self):
        for i in range(-2, self.play_zone_width_height[0] + 3):
            for j in range(-2, self.play_zone_width_height[1] + 3):
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

    def draw_ufos(self):
        self.ufos.draw()

    def draw_bugs(self):
        self.bugs.draw()

    def draw(self):
        self.draw_background()
        self.draw_walls()
        self.draw_spacejunk()
        self.draw_ufos()
        self.draw_bugs()

    def update(self):
        self.spacejunk.update()
        self.ufos.update()
        self.bugs.update()

    def reset(self):
        pass

    def generate_spacejunk(self):
        spacejunks = self.generator.generate_spacejunk()

        if spacejunks is not None:
            for junk in spacejunks:
                self.spacejunk.append(junk)


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
                 spacejunk_data=None,
                 ufo_data=None,
                 spacejunk_ranges=DEFAULT_SPACEJUNK_GEN_RANGES,
                 ufo_ranges=DEFAULT_UFO_GEN_RANGES):

        self.main = main
        self.playzone = playzone
        self.spacejunk_ranges = spacejunk_ranges
        self.ufo_ranges = ufo_ranges
        self.objects = []
        self.seed = seed

        if spacejunk_data:
            self.spacejunk_data = spacejunk_data
            self.ufo_data = ufo_data
        else:
            self.spacejunk_data = self.generateSpaceJunkData()

        if ufo_data:
            self.ufo_data = ufo_data
        else:
            self.ufo_data = self.generateUFOData()

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

    def random_angular_velocity(self, range):
        return random.randrange(range[0], range[1])

    def initalize_space_object(self, object, velocity_range, angular_velocity_range):
        object.position = self.random_position()
        object.setup()
        object.body.velocity = (self.random_velocity(velocity_range))
        object.body.angular_velocity = self.random_angular_velocity(angular_velocity_range)

    def select_n_rand_objs(self, dataObjects: [], n_objects: int) -> []:
        objects = []
        for i in range(0, n_objects):
            objects.append(random.choice(dataObjects))

        return objects

    def select_and_initalize_space_object(self,
                                          n_objects,
                                          Object,
                                          data_list,
                                          velocity_range,
                                          angular_velocity_range):
        selected_data = self.select_n_rand_objs(data_list, n_objects)
        objects = []
        for data in selected_data:
            object = Object(data, self.main)
            self.initalize_space_object(object,
                                        velocity_range,
                                        angular_velocity_range)
            objects.append(object)

        return objects

    def generate_stations_small(self):
        return self.select_and_initalize_space_object(self.spacejunk_data.num_stations_small,
                                                      SpaceObject,
                                                      stations_small,
                                                      self.spacejunk_ranges.stations_small_velocity,
                                                      self.spacejunk_ranges.stations_small_angular_velocity)

    def generate_stations_big(self):
        return self.select_and_initalize_space_object(self.spacejunk_data.num_stations_big,
                                                      SpaceObject,
                                                      stations_big,
                                                      self.spacejunk_ranges.stations_big_velocity,
                                                      self.spacejunk_ranges.stations_big_angular_velocity)

    def generate_spacejunk(self):
        small_stations = self.generate_stations_small()
        big_stations = self.generate_stations_big()
        return small_stations + big_stations

    def generate_ufos(self):
        ufo_objects = self.select_and_initalize_space_object(self.ufo_data.num_ufos,
                                                             UFO,
                                                             UFOS,
                                                             self.ufo_ranges.velocity,
                                                             self.ufo_ranges.angular_velocity)

        return ufo_objects

    def generateUFOData(self):
        return UFOGeneratorData(num_ufos=self.generate_int(self.ufo_ranges.num_ufos))

    def generateSpaceJunkData(self):
        return SpaceJunkGenerateData(num_stations_small=self.generate_int(self.spacejunk_ranges.num_stations_small),
                                     num_stations_big=self.generate_int(self.spacejunk_ranges.num_stations_big))

    def generate_int(self, range):
        return random.randint(range[0], range[1])

    def seed_seed(self):
        random.seed(self._seed)

    @property
    def seed(self) -> int:
        return self._seed

    @seed.setter
    def seed(self, seed='random'):
        if seed == 'random':
            self._seed = datetime.datetime.now().timestamp()
        else:
            self._seed = seed
