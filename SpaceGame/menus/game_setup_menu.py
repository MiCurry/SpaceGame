import datetime
from SpaceGame.gametypes.Player import Player, get_player_or_make_new_one
import arcade
import arcade.gui

from SpaceGame import settings
from SpaceGame.gamemodes.pvp import PvpGame
from SpaceGame.gamemodes.single_player import SinglePlayer
from SpaceGame.gamemodes.single_test_game import SinglePlayerTest
from SpaceGame.menus.Inputs import DEFAULT_FONT, ShipNameChoiceWidget, TextInput
from SpaceGame.menus.buttons import BackButton, QuitToWindows, StartButton
from SpaceGame.settings import SettingsButton, SettingsManager

class GameSetupMenu(arcade.gui.UIView):
    def __init__(self,
                 back_view, 
                 start_view,
                 settings : SettingsManager,
                 nrows=3,
                 ncols=2):
        super().__init__()

        self.nrows = nrows
        self.ncols = ncols
        self.back_view = back_view
        self.start_view = start_view
        self.settings = settings

        self.background_color = self.settings['BACKGROUND_COLOR']
        self.background = arcade.load_texture(self.settings['BACKGROUND_IMAGE'])

        arcade.set_background_color(self.background_color)

        self.start_button = StartButton(self.start_view, self.settings)
        self.back_button = BackButton(self.back_view)

        self.v_box = arcade.gui.UIBoxLayout(
            vertical=True,
            space_between=10
        )

        self.start_back_button_box = arcade.gui.UIBoxLayout(
            vertical=False,
            space_between=20
        ) 

        self.start_back_button_box.add(self.start_button)
        self.start_back_button_box.add(self.back_button)

        self.v_box.add(self.start_back_button_box, index=0)

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

class SinglePlayerSetup(GameSetupMenu):
    def __init__(self, back_view, start_view, settings : SettingsManager):
        super().__init__(back_view=back_view, start_view=start_view, settings=settings)

        self.start_button.on_click = self.on_start_click

        self.ship_choice = ShipNameChoiceWidget(names=['One', 'Two', 'Three'], settings=settings)

        self.v_box.add(self.ship_choice, 
                       index=0,
                      )

        self.settings_holder = arcade.gui.UIBoxLayout(vertical=False)

        self.time_input = TextInput('Time', "03:00", width=50,
                                    color=arcade.color.WHITE)
        
        self.time_input.text_input.on_change = self.on_time_change
        self.time : datetime.timedelta
        self.settings_holder.add(self.time_input)

        self.difficulty_slider_row = arcade.gui.UIBoxLayout(
            vertical=False,
            space_between=10
        )

        self.difficulty_slider = arcade.gui.UISlider(
            value=1,
            step=1,
            width=150,
            min_value=1,
            max_value=6,
        )

        self.difficulty_slider.on_change = self.on_slider_change

        self.difficulty_slider_label = arcade.gui.UILabel(
            f'Difficulty: {self.get_difficulty()}',
            font_name=DEFAULT_FONT,
            font_size=12
        )

        self.difficulty_slider_row.add(self.difficulty_slider_label)
        self.difficulty_slider_row.add(self.difficulty_slider)

        self.settings_holder.add(self.difficulty_slider_row)
        self.v_box.add(self.settings_holder, index=0)

    def get_difficulty(self):
        return int(self.difficulty_slider.value)

    def convert_time(self, time_str):
        time = datetime.datetime.strptime(time_str, "%M:%S").time()
        return datetime.timedelta(minutes=time.minute, seconds=time.second)

    def on_time_change(self, event : arcade.gui.UIOnChangeEvent):
        self.time = self.convert_time(event.new_value)
        self.settings['Time'] = self.time

    def on_slider_change(self, event : arcade.gui.UIOnChangeEvent):
        self.difficulty_slider_label.text = f'Difficulty: {self.get_difficulty()}'
        self.settings['Difficulty'] = self.get_difficulty()

    def on_start_click(self, event : arcade.gui.UIOnClickEvent):
        player : Player = get_player_or_make_new_one(self.ship_choice.name)
        player._shipData.sprite = self.ship_choice.selected_ship

        window = arcade.get_window()
        game = self.start_view(self.settings, player)
        game.setup()
        window.show_view(game)


class PvpSetupMenu(GameSetupMenu):
    def __init__(self, back_view, start_view, settings: SettingsManager):
        super().__init__(back_view=back_view, start_view=start_view, settings=settings)

        self.start_button.on_click = self.on_start_click

        # Create ship choice widgets for both players
        self.ship_choice_p1 = ShipNameChoiceWidget(names=['Player One', 'Red', 'Blue'], settings=settings)
        self.ship_choice_p2 = ShipNameChoiceWidget(names=['Player Two', 'Green', 'Yellow'], settings=settings)

        # Create a horizontal layout for the ship choices
        self.players_layout = arcade.gui.UIBoxLayout(vertical=False, space_between=60)
        self.players_layout.add(self.ship_choice_p1)
        self.players_layout.add(self.ship_choice_p2)

        # Add the players layout to the grid
        self.v_box.add(self.players_layout, index=0)

        # Create settings holder for match settings
        self.settings_holder = arcade.gui.UIBoxLayout(vertical=False,
                                                      space_between=10)

        # Time input
        self.time_input = TextInput('Match Time', "05:00", width=50,
                                    color=arcade.color.WHITE)
        self.time_input.text_input.on_change = self.on_time_change
        self.time: datetime.timedelta
        self.settings_holder.add(self.time_input)

        # Difficulty slider
        self.difficulty_slider_row = arcade.gui.UIBoxLayout(
            vertical=False,
            space_between=10
        )

        self.difficulty_slider = arcade.gui.UISlider(
            value=1,
            step=1,
            width=150,
            min_value=1,
            max_value=6,
        )

        self.difficulty_slider.on_change = self.on_slider_change

        self.difficulty_slider_label = arcade.gui.UILabel(
            f'Difficulty: {self.get_difficulty()}',
            font_name=DEFAULT_FONT,
            font_size=12
        )

        self.difficulty_slider_row.add(self.difficulty_slider_label)
        self.difficulty_slider_row.add(self.difficulty_slider)

        self.settings_holder.add(self.difficulty_slider_row)
        
        # Add settings holder to grid
        self.v_box.add(self.settings_holder, index=0)

    def convert_time(self, time_str):
        time = datetime.datetime.strptime(time_str, "%M:%S").time()
        return datetime.timedelta(minutes=time.minute, seconds=time.second)

    def on_time_change(self, event: arcade.gui.UIOnChangeEvent):
        self.time = self.convert_time(event.new_value)
        self.settings['Time'] = self.time

    def get_difficulty(self):
        return int(self.difficulty_slider.value)

    def on_slider_change(self, event: arcade.gui.UIOnChangeEvent):
        self.difficulty_slider_label.text = f'Difficulty: {self.get_difficulty()}'
        self.settings['Difficulty'] = self.get_difficulty()

    def on_start_click(self, event: arcade.gui.UIOnClickEvent):
        # Create players
        player1: Player = get_player_or_make_new_one(self.ship_choice_p1.name)
        player1._shipData.sprite = self.ship_choice_p1.selected_ship
        player1.input_source = settings.KEYBOARD

        player2: Player = get_player_or_make_new_one(self.ship_choice_p2.name)
        player2._shipData.sprite = self.ship_choice_p2.selected_ship
        player2.input_source = settings.CONTROLLER

        window = arcade.get_window()
        game = self.start_view([player1, player2], self.settings)
        game.setup()
        window.show_view(game)
