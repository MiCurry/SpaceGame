import arcade

from SpaceGame import settings


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = settings.BACKGROUND_COLOR
        self.background = arcade.load_texture(settings.BACKGROUND_IMAGE)
        arcade.set_background_color(self.background_color)

    def setup(self):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_show_view(self):
        self.background_color = settings.BACKGROUND_COLOR
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.window.width,
                                            self.window.height,
                                            self.background)

        arcade.draw_text("Space Game",
                         self.window.width / 2, self.window.height / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")