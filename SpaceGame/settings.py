import os.path
from typing import List

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
from SpaceGame.menus.Inputs import DEFAULT_FONT, TextInput
from SpaceGame.menus.buttons import BackButton

# Constants
PLAYER_ONE = 0
PLAYER_TWO = 1
ALIVE = True
DEAD = False
CONTROLLER = 'controller'
KEYBOARD = 'keyboard'


class Setting:
    def __init__(self, name, default_value, label=None, vtype=None, show_in_menu=None):
        self.name = name
        if label is not None:
            self.label = label
        else:
            self.label = name

        self.handles = []
        self.default = default_value
        self.value = default_value
        self.changed = False

        if vtype is not None:
            self.vtype = vtype
        else:
            self.vtype = type(default_value)

        self.show_in_menu = show_in_menu

    def generate_input_item(self):
        self.input = SettingsInput(self, self.label, str(self.value))
        return self.input

    def register_handle(self, handle):
        self.handles.append(handle)

    def call_handles(self):
        for handle in self.handles:
            handle(self)

    def set(self, value):
        self.value = value
        self.call_handles()

    def get(self):
        return self.value


class SettingsInput(UIBoxLayout):
    def __init__(self, setting, label_text, default_text_value, **kwargs):
        super().__init__(vertical=False, size_hint=(1, 0.1))

        self.setting = setting

        self.label = UILabel(label_text,
                             font_name=DEFAULT_FONT,
                             font_size=24)

        self.add(self.label)

        self.text_input = UIInputText(
            width=400,
            height=30,
            font_name=DEFAULT_FONT,
            font_size=24,
            border_color=arcade.color.BLACK,
            border_width=2,
            text=default_text_value
        )

        self.add(self.text_input)

    # Read the setting from the input
    def read(self):
        return self.setting.vtype(self.text_input.text)


class SettingsManager:
    def __init__(self):
        self.settings = {}

        self.add_setting('Title', 'Space Game')
        self.add_setting('SCREEN_WIDTH', 1400,
                         label='Screen Width',
                         show_in_menu=True)
        self.add_setting('SCREEN_HEIGHT', 1400,
                         label='Screen Height', 
                         show_in_menu=True)
        self.add_setting('SCREEN_SPLIT_WIDTH',
                         self.settings['SCREEN_WIDTH'].value / 2.0,
                         'Split Screen Width')

        self.add_setting("PLAY_ZONE", (4,4),
                         label='Play Zone Size',
                         show_in_menu=False)

        self.add_setting("BACKGROUND_COLOR",
                         arcade.color.SPACE_CADET,
                         show_in_menu=False)

        self.add_setting("BACKGROUND_IMAGE",
                         ":sprites:png/backgrounds/stars.png",
                         show_in_menu=False)
        self.add_setting("DEFAULT_BACKGROUND", 
                         Background(self.settings['BACKGROUND_IMAGE'],
                                    1024,
                                    1024,
                                    1.0),
                                    show_in_menu=False)

        self.add_setting("GRAVITY_X",
                         0.0,
                         label='Gravity X',
                         show_in_menu=True)
        self.add_setting("GRAVITY_Y",
                         0.0, label='Gravity Y', show_in_menu=True)
        self.add_setting("DEFAULT_DAMPING", 1.0, label='Physics Damping', show_in_menu=True)
        self.add_setting("SHIP_STARTING_HITPOINTS", 10, label='Ship Max Hitpoints', show_in_menu=True)
        self.add_setting("SHIP_SCALING", 0.5, label="Ship Scaling", show_in_menu=False)
        self.add_setting("SHIP_MASS", 1.0, label='Ship Mass', show_in_menu=True)
        self.add_setting("SHIP_FRICTION", 1.0, label='Ship Friction', show_in_menu=True)
        self.add_setting("SHIP_ELASTICITY", 0.1, 'Ship Elasticity', show_in_menu=True)
        self.add_setting("SHIP_DAMPING", 1.0, 'Ship Physics Damping', show_in_menu=True)
        self.add_setting("ROTATION_SPEED", 0.05, 'Ship Rotation Speed', show_in_menu=True)
        self.add_setting("MOVEMENT_SPEED", 450.0, 'Movement Speed', show_in_menu=True)

        self.add_setting("CONTROLLER", 'controller')
        self.add_setting("KEYBOARD", 'keyboard')
        self.add_setting("DEAD_ZONE_LEFT_STICK", 0.05)
        self.add_setting("DEAD_ZONE_RIGHT_STICK", 0.1)

    def __getitem__(self, key):
        return self.settings[key].value

    def __setitem__(self, key, value):
        self.settings[key].value = value

    def get(self, name : str) -> Setting:
        return self.settings[name]
    
    def add_setting(self, name,
                          default_value,
                          label=None,
                          type=None,
                          show_in_menu=False):
        self.settings[name] = Setting(name, label=label, default_value=default_value, show_in_menu=show_in_menu)

    def generate_settings_inputs(self, box_layout : UIBoxLayout) -> List[SettingsInput]:
        settings_to_show : List[SettingsInput] = []
        for setting in self.settings.values():
            setting : Setting
            if not setting.show_in_menu:
                continue

            setting.generate_input_item()
            box_layout.add(setting.input)
            settings_to_show.append(setting.input)

        return settings_to_show
        
    def get_setting(self, name):
        return self[name]


class SettingsButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, back_view, settings : SettingsManager, text="Settings", width=200):
        self.settings = settings
        self.back_view = back_view
        super().__init__(text=text, width=width)

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        settings = SettingsMenu(self.back_view, settings=self.settings)
        window = arcade.get_window()
        window.show_view(settings)


class SettingsMenu(arcade.View):
    def __init__(self, back_view, settings : SettingsManager):
        super().__init__()
        self.back_view = back_view
        self.settings = settings

        self.ui = arcade.gui.UIManager()
        self.v_box = UIBoxLayout(space_between=20)

        self.setting_inputs = self.settings.generate_settings_inputs(self.v_box)

        self.back_button = BackButton(self.back_view)
        self.v_box.add(self.back_button)

        ui_anchor_layout = UIAnchorLayout()
        ui_anchor_layout.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(ui_anchor_layout)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.game_view.on_resize(width, height)

    def apply(self):
        for setting_input in self.setting_inputs:
            setting_input : SettingsInput
            setting = self.settings.get(setting_input.setting.name)

            self.settings.get(setting_input.setting.name).set(setting_input.read())

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.apply()

        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.back_view.on_draw()
        self.window.default_camera.use()
        self.ui.draw()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            self.back_button.on_click("foo")

