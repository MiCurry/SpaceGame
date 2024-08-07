import os
from enum import Enum
from dataclasses import dataclass
import math
import random
from typing import Tuple

from SpaceGame.gametypes.Bullet import Bullet
from SpaceGame.gametypes.Explosion import ExplosionSize
from SpaceGame.gametypes.PlayZoneTypes import CollisionTypes, SpaceObject, SpaceObjectData

HEALTH = 5
MASS = 0.5
FRICTION = 0.0
ELASTICITY = 0.9
RADIUS = 1.0
SCALE = 1.0
SHOOT_DISTANCE = 625.0

UFO_BULLET_SPAWN_OFFSET = 100.0

SPRITE_FILE = ":sprites:/png/sprites/Ships/enemyBlack4.png"

ALIVE = True
DEAD = False


class Enemy(SpaceObject):
    def __init__(self, main):
        self.main = main
        self.status = ALIVE
        super().__init__(SpaceObjectData(SPRITE_FILE,
                                         HEALTH,
                                         MASS,
                                         FRICTION,
                                         ELASTICITY,
                                         RADIUS,
                                         CollisionTypes.UFO.value,
                                         SCALE),
                         main)
        self.gun_cooldown = 0
        self.range = SHOOT_DISTANCE
        self.cnt = 0
        self.gun_fired_normal = 300
        self.target_angle = 0
        self.hitpoints = 15

    def explode(self):
        self.remove_from_sprite_lists()
        self.main.add_explosion(self.position, ExplosionSize.BIG)

    def damage(self, damage: int):
        self.hitpoints -= damage

    def update(self):
        if self.hitpoints <= 0:
            self.explode()

        # First find a player to lock onto
        self.find_target()

        # Then decide to shoot at the target
        if self.decide_to_shoot():
            self.shoot()

        # Then move - if we deicde too
        if self.decide_to_move():
            self.move()

        self.gun_cooldown -= 1

    def find_angle_to_target(self, target):
        return math.atan2((target.center_y - self.center_y), (target.center_x - self.center_x)) - math.pi / 2

    def find_target(self):
        self.target, self.target_distance = self.main.find_nearest_sprite(self, self.main.players)

        if self.target_distance > self.range:
            self.target = None
        else:  # Only run find_angle if we have a target
            self.target_angle = self.find_angle_to_target(self.target)

    def target_in_range(self):
        return self.target and (self.target_distance < self.range)

    def decide_to_shoot(self):
        pass

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
                   self.type,
                   spawn_offset=BULLET_SPAWN_OFFSET)

    def move(self):
        pass