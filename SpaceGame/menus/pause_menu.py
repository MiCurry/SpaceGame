import arcade
import arcade.gui

from SpaceGame import settings
from SpaceGame.menus.pause_button import QuitToWindows
from SpaceGame.settings import SettingsButton


class ContinuePlayButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, text="Unpause", width=200):
        super().__init__(text=text, width=width)


class PauseMenu(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        self.ui = arcade.gui.UIManager()
        self.v_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=20)

        unpause_button = ContinuePlayButton()
        unpause_button.on_click = self.on_click_unpause
        self.v_box.add(unpause_button)

        settings_button = SettingsButton()
        self.v_box.add(settings_button)

        quit_to_windows_button = QuitToWindows(text="Quit")
        self.v_box.add(quit_to_windows_button)

        ui_anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        ui_anchor_layout.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(ui_anchor_layout)

    def setup(self):
        pass

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.game_view.on_resize(width, height)

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear()

        self.game_view.on_draw()
        self.window.default_camera.use()
        self.ui.draw()

    def on_click_unpause(self, event: arcade.gui.UIOnClickEvent):
        self.unpause()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            self.unpause()

    def unpause(self):
        self.window.show_view(self.game_view)
