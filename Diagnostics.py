from typing import Callable, Dict
import arcade

class DiagnosticsController():
    def __init__(self, game):
        self.game = game
        self.START_HEIGHT_OFFSET = 20
        self.HEIGHT_OFFSET = 20
        self.WIDTH_OFFSET = 20
        self.num_active = 0
        self.diags = []
        self.active_diags = []

    def add_diagnostic(self, 
                        key : int,
                        output_message : Callable,
                        display_at_start : bool,
                        text_color=arcade.color.WHITE):

        diag = {'key' : key,
                'output' : output_message,
                'text_color' : text_color,
                'display' : display_at_start}
        self.diags.append(diag)
        if display_at_start:
            self.active_diags.append(diag)

    def on_key_press(self, key: int, modifiers: int):
        for diag in self.diags:
            if key == diag['key'] and diag in self.active_diags:
                self.active_diags.remove(diag)
            elif key == diag['key'] and diag not in self.active_diags:
                self.active_diags.append(diag)

    def get_offset(self, display_number: int):
        return (display_number + 1) * self.HEIGHT_OFFSET

    def on_draw(self):
        for display_number, diag in enumerate(self.active_diags):
            self.display_diagnostics(diag, display_number)

    def display_diagnostics(self, diag: Dict, display_number: int):
        arcade.draw_text(diag['output'](self.game),
                         self.WIDTH_OFFSET, 
                         (self.game.height - self.START_HEIGHT_OFFSET) - self.get_offset(display_number),
                         diag['text_color'])