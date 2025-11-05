import logging
logger = logging.getLogger('space_game')

import os
import textwrap
from typing import List
import arcade

from arcade import uicolor
from arcade.gui import (
    UIDropdown,
    UIOnChangeEvent,
    UIBoxLayout,
    UIInputText,
    UILabel,
    UITextEvent,
    UITextArea,
    UIFlatButton,
    UILayout,
    UIMessageBox,
    UIManager,
    UIImage
)
import arcade.gui.widgets
import arcade.gui.widgets.buttons

from arcade.gui.events import UIOnActionEvent, UIOnClickEvent
from arcade.gui.mixins import UIMouseFilterMixin
from arcade.gui.nine_patch import NinePatchTexture
from arcade.gui.widgets.buttons import UIFlatButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from arcade.gui.widgets.text import UILabel, UITextArea

DEFAULT_FONT = ("Kenney Future", "arial")

class TextInput(UIBoxLayout):
    def __init__(self, label_text, default_text_value, 
                 width=300,
                 height=20,
                 color=arcade.color.BLACK,
                 **kwargs):
        super().__init__(vertical=False, space_between=10)

        self.label = UILabel(label_text,
                             font_name=DEFAULT_FONT,
                             font_size=12,
                             text_color=color)

        self.add(self.label)

        self.text_input = UIInputText(
            width=width,
            height=height,
            font_name=DEFAULT_FONT,
            font_size=12,
            border_color=arcade.color.WHITE,
            border_width=2,
            text=default_text_value,
            text_color=color
        )

        self.add(self.text_input)

    def text(self):
        return self.text_input.text

class NewPlayerPopUp(UIMessageBox):
    def __init__(self, parent):
        super().__init__(
            width=500,
            height=250,
            title="New Player",
            buttons=("Add", 'Cancel'),
            message_text=textwrap.dedent(
                "Enter Your Name"
            )
        )

        self._parent = parent
        self.name_input = TextInput(label_text='Name:', default_text_value='')
        self.add(self.name_input)

    def on_action(self, event: UIOnActionEvent):
        if event.action == 'Add':
            # Add New Player name
            self._parent.add_new_name(self.name_input.text())
            logging.debug(f"New player added with name: {self.name_input.text()}")

        return super().on_action(event)
    
class AddNewPlayerButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, parent):
        self._parent = parent
        super().__init__(text='+', width=20, height=30)

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.get_ui_manager().add(NewPlayerPopUp(self), layer=UIManager.OVERLAY_LAYER)

    def add_new_name(self, name):
        self._parent.add_new_name(name)


SHIP_RES_PATH = ':sprites:png/sprites/Ships/'

SHIPS = [
    'playerShip1_blue.png',
    'playerShip1_green.png',
    'playerShip1_orange.png',
    'playerShip1_red.png',
    'playerShip2_blue.png',
    'playerShip2_green.png',
    'playerShip2_orange.png',
    'playerShip2_red.png',
    'playerShip3_blue.png',
    'playerShip3_green.png',
    'playerShip3_orange.png',
]

class ShipNameChoiceWidget(UIBoxLayout):
    def __init__(self, names : List[str], settings, height=50, width=50, **kwargs):
        super().__init__(vertical=True, space_between=10, kwargs=kwargs)

        self.ship_selc_index = 0

        self.settings = settings

        self.name_selection = UIBoxLayout(vertical=False,
                                          space_between=5)

        self.name_dropdown : UIDropdown
        self.name_dropdown : UIDropdown = UIDropdown(
            default='Select User   v',
            options=names,
            primary_style=UIFlatButton.STYLE_BLUE
        )

        self.name_dropdown.push_handlers(on_change=self.on_name_change)

        self.new_player_button = AddNewPlayerButton(self)

        self.name_selection.add(self.name_dropdown)
        self.name_selection.add(self.new_player_button)

        self.cur_selected_ship = arcade.load_texture(os.path.join(SHIP_RES_PATH, SHIPS[self.ship_selc_index]))

        self.ship_image = UIImage(texture=self.cur_selected_ship,
                                  width=height, height=width)

        self.ship_selection = UIBoxLayout(vertical=False,
                                          space_between=105)
        self.prev_ship_button = UIFlatButton(text="<",
                                             width=35,
                                             height=35,
                                             )
        self.prev_ship_button.on_click = self.prev_ship

        self.next_ship_button = UIFlatButton(text=">",
                                             width=35,
                                             height=35,
                                             )
        self.next_ship_button.on_click = self.next_ship

        self.ship_selection.add(self.prev_ship_button)
        self.ship_selection.add(self.next_ship_button)

        self.add(self.name_selection)
        self.add(self.ship_image)
        self.add(self.ship_selection)

    @property
    def ship(self) -> str:
        return SHIPS[self.ship_selc_index]
    
    @property
    def name(self) -> str:
        return self.name_dropdown.value

    def next_ship(self, event):
        logging.debug(f"Next ship button clicked. Current index: {self.ship_selc_index}")
        if self.ship_selc_index == len(SHIPS) - 1:
            self.ship_selc_index = 0
        else:
            self.ship_selc_index += 1

        self.ship_image.texture = arcade.load_texture(os.path.join(
            SHIP_RES_PATH,
            SHIPS[self.ship_selc_index]
        ))

    def prev_ship(self, event):
        logging.debug(f"Previous ship button clicked. Current index: {self.ship_selc_index}")   
        if self.ship_selc_index == 0:
            self.ship_selc_index = len(SHIPS) - 1
        else:
            self.ship_selc_index -= 1

        self.ship_image.texture = arcade.load_texture(os.path.join(
            SHIP_RES_PATH,
            SHIPS[self.ship_selc_index]
        ))

    @property
    def selected_ship(self):
        return os.path.join(SHIP_RES_PATH, SHIPS[self.ship_selc_index])

    def add_new_name(self, name):
        self.name_dropdown._options.append(name)
        self.name_dropdown.value = name

    def on_name_change(self, event):
        logging.debug(f"Name changed to: {self.name}")
