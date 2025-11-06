import arcade

import SpaceGame.menus.main_menu
from SpaceGame.menus.buttons import QuitToMainMenu, QuitToWindows
from SpaceGame.settings import SettingsButton, SettingsManager


class PauseMenu(arcade.View):
    def __init__(self, game_view, settings : SettingsManager):
        super().__init__()
        self.game_view = game_view
        self.settings = settings

        self.ui = arcade.gui.UIManager()
        self.v_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=20)

        unpause_button = SpaceGame.menus.main_menu.ContinuePlayButton()
        unpause_button.on_click = self.on_click_unpause
        self.v_box.add(unpause_button)

        settings_button = SettingsButton(self, self.settings)
        self.v_box.add(settings_button)

        quit_to_windows_button = QuitToMainMenu(self.settings, game_view=self.game_view)
        self.v_box.add(quit_to_windows_button)

        quit_to_windows_button = QuitToWindows(text="Quit", game_view=self.game_view)
        self.v_box.add(quit_to_windows_button)

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
        self.game_view.on_draw()
        self.window.default_camera.use()
        if self.ui._enabled:
            self.ui.draw()

    def on_click_unpause(self, event: arcade.gui.UIOnClickEvent):
        self.unpause()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            self.unpause()

    def unpause(self):
        self.window.show_view(self.game_view)

    def on_exit_to_main_menu_click(self, event: arcade.gui.UIOnClickEvent):
        logger.debug("Saving players before exiting to main menu")
        self.game_view.save_players()
        arcade.get_window().show_view(MainMenu())
