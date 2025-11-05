import logging
logger = logging.getLogger('space_game')

import arcade
import arcade.gui
import arcade.gui.widgets
import arcade.gui.widgets.buttons

import SpaceGame.menus.main_menu

""" Buttons that are to be reused """

class StartButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, start_view: arcade.View, settings, text="Start", width=200):
        super().__init__(text=text, width=width)
        self.start_view : arcade.View = start_view
        self.settings = settings

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        logger.debug("Start Button Clicked")
        window = arcade.get_window()
        game = self.start_view(self.settings)
        game.setup()
        window.show_view(game)

class BackButton(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, back_view: arcade.View, text="Back", width=200):
        super().__init__(text=text, width=width)
        if not isinstance(back_view, arcade.View):
            raise TypeError(
                f"BackButton() takes an arcade.View,"
                f"but it got a {type(back_view)}."
            )

        self.back_view = back_view

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        logger.debug("Back Button Clicked")
        window = arcade.get_window()
        window.show_view(self.back_view)


class QuitToWindows(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, text="Quit To Windows", width=200):
        super().__init__(text=text, width=width)

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        logger.debug("Quit to Windows Button Clicked")
        arcade.exit()


class QuitToMainMenu(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, settings, text="Quit to Main Menu", width=200):
        self.settings = settings
        super().__init__(text=text, width=width)

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        logger.debug("Quit to Main Menu Button Clicked")
        arcade.get_window().show_view(SpaceGame.menus.main_menu.MainMenu(self.settings))
