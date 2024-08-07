import arcade
import arcade.gui

from SpaceGame import settings
from SpaceGame.gamemodes.pvp import PvpGame
from SpaceGame.gamemodes.single_player import SinglePlayer
from SpaceGame.gamemodes.single_test_game import SinglePlayerTest
from SpaceGame.menus.buttons import QuitToWindows
from SpaceGame.settings import SettingsButton


class PvpMenuButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, text="Head to Head", width=200):
        super().__init__(text=text, width=width)

class SinglePlayerButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, text="Single Player", width=200):
        super().__init__(text=text, width=width)

    def on_click(self, event):
        window = arcade.get_window()
        sp = SinglePlayer()
        sp.setup()
        window.show_view(sp)

class TestPlayerButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, text="Test Arena", width=200):
        super().__init__(text=text, width=width)

    def on_click(self, event):
        window = arcade.get_window()
        ta = SinglePlayerTest()
        ta.setup()
        window.show_view(ta)

class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = settings.BACKGROUND_COLOR
        self.background = arcade.load_texture(settings.BACKGROUND_IMAGE)
        arcade.set_background_color(self.background_color)

        self.ui = arcade.gui.UIManager()
        self.v_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=20)

        pvp_button = PvpMenuButton()
        pvp_button.on_click = self.on_click_pvp
        self.v_box.add(pvp_button)

        single_player_button = SinglePlayerButton()
        self.v_box.add(single_player_button)

        test_area_buttons = TestPlayerButton()
        self.v_box.add(test_area_buttons)

        settings_button = SettingsButton(self)
        self.v_box.add(settings_button)

        quit_to_windows_button = QuitToWindows(text="Quit")
        self.v_box.add(quit_to_windows_button)

        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(ui_anchor_layout)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)

    def on_show_view(self):
        self.background_color = settings.BACKGROUND_COLOR
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.window.width,
                                            self.window.height,
                                            self.background)

        if self.ui.is_enabled():
            self.ui.draw()

    def on_click_pvp(self, event: arcade.gui.UIOnClickEvent):
        game = PvpGame()
        game.setup()
        self.window.show_view(game)


class ContinuePlayButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, text="Unpause", width=200):
        super().__init__(text=text, width=width)


