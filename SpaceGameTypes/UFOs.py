from enum import Enum
from dataclasses import dataclass
import math
import random
from typing import Tuple

import arcade 

from SpaceGameTypes.SpaceGameTypes import CollisionTypes
from SpaceGameTypes.PlayZoneTypes import SpaceObject, SpaceObjectData
from SpaceGameTypes.Bullet import Bullet

UFO_HEALTH = 5
UFO_MASS = 0.5
UFO_FRICTION = 0.0
UFO_ELASTICITY = 0.9
UFO_RADIUS = 1.0
UFO_SCALE = 1.0
UFO_SHOOT_DISTANCE = 625.0

UFO_BULLET_SPAWN_OFFSET = 100.0


class UFOColor(Enum):
    BLUE = "ufoBlue.png"
    GREEN = "ufoGreen.png"
    RED = "ufoRed.png"
    YELLOW = "ufoYellow.png"

@dataclass
class UFOData():
    color: str
    aggression: int
    intelligence: int    
    lazer: str = "laserRed16.png"

@dataclass
class UFOGeneratorRanges:
    num_ufos: Tuple[int, int]
    agression: Tuple[int, int]
    intelligence: Tuple[int, int]
    velocity: Tuple[int, int]
    angular_velocity: Tuple[int, int]

@dataclass
class UFOGeneratorData:
    num_ufos: int

DEFAULT_UFO_GEN_RANGES = UFOGeneratorRanges(num_ufos=[1,1],
                                            agression=[1,1],
                                            intelligence=[1,1],
                                            velocity=[-10,10],
                                            angular_velocity=[-1,1])

RED_UFO = UFOData(UFOColor.RED.value,
                  aggression=1,
                  intelligence=1)

BLUE_UFO = UFOData(UFOColor.BLUE.value,
                   aggression=1,
                   intelligence=1)

GREEN_UFO = UFOData(UFOColor.GREEN.value,
                    aggression=1,
                    intelligence=1)

YELLOW_UFO = UFOData(UFOColor.YELLOW.value,
                    aggression=1,
                    intelligence=1)

UFOS = [RED_UFO, BLUE_UFO, GREEN_UFO, YELLOW_UFO]

def random_name():
    return random.choice(["Bill",
                          "Bob",
                          "Steve"])

ALIVE = True
DEAD = False

class UFO(SpaceObject):
    def __init__(self, props: UFOData, main):
        self.props = props
        self.main = main
        self.status = ALIVE
        super().__init__(SpaceObjectData(":sprites:png/sprites/Ships/" + self.color,
                                         UFO_HEALTH,
                                         UFO_MASS,
                                         UFO_FRICTION,
                                         UFO_ELASTICITY,
                                         UFO_RADIUS,
                                         CollisionTypes.SPACE_JUNK.value,
                                         UFO_SCALE), 
                        main)
        self.gun_cooldown = 0
        self.range = UFO_SHOOT_DISTANCE
        self.name = random_name()
        self.cnt = 0
        self.gun_fired_normal = 75
        self.target_angle = 0

    def print_diag(self):
        print(f"{self.name} ({self.position}) - Locked onto: '{self.target}' - {self.target_distance} - {self.target_angle}")

    def update(self):
        # First find a player to lock onto
        self.find_target()

        # Then decide to shoot at the target
        if self.decide_to_shoot():
            self.shoot()

        # Then move - if we deicde too
        if self.decide_to_move():
            self.move()

        self.gun_cooldown -= 1

      # Uncomment for UFO Diag
      #  if self.cnt == 30:
      #      self.print_diag()
      #      self.cnt = 0
      #  else:
      #      self.cnt += 1


    def find_angle_to_target(self, target):
        return math.atan2((target.center_y - self.center_y), (target.center_x - self.center_x)) - math.pi/2
        
    def find_target(self):
        self.target, self.target_distance = self.main.find_nearest_sprite(self, self.main.players)
        
        if self.target_distance > self.range:
            self.target = None
        else: # Only run find_angle if we have a target
            self.target_angle = self.find_angle_to_target(self.target)


    def target_in_range(self):
        return self.target and (self.target_distance < self.range)

    def gun_cooleddown(self):
        if self.gun_cooldown <= 0:
            return True
        return False

    def decide_to_shoot(self):
        if self.target_in_range() and self.gun_cooleddown():
            return True
        return False

    def decide_to_move(self):
        pass

    def shoot(self):
        self.gun_cooldown = self.gun_fired_normal

        if self.status is ALIVE:
            Bullet(self.main,
                (self.center_x, self.center_y),
                self.target_angle,
                self.body.velocity[0],
                self.body.velocity[1],
                "UFO",
                spawn_offset=UFO_BULLET_SPAWN_OFFSET)


    def move(self):
        pass


    @property
    def color(self):
        return self.props.color

    @property
    def agression(self):
        return self.props.agression

    @property
    def intelligence(self):
        return self.props.intelligence

    @property
    def lazer(self):
        return self.props.lazer


def UFOGenerator():
    pass