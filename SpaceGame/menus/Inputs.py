import arcade

from arcade.gui import (
    UIOnChangeEvent,
    UIBoxLayout,
    UIInputText,
    UILabel,
    UITextEvent
)
import arcade.gui.widgets


DEFAULT_FONT = ("Kenney Future", "arial")

class TextInput(UIBoxLayout):
    def __init__(self, label_text, default_text_value, **kwargs):
        super().__init__(vertical=False,
                         size_hint=(1, 0.1))

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

    def text(self):
        return self.text_input.text

