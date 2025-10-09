import os.path

import arcade
from arcade.gui import (
    UIAnchorLayout,
    UIBoxLayout,
    UILabel,
    UIInputText,
    UIOnChangeEvent
)
import arcade.gui.widgets

from SpaceGame.gametypes.PlayZoneTypes import Background
from SpaceGame.menus.Inputs import TextInput
from SpaceGame.menus.buttons import BackButton

# Constants
PLAYER_ONE = 0
PLAYER_TWO = 1
ALIVE = True
DEAD = False
CONTROLLER = 'controller'
KEYBOARD = 'keyboard'

class SettingsButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, back_view, text="Settings", width=200):
        self.back_view = back_view
        super().__init__(text=text, width=width)

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        settings = SettingsMenu(self.back_view)
        window = arcade.get_window()
        window.show_view(settings)

class SettingsMenu(arcade.View):
    def __init__(self, back_view):
        super().__init__()
        self.back_view = back_view

        self.ui = arcade.gui.UIManager()
        self.v_box = UIBoxLayout(space_between=20)

        self.back_button = BackButton(self.back_view)
        self.v_box.add(self.back_button)

        ui_anchor_layout = UIAnchorLayout()
        ui_anchor_layout.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(ui_anchor_layout)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.game_view.on_resize(width, height)

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.back_view.on_draw()
        self.window.default_camera.use()
        self.ui.draw()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            self.back_button.on_click("foo")


class SettingsManager:
    def __init__(self):
        self.settings = {}

        self.add_setting('Title', 'Space Game')
        self.add_setting('SCREEN_WIDTH', 1400)
        self.add_setting('SCREEN_HEIGHT', 1400)
        self.add_setting('SCREEN_SPLIT_WIDTH', self.settings['SCREEN_WIDTH'] / 2.0)

        self.add_setting("PLAY_ZONE", (4,4))
        self.add_setting("BACKGROUND_COLOR", arcade.color.SPACE_CADET)
        self.add_setting("BACKGROUND_IMAGE", ":sprites:png/backgrounds/stars.png")
        self.add_setting("DEFAULT_BACKGROUND", Background(self.settings['BACKGROUND_IMAGE'],
                                                          1024,
                                                          1024,
                                                          1.0))
        self.add_setting("GRAVITY", 0.0)
        self.add_setting("DEFAULT_DAMPING", 1.0)

        self.add_setting("SHIP_STARTING_HITPOINTS", 10)
        self.add_setting("SHIP_SCALING", 0.5)
        self.add_setting("SHIP_MASS", 1.0)
        self.add_setting("SHIP_FRICTION", 1.0)
        self.add_setting("SHIP_ELASTICITY", 0.1)
        self.add_setting("SHIP_DAMPING", 1.0)
        self.add_setting("ROTATION_SPEED", 0.05)
        self.add_setting("KEYBOARD_THRUSTER_FORCE", 200.0)
        self.add_setting("KEYBOARD_ROTATION_FORCE", 0.05)
        self.add_setting("MOVEMENT_SPEED", 450.0)



        self.add_setting("CONTROLLER", 'controller')
        self.add_setting("KEYBOARD", 'keyboard')
        self.add_setting("DEAD_ZONE_LEFT_STICK", 0.05)
        self.add_setting("DEAD_ZONE_RIGHT_STICK", 0.1)

    def __getitem__(self, key):
        return self.settings[key]

    def __setitem__(self, key, value):
        self.settings[key] = value
    
    def add_setting(self, name,
                          default_value):
        self[name] = default_value
        
    def get_setting(self, name):
        return self[name]
