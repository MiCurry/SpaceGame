from typing import Optional

import arcade
from arcade.experimental.input import InputManager, Keys, ControllerAxes, ControllerButtons
import pyglet
from pyglet.input import Controller

from SpaceGame.settings import KEYBOARD, CONTROLLER


class ControllerManager(pyglet.input.ControllerManager):
    def on_connect(self, controller):
        print("Connected controller")

    def on_disconnect(self, controller):
        print("Disconnected Controller")


class InputManager:
    def __init__(self, input_type, action_handler):
        self.controller = None
        if input_type == CONTROLLER:
            manager = ControllerManager()
            self.controller = manager.get_controllers()[0]

        self.input_manager = arcade.experimental.input.InputManager(controller=self.controller,
                                                                    action_handlers=action_handler)
        self.add_actions_and_axis()

        if input_type == CONTROLLER:
            self.add_controller_inputs()
            self.controller: Optional[Controller] = None
        elif input_type == KEYBOARD:
            self.add_keyboard_inputs()

    def add_actions_and_axis(self):
        self.input_manager.new_action('shoot')
        self.input_manager.new_axis('up_down')
        self.input_manager.new_axis('left_right')
        self.input_manager.new_axis('rotate')
        self.input_manager.new_action('damping_up')
        self.input_manager.new_action('damping_down')

    def add_controller_inputs(self):
        self.input_manager.add_action_input('shoot', ControllerButtons.RIGHT_SHOULDER)
        self.input_manager.add_axis_input('up_down', ControllerAxes.LEFT_STICK_Y, scale=-1.0)
        self.input_manager.add_axis_input('left_right', ControllerAxes.LEFT_STICK_X, scale=1.0)
        self.input_manager.add_axis_input('rotate', ControllerAxes.RIGHT_STICK_X, scale=-1.0)
        self.input_manager.add_action_input('damping_up', ControllerButtons.BACK)

    def add_keyboard_inputs(self):
        self.input_manager.add_action_input('shoot', Keys.SPACE)
        self.input_manager.add_axis_input('up_down', Keys.W, scale=-1.0)
        self.input_manager.add_axis_input('up_down', Keys.S, scale=1.0)
        self.input_manager.add_axis_input('left_right', Keys.A, scale=-1.0)
        self.input_manager.add_axis_input('left_right', Keys.D, scale=1.0)
        self.input_manager.add_axis_input('rotate', Keys.LEFT, scale=1.0)
        self.input_manager.add_axis_input('rotate', Keys.RIGHT, scale=-1.0)
        self.input_manager.add_action_input('damping_down', Keys.COMMA)
        self.input_manager.add_action_input('damping_up', Keys.PERIOD)

    def on_update(self):
        self.input_manager.update()
