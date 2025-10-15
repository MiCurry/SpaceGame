import arcade
import arcade.gui

from SpaceGame import settings
from SpaceGame.gamemodes.pvp import PvpGame
from SpaceGame.gamemodes.single_player import SinglePlayer
from SpaceGame.gamemodes.single_test_game import SinglePlayerTest
from SpaceGame.menus.buttons import BackButton, QuitToWindows, StartButton
from SpaceGame.settings import SettingsButton, SettingsManager

class GameSetupMenu(arcade.View):
    def __init__(self, back_view, start_view, settings : SettingsManager):
        super().__init__()
        self.back_view = back_view
        self.start_view = start_view
        self.settings = settings

        self.background_color = self.settings['BACKGROUND_COLOR']
        self.background = arcade.load_texture(self.settings['BACKGROUND_IMAGE'])

        arcade.set_background_color(self.background_color)

        self.ui = arcade.gui.UIManager()
        self.v_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=20)

        self.start_button = StartButton(self.start_view, self.settings)
        self.v_box.add(self.start_button)

        self.back_button = BackButton(self.back_view)
        self.v_box.add(self.back_button)

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

    def on_click_pvp(self, event: arcade.gui.UIOnClickEvent):
        game = PvpGame(settings=self.settings)
        game.setup()
        self.window.show_view(game)


class ContinuePlayButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, text="Unpause", width=200):
        super().__init__(text=text, width=width)


