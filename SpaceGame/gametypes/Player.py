from typing import Tuple

import arcade

import pyglet.input

from SpaceGame.controls import Controller
from SpaceGame.gametypes.Ship import Ship
from SpaceGame.settings import MOVEMENT_SPEED, DEAD_ZONE_LEFT_STICK, DEAD_ZONE_RIGHT_STICK, SHIP_FRICTION, CONTROLLER, KEYBOARD, \
    ROTATION_SPEED, KEYBOARD_THRUSTER_FORCE, KEYBOARD_ROTATION_FORCE, ALIVE


class Player(Ship):
    def __str__(self):
        return f"Player: {self.player_number} - {self.player_name}"

    def __init__(self, main, player_name,
                 start_position: Tuple,
                 player_number=0,
                 input_source=CONTROLLER,
                 ship_color='orange'):
        self.player_name = player_name
        self.input_source = input_source
        self.controller = None
        self.player_number = player_number
        self.sprite_filename = None

        if ship_color == "orange":
            self.sprite_filename = "./resources/png/sprites/Ships/playerShip1_orange.png"
        elif ship_color == "blue":
            self.sprite_filename = "./resources/png/sprites/Ships/playerShip1_blue.png"
        else:
            self.sprite_filename = "./resources/png/sprites/Ships/playerShip1_orange.png"

        self.main = main
        self.dx = 0.0
        self.dy = 0.0
        self.force = 0.0
        self.applied_rotational_vel = 0
        self.body = None
        self.start_position = start_position
        self.friction = SHIP_FRICTION

        self.w_pressed = 0.0
        self.s_pressed = 0.0
        self.a_pressed = 0.0
        self.d_pressed = 0.0
        self.left_pressed = 0.0
        self.right_pressed = 0.0

        self.status = ALIVE

        super().__init__(self.sprite_filename, self.main)


    def setup(self):
        self.body = self.main.physics_engine.get_physics_object(self).body
        self.shape = self.main.physics_engine.get_physics_object(self).shape

        if self.input_source == CONTROLLER:
            controllers = pyglet.input.get_controllers()

            if len(controllers) > 0:
                self.controller = pyglet.input.get_controllers()[0]
                self.controller.push_handlers(self)
                self.controller.open()
                self.controller.rumble_play_strong()

    def apply_angle_damping(self):
        self.body.angular_velocity /= 1.05

    def on_update(self, delta_time: float):
        super().update()

        if self.input_source == CONTROLLER and self.controller:
            self.dx = Controller.apply_deadzone(self.controller.leftx,
                                                dead_zone=DEAD_ZONE_LEFT_STICK) * MOVEMENT_SPEED
            self.dy = Controller.apply_deadzone(-self.controller.lefty,
                                                dead_zone=DEAD_ZONE_LEFT_STICK) * MOVEMENT_SPEED
            self.applied_rotational_vel = Controller.apply_deadzone(-self.controller.rightx,
                                                                    dead_zone=DEAD_ZONE_RIGHT_STICK) * ROTATION_SPEED

        if self.input_source == KEYBOARD:
            self.dx = self.a_pressed + self.d_pressed
            self.dy = self.w_pressed + self.s_pressed
            self.applied_rotational_vel = self.left_pressed - self.right_pressed

        if self.applied_rotational_vel == 0.0:
            self.apply_angle_damping()

        self.body.angular_velocity += self.applied_rotational_vel
        self.body.apply_force_at_world_point((self.dx, -self.dy), (self.center_x, self.center_y))

    def on_button_press(self, joystick, button: int):
        if button == "rightshoulder":
            self.shoot()

    def on_key_press(self, key: int, modifiers: int):
        if self.input_source == KEYBOARD:
            if key == arcade.key.W:
                self.w_pressed = -KEYBOARD_THRUSTER_FORCE
            elif key == arcade.key.S:
                self.s_pressed = KEYBOARD_THRUSTER_FORCE
            elif key == arcade.key.A:
                self.a_pressed = -KEYBOARD_THRUSTER_FORCE
            elif key == arcade.key.D:
                self.d_pressed = KEYBOARD_THRUSTER_FORCE
            elif key == arcade.key.LEFT:
                self.left_pressed = KEYBOARD_ROTATION_FORCE
            elif key == arcade.key.RIGHT:
                self.right_pressed = KEYBOARD_ROTATION_FORCE

            if key == arcade.key.SPACE:
                self.shoot()

    def on_key_release(self, key: int, modifiers: int):
        if self.input_source == KEYBOARD:
            if key == arcade.key.W:
                self.w_pressed = 0.0
            elif key == arcade.key.S:
                self.s_pressed = 0.0
            elif key == arcade.key.A:
                self.a_pressed = 0.0
            elif key == arcade.key.D:
                self.d_pressed = 0.0
            elif key == arcade.key.LEFT:
                self.left_pressed = 0.0
            elif key == arcade.key.RIGHT:
                self.right_pressed = 0.0

    def reset(self):
        self.body.apply_force_at_world_point((0.0, 0.0), (self.center_x, self.center_y))
        self.dx = 0.0
        self.dy = 0.0
        self.body.velocity = (0.0, 0.0)
        self.body.position = (self.start_position)
        self.center_x = self.start_position[0]
        self.center_y = self.start_position[1]
        self.body.angular_velocity = 0.0
        self.applied_rotational_vel = 0
        if self.controller:
            self.controller.remove_handlers(self)
