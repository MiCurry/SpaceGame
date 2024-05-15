import arcade
import arcade.gui

class QuitToWindows(arcade.gui.widgets.buttons.UIFlatButton):
    def __init__(self, text="Quit To Windows", width=200):
        super().__init__(text=text, width=width)

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()