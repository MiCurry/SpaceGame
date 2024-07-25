import os.path

import arcade
import arcade.gui
from SpaceGame.gametypes.PlayZoneTypes import Background
from SpaceGame.menus.buttons import BackButton

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
        self.v_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=20)

        self.back_button = BackButton(self.back_view)
        self.v_box.add(self.back_button)

        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
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
        pass

# Window settings
TITLE = "Space Game"
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000
SCREEN_SPLIT_WIDTH = SCREEN_WIDTH / 2.0

# Play Zone Settings
PLAY_ZONE = (4, 4)
BACKGROUND_COLOR = arcade.color.SPACE_CADET
BACKGROUND_IMAGE = ":sprites:png/backgrounds/stars.png"
DEFAULT_BACKGROUND = Background(BACKGROUND_IMAGE,
                                1024,
                                1024,
                                1.0)

# Physics settings
GRAVITY = 0.0
DEFAULT_DAMPING = 1.0

# Ship Physics and properties
SHIP_STARTING_HITPOINTS = 5
SHIP_SCALING = 0.5
SHIP_MASS = 1.0
SHIP_FRICTION = 0.0
SHIP_ELASTICITY = 0.1
SHIP_DAMPING = 1.0

# Player settings
PLAYER_ONE = 0
PLAYER_TWO = 1
ALIVE = True
DEAD = False

# Ship controls settings
CONTROLLER = 'controller'
KEYBOARD = 'keyboard'
ROTATION_SPEED = 0.05
KEYBOARD_THRUSTER_FORCE = 200.0
KEYBOARD_ROTATION_FORCE = 0.05
MOVEMENT_SPEED = 450.0
DEAD_ZONE_LEFT_STICK = 0.05
DEAD_ZONE_RIGHT_STICK = 0.1
