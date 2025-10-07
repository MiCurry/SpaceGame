from typing import Optional

import SpaceGame
from SpaceGame.PlayZone import PlayZone
from typing import Optional

import arcade

from SpaceGame.gamemodes.basegame import BaseGame
from SpaceGame.PlayZone import PlayZone
from SpaceGame.scoreboard.scoreboard import Scoreboard, SinglePlayerScoreboard
from SpaceGame.settings import PLAY_ZONE, DEFAULT_BACKGROUND, PLAYER_ONE, \
    PLAYER_TWO, \
    DEFAULT_DAMPING, CONTROLLER, KEYBOARD, DEAD
from SpaceGame.gametypes.PlayZoneTypes import CollisionTypes
from SpaceGame.shared.physics import ship_bullet_hit_handler, spaceObject_bullet_hit_handler

MINUTES = 60

class SinglePlayer(BaseGame):
    def __init__(self):
        super().__init__()
        self.cameras = []
        self.play_zone: Optional[PlayZone] = None
        self.player_one_projection_data = None
        self.player_one_viewport = None
        self.player_two_projection_data = None
        self.player_two_viewport = None

    def setup(self):
        super().setup()
        self.setup_playzone()
        self.setup_players()
        self.setup_players_cameras()
        self.setup_collision_handlers()
        self.setup_scoreboard()

    def setup_scoreboard(self):
        self.scoreboard = SinglePlayerScoreboard('Single Player',
                                     self.players,
                                     starting_lives=10,
                                     time=2 * MINUTES)
        self.scoreboard.setup()

    def setup_physics_engine(self):
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING,
                                                         gravity=(0, 0))

    def setup_playzone(self):
        self.play_zone = PlayZone(self, DEFAULT_BACKGROUND, PLAY_ZONE)
        self.play_zone.setup(background=True,
                             boundry=True,
                             spacejunk=True,
                             ufo=True
                            )

    def setup_players(self):
        self.add_player("Player One",
                        PLAYER_ONE,
                        (200, 200),
                        KEYBOARD,
                        "orange")

    def end_game(self):
        self.scoreboard.game_over()
        game_over = SpaceGame.menus.game_over_view.GameOverMenu(self)
        self.window.show_view(game_over)

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        for player in range(len(self.players)):
            if self.players[player].status != DEAD:
                self.center_camera_on_player(player)

        if self.scoreboard.timer_elapsed():
            self.scoreboard.end_game()

        self.scoreboard.on_update(delta_time)
        

    def on_hide_view(self):
        pass

    def on_draw(self):
        for player in range(len(self.players)):
            self.cameras[player].use()
            self.clear()
            self.play_zone.draw()
            self.players_list[player].draw()
            self.players.draw()
            self.healthBars.draw()
            self.bullets.draw()
            self.explosions.draw()

        self.scoreboard.on_draw()

    def reset(self):
        for player in self.players:
            player.reset()
            self.physics_engine.remove_sprite(player)

        while len(self.players) != 0:
            self.players.pop()

        self.players = None
        self.setup_spritelists()
        self.setup_players()
        self.setup_players_cameras()