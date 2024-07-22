import arcade
from arcade.types import Color

import SpaceGame.menus.main_menu
from SpaceGame.menus.buttons import QuitToMainMenu, QuitToWindows
from SpaceGame.scoreboard.scoreboard import Scoreboard
from SpaceGame.settings import SettingsButton


class GameOverMenu(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.background = None
        self.game_view = game_view
        self.main = self.game_view

        self.get_player_scores()

        self.create_ui_elements()
        self.add_menu_background()

        self.add_game_over_text(font_size=25)
        self.add_winner_text(self.create_winner_text(), font_size=20)

        self.add_score_text()

        self.generate_ui()

    def add_score_text(self):
        player_one_kills = self.main.score.kills[0]
        player_one_deaths = self.main.score.deaths[0]
        player_one_ufo_deaths = self.main.score.ufo_deaths[0]

        player_two_kills = self.main.score.kills[1]
        player_two_deaths = self.main.score.deaths[1]
        player_two_ufo_deaths = self.main.score.ufo_deaths[1]

        player_1_scores_text = self.generate_score_text(player_one_kills, player_one_deaths, player_one_ufo_deaths)
        player_2_scores_text = self.generate_score_text(player_two_kills, player_two_deaths, player_two_ufo_deaths)

        self.v_box.add(arcade.gui.widgets.text.UILabel(
            text="Player One",
            font_size=16
        ))
        self.v_box.add(player_1_scores_text['kills'])
        self.v_box.add(player_1_scores_text['deaths'])
        self.v_box.add(player_1_scores_text['ufo_deaths'])

        self.v_box.add(arcade.gui.widgets.text.UILabel(
            text="Player Two",
            font_size=16
        ))
        self.v_box.add(player_2_scores_text['kills'])
        self.v_box.add(player_2_scores_text['deaths'])
        self.v_box.add(player_2_scores_text['ufo_deaths'])


    def generate_score_text(self, kills, deaths, ufo_deaths, font_size=12):
        score_text = {}
        score_text['kills'] = arcade.gui.widgets.text.UILabel(
            text=f"Kills: {kills}",
            font_size=font_size
        )
        score_text['deaths'] = arcade.gui.widgets.text.UILabel(
            text=f"Deaths: {deaths}",
            font_size=font_size
        )
        score_text['ufo_deaths'] = arcade.gui.widgets.text.UILabel(
            text=f"UFO Deaths: {ufo_deaths}",
            font_size=font_size
        )
        return score_text



    def generate_ui(self):
        anchor_layout = arcade.gui.widgets.layout.UIAnchorLayout()
        anchor_layout.add(self.v_box,
                          anchor_x='center',
                          anchor_y='center')
        self.ui.add(anchor_layout)

    def create_ui_elements(self, space_between=20):
        self.ui = arcade.gui.UIManager()
        self.v_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=20)

    def add_menu_background(self, color=Color(145, 163, 176, 127)):
        self.background = arcade.gui.UIWidget(width=self.window.width,
                                              height=self.window.height)
        self.background.with_background(color=color)
        self.ui.add(self.background)

    def add_game_over_text(self, text='GAME OVER', font_size=25):
        game_over_big_text = arcade.gui.widgets.text.UILabel(
            text=text,
            font_size=font_size,
        )
        self.v_box.add(game_over_big_text)

    def add_winner_text(self, text, font_size=25):
        winner = arcade.gui.widgets.text.UILabel(
            text=text,
            font_size=font_size,
        )
        self.v_box.add(winner)

    def get_player_scores(self):
        self.player_one_score = self.game_view.scoreboard.get_player_score(0)
        self.player_two_score = self.game_view.scoreboard.get_player_score(1)

    def create_winner_text(self):
        winner_text = ""

        if self.player_one_score == self.player_two_score:
            winner_text = "TIE!"
        elif self.player_one_score > self.player_two_score:
            winner_text = "Player one wins!"
        elif self.player_two_score > self.player_one_score:
            winner_text = "Player two wins!"

        return winner_text

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.game_view.on_resize(width, height)
        self.background.resize(width=width, height=height)

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        self.window.default_camera.use()
        self.ui.draw()
