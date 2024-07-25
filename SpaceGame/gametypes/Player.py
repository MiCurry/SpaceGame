from typing import Tuple

import arcade

import pyglet.input
from arcade.experimental.input import ActionState
from pyglet import clock

from SpaceGame.controls import Controller
from SpaceGame.gametypes.InputManager import InputManager
from SpaceGame.gametypes.Ship import Ship
from SpaceGame.settings import MOVEMENT_SPEED, DEAD_ZONE_LEFT_STICK, DEAD_ZONE_RIGHT_STICK, SHIP_FRICTION, CONTROLLER, \
    KEYBOARD, \
    ROTATION_SPEED, KEYBOARD_THRUSTER_FORCE, KEYBOARD_ROTATION_FORCE, ALIVE
from SpaceGame.shared.timer import TimerManager

RESPAWN_TIMER = "respawn"


class Player(Ship):
    def __str__(self):
        return f"Player: {self.player_number} - {self.player_name}"

    def __init__(self, main, player_name,
                 start_position: Tuple,
                 player_number=0,
                 input_source=CONTROLLER,
                 ship_color='orange',
                 status=ALIVE,
                 lives=-1):

        self.player_name = player_name
        self.input_source = input_source
        self.controller = None
        self.player_number = player_number

        self.w_pressed = 0.0
        self.s_pressed = 0.0
        self.a_pressed = 0.0
        self.d_pressed = 0.0
        self.left_pressed = 0.0
        self.right_pressed = 0.0

        self.lives = lives

        super().__init__(ship_color,
                         main,
                         start_position,
                         status=status)

        self.timers = TimerManager()
        self.input_manager = InputManager(self.input_source, action_handler=self.on_action)

    def setup(self):
        super().setup()

    def apply_angle_damping(self):
        self.body.angular_velocity /= 1.05

    def on_update(self, delta_time: float):
        self.input_manager.on_update()
        super().update()

        if RESPAWN_TIMER in self.timers.get_elapsed():
            self.timers.clear_elapsed(RESPAWN_TIMER)
            self.respawn()

        if self.applied_rotational_vel == 0.0:
            self.apply_angle_damping()

        dx = self.input_manager.input_manager.axis('left_right') * MOVEMENT_SPEED
        dy = self.input_manager.input_manager.axis('up_down') * MOVEMENT_SPEED
        self.applied_rotational_vel = self.input_manager.input_manager.axis('rotate') * ROTATION_SPEED

        self.body.angular_velocity += self.applied_rotational_vel
        self.body.apply_force_at_world_point((dx, -dy), (self.center_x, self.center_y))

    def on_action(self, action: str, state: ActionState):
        if action == 'shoot' and state == ActionState.PRESSED:
            self.shoot()

    def explode(self):
        super().explode()

        if self.last_hit_buy == "UFO":
            self.main.scoreboard.add_ufo_death(self.player_number)
        else:
            self.main.scoreboard.add_kill(self.last_hit_buy, self)
            self.main.scoreboard.add_death(self.player_number)

        self.lives -= 1
        self.timers.add(RESPAWN_TIMER, 5)