from dataclasses import dataclass

import logging
logger = logging.getLogger('space_game')

import datetime
from typing import List

import arcade

PLAYER_KILL_SCORE = 100

@dataclass
class Score:
    kills: int
    score: int
    deaths: int
    space_junk_blown_up : int
    ufo_deaths: int
    ufo_kills: int
    shots_fired : int
    shots_hit : int
    accuracy : float
    kd : float
    distance_flown : int
    highest_speed : int

@dataclass
class TotalPlayerStats:
    total_score : int
    highest_score : int
    total_space_junk_blown_up : int 
    highest_space_junk_blown_up : int 
    highest_kills : int
    highest_deaths : int
    kills : int
    deaths : int
    kd_ratio : int
    ufo_deaths : int
    ufo_kills : int
    shots_fired : int
    shots_hit : int
    accuracy : float
    distance_traveled : int

class Scoreboard:
    def __init__(self, time : datetime.timedelta, players, starting_lives=None):
        self.time = time
        self.total_time = time
        self.players = players
        self.stat_texts : List[arcade.Text] = []
        
        self.game_over_flag = False

        self.draw_timer_flag = True
        self.draw_score_flag = True

        self.score = []
        self.kills = []
        self.deaths = []
        self.lives = []
        self.ufo_deaths = []

    def setup(self):
        self.setup_timer()
        self.init_player_lives()
        self.init_kills()
        self.init_deaths()
        self.init_ufo_deaths()
        self.init_score_text()
        self.init_score()
        self.draw_timer_flag = True
        self.draw_score_flag = True

    def init_score(self):
        for player in self.players:
            self.score.append(0)

    def init_kills(self):
        for player in self.players:
            self.kills.append(0)

    def init_deaths(self):
        for player in self.players:
            self.deaths.append(0)

    def init_ufo_deaths(self):
        for player in self.players:
            self.ufo_deaths.append(0)

    def init_player_lives(self):
        for player in self.players:
            self.lives.append(0)

    def add_kill(self, killer, killed):
        logger.info(f"'{killer}' killed '{killed}'")
        self.kills[killer.player_number] += 1
        self.add_score(killer, PLAYER_KILL_SCORE)
        self.add_death(killed.player_number)

    def add_death(self, player):
        logger.info(f"Player {player} died.")
        self.deaths[player] += 1

    def add_ufo_death(self, player):
        logger.info(f"Player {player} was destroyed by a UFO.")
        self.ufo_deaths[player] += 1

    def add_score(self, player, amount):
        self.score[player.player_number] += amount

    def sub_life(self, player):
        self.lives[player] -= 1

    def draw_timer(self):
        camera = arcade.get_window().current_camera
        vp = camera.viewport
        self.timer_text.x = camera.position[0]
        self.timer_text.y = camera.position[1] - (vp[3] / 2) + vp[3] - 100
        self.timer_text.draw()

    def draw_score(self):
        camera = arcade.get_window().current_camera
        vp = camera.viewport
        self.score_text.x = camera.position[0]
        self.score_text.y = camera.position[1] - (vp[3] / 2) + vp[3] - 150
        self.score_text.draw()

    def on_draw(self):
        if self.draw_timer_flag:
            self.draw_timer()

        if self.draw_score_flag:
            self.draw_score()

    def timer_elapsed(self):
        if self.total_time <= datetime.timedelta(days=0, minutes=0, seconds=0):
            return True

    def setup_timer(self):
        window = arcade.get_window()
        self.timer_text = arcade.Text(
            text="00:00:00",
            x=window.width // 2,
            y=window.height // 2 - 50,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )
        minutes = (self.total_time.seconds % 3600) // 60
        seconds = self.total_time.seconds % 60
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}"

    def update_timer(self, delta_time):
        self.total_time -= datetime.timedelta(seconds=delta_time)

        if self.total_time <= datetime.timedelta(minutes=0, seconds=0):
            self.timer_elapsed()

        minutes = int(self.total_time.seconds) // 60
        seconds = int(self.total_time.seconds) % 60
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}"

    def update_score(self):
        self.score_text.text = f"{self.kills[self.players[0].player_number]} to {self.kills[self.players[1].player_number]}"

    def on_update(self, delta_time):
        self.update_timer(delta_time)
        self.update_score()

    def game_over(self, draw_pvp_score=False, draw_pvp_timer=False):
        self.game_over_flag = True
        self.draw_score_flag = draw_pvp_score
        self.draw_timer_flag = draw_pvp_timer

    def get_player_score(self, player_number):
        return self.score[player_number]

class PvPScoreboard(Scoreboard):
    def __init__(self, mode, players, time=None, starting_lives=6):
        self.game_mode = mode

        super().__init__(
            time,
            players
        )

    def init_score_text(self):
        window = arcade.get_window()
        self.score_text = arcade.Text(
            text="0 to 0",
            x=window.width // 2,
            y=window.height // 2 - 50,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )

    def update_score(self):
        self.score_text.text = f"{self.score[self.players[0].player_number]} to {self.score[self.players[1].player_number]}"


class SinglePlayerScoreboard(Scoreboard):
    def __init__(self, mode, players, time : datetime.timedelta, starting_lives=5):
        super().__init__(
            time,
            players
        )

    def init_score_text(self):
        window = arcade.get_window()
        self.score_text = arcade.Text(
            text="Score: ",
            x=window.width // 2,
            y=window.height // 2 - 50,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )

    def update_score(self):
        self.score_text.text = f"Score: {self.score[self.players[0].player_number]}"
