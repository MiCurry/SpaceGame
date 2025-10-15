import arcade
import arcade.gui

from SpaceGame import settings
from SpaceGame.gamemodes.pvp import PvpGame
from SpaceGame.gamemodes.single_player import SinglePlayer
from SpaceGame.gamemodes.single_test_game import SinglePlayerTest
from SpaceGame.menus.buttons import QuitToWindows
from SpaceGame.menus.game_setup_menu import GameSetupMenu
from SpaceGame.settings import SettingsButton, SettingsManager


class PvpMenuButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, back_view, text="Head to Head", width=200):
        self.back_view = back_view
        super().__init__(text=text, width=width)

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        setup_menu = GameSetupMenu(self.back_view, PvpGame, self.back_view.settings)
        window = arcade.get_window()
        window.show_view(setup_menu)

class SinglePlayerButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, back_view, text="Single Player", width=200):
        self.back_view = back_view
        super().__init__(text=text, width=width)

    def on_click(self, event):
        setup_menu = GameSetupMenu(self.back_view, SinglePlayer, self.back_view.settings)
        window = arcade.get_window()
        window.show_view(setup_menu)

class TestPlayerButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, back_view, text="Test Arena", width=200):
        self.back_view = back_view
        super().__init__(text=text, width=width)

    def on_click(self, event):
        window = arcade.get_window()
        setup_menu = GameSetupMenu(self.back_view, SinglePlayerTest, self.back_view.settings)
        window.show_view(setup_menu)

class MainMenu(arcade.View):
    def __init__(self, settings : SettingsManager):
        super().__init__()
        self.settings = settings
        self.background_color = self.settings['BACKGROUND_COLOR']
        self.background = arcade.load_texture(self.settings['BACKGROUND_IMAGE'])
        arcade.set_background_color(self.background_color)

        self.ui = arcade.gui.UIManager()
        self.v_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=20)

        pvp_button = PvpMenuButton(self)
        self.v_box.add(pvp_button)

        single_player_button = SinglePlayerButton(self)
        self.v_box.add(single_player_button)

        test_area_buttons = TestPlayerButton(self)
        self.v_box.add(test_area_buttons)

        settings_button = SettingsButton(self, self.settings)
        self.v_box.add(settings_button)

        quit_to_windows_button = QuitToWindows(text="Quit")
        self.v_box.add(quit_to_windows_button)

        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(ui_anchor_layout)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)

    def on_show_view(self):
        self.background_color = self.settings['BACKGROUND_COLOR']
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, self.window.width, self.window.height)
        )

        if self.ui._enabled:
            self.ui.draw()



class ContinuePlayButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, text="Unpause", width=200):
        super().__init__(text=text, width=width)


