from SpaceGame.gametypes.PlayZoneTypes import SpaceObjectData, CollisionTypes

SPRITE_SCALE = 1.0

STATION_SPRITE_PATH = "resources/png/sprites/Station/"
HEALTH_SMALL = 15
MASS_SMALL = 2.0
ELASTICITY_SMALL = 0.9
RADIUS_SMALL = 1.0

HEALTH_BIG = 60
MASS_BIG = 8.0
ELASTICITY_BIG = 0.9
RADIUS_BIG = 0.9

stations = []
stations_small = []
stations_big = []

# Small - Sputnik

StationSputnik1 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_015.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticity=ELASTICITY_SMALL,
    radius=RADIUS_SMALL,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)
stations_small.append(StationSputnik1)

StationSputnik2 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_016.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticity=ELASTICITY_SMALL,
    radius=RADIUS_SMALL,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)
stations_small.append(StationSputnik2)

# Small - modern
StationSmall1 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_018.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticity=ELASTICITY_SMALL,
    radius=RADIUS_SMALL,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)
stations_small.append(StationSmall1)

StationSmall2 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_019.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticity=ELASTICITY_SMALL,
    radius=RADIUS_SMALL,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)
stations_small.append(StationSmall2)

StationSmall3 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_022.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticity=ELASTICITY_SMALL,
    radius=RADIUS_SMALL,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)
stations_small.append(StationSmall3)

StationSmall4 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_023.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticity=ELASTICITY_SMALL,
    radius=RADIUS_SMALL,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)
stations_small.append(StationSmall4)


# Big Space Stations
StationBig1 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_020.png",
    health=HEALTH_BIG,
    mass=MASS_BIG,
    friction=0.0,
    elasticity=ELASTICITY_BIG,
    radius=RADIUS_BIG,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)
stations_big.append(StationBig1)

StationBig2 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_021.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticity=ELASTICITY_BIG,
    radius=RADIUS_BIG,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)
stations_big.append(StationBig2)

StationBig3 = SpaceObjectData(
    spritefile=STATION_SPRITE_PATH + "spaceStation_024.png",
    health=HEALTH_SMALL,
    mass=MASS_SMALL,
    friction=0.0,
    elasticity=ELASTICITY_BIG,
    radius=RADIUS_BIG,
    type=CollisionTypes.SPACE_JUNK.value,
    scale=SPRITE_SCALE
)
stations_big.append(StationBig3)

for small in stations_small:
    stations.append(small)

for big in stations_big:
    stations.append(big)