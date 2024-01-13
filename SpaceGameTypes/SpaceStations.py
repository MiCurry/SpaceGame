from SpaceGameTypes.SpaceGameTypes import CollisionTypes
from SpaceGameTypes.PlayZoneTypes import SpaceObjectData


SPRITE_SCALE = 1.0

STATION_SPRITE_PATH = ":sprites:png/sprites/Station/"
HEALTH_SMALL = 15
MASS_SMALL = 2.0
ELASTICITY_SMALL = 0.9
RADIUS_SMALL = 1.0

HEALTH_BIG = 60
MASS_BIG = 8.0
ELASTICITY_BIG = 0.9
RADIUS_BIG = 0.9

# Small - Sputnik

StationSputnik1 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_015.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticit=ELASTICITY_SMALL,
    radius=RADIUS_SMALL,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)

StationSputnik2 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_016.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticit=ELASTICITY_SMALL,
    radius=RADIUS_SMALL,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)

# Small - modern

StationSmall1 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_018.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticit=ELASTICITY_SMALL,
    radius=RADIUS_SMALL,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)

StationSmall2 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_019.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticit=ELASTICITY_SMALL,
    radius=RADIUS_SMALL,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)

StationSmall3 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_022.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticit=ELASTICITY_SMALL,
    radius=RADIUS_SMALL,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)

StationSmall4 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_023.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticit=ELASTICITY_SMALL,
    radius=RADIUS_SMALL,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)


# Big Space Stations

StationBig1 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_020.png",
    health=HEALTH_BIG,
    mass=MASS_BIG,
    friction=0.0,
    elasticit=ELASTICITY_BIG,
    radius=RADIUS_BIG,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)

StationBig2 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_021.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticit=ELASTICITY_BIG,
    radius=RADIUS_BIG,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)

StationBig3 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_024.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticit=ELASTICITY_BIG,
    radius=RADIUS_BIG,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)
