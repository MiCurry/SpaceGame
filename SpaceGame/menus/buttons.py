import arcade
import arcade.gui

""" Buttons that are to be reused """
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
        window = arcade.get_window()
        window.show_view(self.back_view)


class QuitToWindows(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, text="Quit To Windows", width=200):
        super().__init__(text=text, width=width)

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class QuitToMainMenu(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, main_menu_view, text="Quit to Main Menu", width=200):
        self.main_menu_view = main_menu_view
        super().__init__(text=text, width=width)

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.get_window().show_view(self.main_menu_view)
