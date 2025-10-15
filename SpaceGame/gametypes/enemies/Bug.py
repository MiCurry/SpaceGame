import os
import sys
from enum import Enum
from dataclasses import dataclass
import math
import random
from typing import Tuple
import numpy as np

from SpaceGame.gametypes.Bullet import Bullet
from SpaceGame.gametypes.Explosion import ExplosionSize
from SpaceGame.gametypes.PlayZoneTypes import CollisionTypes, SpaceObject, SpaceObjectData
from SpaceGame.shared.LQR import Lqr
from SpaceGame.shared.PID import Pid, PidData, PidInput
from SpaceGame.shared.timer import TimerManager

HEALTH = 5
MASS = 0.5
FRICTION = 0.0
ELASTICITY = 0.9
RADIUS = 1.0
SCALE = 0.40
SHOOT_DISTANCE = 625.0

UFO_BULLET_SPAWN_OFFSET = 100.0

SPRITE_FILE = ":sprites:/png/sprites/Ships/enemyBlack4.png"

ALIVE = True
DEAD = False

BUG_SCORE = 10


class Bug(SpaceObject):
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
                                         SCALE,
                                         BUG_SCORE),
                         main)
        self.gun_cooldown = 0
        self.range = SHOOT_DISTANCE
        self.cnt = 0
        self.gun_fired_normal = 300
        self.target_angle = 0
        self.hitpoints = 15
        self.bug_dis = 10
        self.pid_input = PidInput(kp=0.5,
                                  ki=0.00002,
                                  kd=75.0,
                                  tau=0.0,
                                  lim_min=-200,
                                  lim_max=200,
                                  lim_min_init=0.0,
                                  lim_max_init=5.0,
                                  )
        pid_debug = False
        self.x_pid = Pid(self.pid_input, debug=pid_debug)
        self.y_pid = Pid(self.pid_input, debug=pid_debug)
        self.timers = TimerManager()
        self.dx = 0
        self.dy = 0

        self.timers.add('pid', .01, restart=True)

    def print_diag(self):
        print(
            f"{self.name} ({self.position}) - Locked onto: '{self.target}' - {self.target_distance} - {self.target_angle}")

    def explode(self):
        self.remove_from_sprite_lists()
        self.main.add_explosion(self.position, ExplosionSize.BIG)
        self.main.scoreboard.add_score(self.last_hit_by, self.score)

    def damage(self, bullet: Bullet):
        self.hitpoints -= bullet.damage
        self.last_hit_by = bullet.creator

    def update(self, delta_t):
        if self.hitpoints <= 0:
            self.explode()
        nearest_bug, dis, angle, x_y_dist = self.find_nearest_sprite(self.main.players, 10000000)
        if nearest_bug and dis > self.bug_dis:
            self.move_towards(nearest_bug, x_y_dist, 1)

    def move_towards(self, target, xy_dist, dt):
        x_dist = xy_dist[0]
        y_dist = xy_dist[1]

        self.dx = self.x_pid.update(100, x_dist, dt)
        self.dy = self.y_pid.update(100, y_dist, dt)

        self.body.apply_force_at_world_point((self.dx, self.dy), (self.center_x, self.center_y))

    def find_angle_to_target(self, target):
        return math.atan2((target.center_y - self.center_y), (target.center_x - self.center_x)) - math.pi / 2

    def find_nearest_sprite(self, target_sprites, range):
        target, target_distance, x_y_dist = self.main.find_nearest_sprite(self, target_sprites)

        if target_distance > range:
            target = None
            target_angle = None
        else:  # Only run find_angle if we have a target
            target_angle = self.find_angle_to_target(target)

        return target, target_distance, target_angle, x_y_dist

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
