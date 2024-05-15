import arcade
from pathlib import Path
from PlayZone import Background, PlayZone, SpaceJunkGenerator, SpaceJunkGenerateData, SpaceJunkGeneratorRanges

class Body:
    def apply_force_at_world_point(self, velocity, point):
        pass

class PhysicsObject:
    def __init__(self):
        self.body = Body()

class PhysicsEngine:
    def __init__(self):
        self.space = {}
        self.object = PhysicsObject()

    def get_physics_object(self, object):
        return self.object

class MainMock:
    def __init__(self):
        self.physics_engine = PhysicsEngine()

    def add_sprite_to_pymunk(self, object):
        pass

# Left, Right, Width, Height
PLAY_ZONE = (4, 4)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BACKGROUND_IMAGE = "resources/png/backgrounds/stars.png"
DEFAULT_BACKGROUND = Background(BACKGROUND_IMAGE,
                                1024,
                                1024,
                                1.0)

main = MainMock()
playzone = PlayZone(main, DEFAULT_BACKGROUND, PLAY_ZONE)

generator = SpaceJunkGenerator(main, playzone)
assert type(generator.seed) == float

generator = SpaceJunkGenerator(main, playzone, seed=42)
assert generator.seed == 42

# Default data -> Ranges will be default, but not used
data = SpaceJunkGenerateData(4, 5)
generator = SpaceJunkGenerator(main, playzone, data=data, seed=42)

assert generator.spacejunk_data.num_stations_big == data.num_stations_big
assert generator.spacejunk_data.num_stations_small == data.num_stations_small

assert generator.ranges.num_stations_small == (15, 30)
assert generator.ranges.num_stations_big == (1, 3)

assert generator.spacejunk_data.num_stations_big == 4
assert generator.spacejunk_data.num_stations_small == 5


# Custom ranges
ranges = SpaceJunkGeneratorRanges(num_stations_small=(3, 10),
                                  num_stations_big=(10, 20),
                                  stations_big_velocity=(-3, 3),
                                  stations_small_velocity=(-10, 10))
generator = SpaceJunkGenerator(main, playzone, ranges=ranges, seed=30)

assert generator.seed == 30

assert generator.ranges.num_stations_small == ranges.num_stations_small
assert generator.ranges.num_stations_big == ranges.num_stations_big

assert generator.spacejunk_data.num_stations_big >= generator.ranges.num_stations_big[0]
assert generator.spacejunk_data.num_stations_big <= generator.ranges.num_stations_big[1]

assert generator.spacejunk_data.num_stations_small >= generator.ranges.num_stations_small[0]
assert generator.spacejunk_data.num_stations_small <= generator.ranges.num_stations_small[1]

generator = SpaceJunkGenerator(main, playzone, ranges=ranges, seed=30)

generator.generate_objects()