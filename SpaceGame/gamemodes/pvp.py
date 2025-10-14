from typing import Optional

import arcade

from SpaceGame.gametypes.Ship import ShipData
import SpaceGame.menus.game_over_view
from SpaceGame.gamemodes.basegame import BaseGame
from SpaceGame.PlayZone import PlayZone
from SpaceGame.scoreboard.scoreboard import PvPScoreboard, Scoreboard
from SpaceGame.settings import ALIVE, PLAYER_ONE, PLAYER_TWO, CONTROLLER, KEYBOARD, DEAD
from SpaceGame.gametypes.PlayZoneTypes import CollisionTypes
from SpaceGame.shared.physics import ship_bullet_hit_handler, spaceObject_bullet_hit_handler, bullet_ufo_hit_handler
from SpaceGame.shared.timer import TimerManager

SPAWNED = 0
RESPAWNING = 1

MINUTES = 60 # Seconds

class PvpGame(BaseGame):
    def __init__(self, settings):
        super().__init__(settings)
        self.score = None
        self.cameras = []
        self.play_zone: Optional[PlayZone] = None
        self.player_one_projection_data = None
        self.player_one_viewport = None
        self.player_two_projection_data = None
        self.player_two_viewport = None
        self.scoreboard = None
        self.respawning_players = {}
        self.timers = TimerManager()

    def setup(self):
        super().setup()
        self.setup_playzone()
        self.setup_players()
        self.setup_players_cameras()
        self.setup_splitscreen_sprite()
        self.setup_collision_handlers()
        self.setup_scoreboard()

    def setup_scoreboard(self):
        self.scoreboard = PvPScoreboard('pvp',
                                     self.players_list,
                                     starting_lives=10,
                                     time=.25 * MINUTES,
                                     )
        self.scoreboard.setup()
        self.score = self.scoreboard

    def setup_playzone(self):
        self.play_zone = PlayZone(self,
                                  self.settings['DEFAULT_BACKGROUND'],
                                  self.settings['PLAY_ZONE'])
        self.play_zone.setup(background=True,
                             boundry=True,
                             spacejunk=True,
                             ufo=True
                            )

    def setup_players(self, players=-1):
        if players == -1:
            self.setup_player_one()
            self.setup_player_two()
        elif players == 0:
            self.setup_player_one()
        elif players == 1:
            self.setup_player_two()

    def setup_player_one(self):

        player_data = ShipData(status=ALIVE,
                               hitpoints=self.settings['SHIP_STARTING_HITPOINTS'],
                               mass = self.settings['SHIP_MASS'],
                               friction = self.settings['SHIP_FRICTION'],
                               elasticity = self.settings['SHIP_ELASTICITY'],
                               scaling = self.settings['SHIP_SCALING'],
                               movement_speed = self.settings['MOVEMENT_SPEED'],
                               rotation_speed = self.settings['ROTATION_SPEED']
                               )
        self.add_player("Player One",
                        PLAYER_ONE,
                        (199, 200),
                        KEYBOARD,
                        "orange",
                        player_data)

    def setup_player_two(self):

        player_data = ShipData(status=ALIVE,
                               hitpoints=self.settings['SHIP_STARTING_HITPOINTS'],
                               mass = self.settings['SHIP_MASS'],
                               friction = self.settings['SHIP_FRICTION'],
                               elasticity = self.settings['SHIP_ELASTICITY'],
                               scaling = self.settings['SHIP_SCALING'],
                               movement_speed = self.settings['MOVEMENT_SPEED'],
                               rotation_speed = self.settings['ROTATION_SPEED']
                               )
        self.add_player("Player Two",
                        PLAYER_TWO,
                        (300, 300),
                        CONTROLLER,
                        "blue",
                        player_data)

    def on_key_press(self, key: int, modifiers: int):
        super().on_key_press(key, modifiers)

        if key == arcade.key.O:
            self.end_game()

    def end_game(self):
        self.scoreboard.game_over()
        game_over = SpaceGame.menus.game_over_view.PvPGameOverMenu(self, settings=self.settings)
        self.window.show_view(game_over)

        for player in self.players_list:
            if player.input_source == CONTROLLER:
                player.input_manager.input_manager.unbind_controller()

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        if self.scoreboard.timer_elapsed():
            self.end_game()

        for player in range(len(self.players)):
            if self.players[player].status != DEAD:
                self.center_camera_on_player(player)

        self.scoreboard.on_update(delta_time)

    def on_hide_view(self):
        pass

    def on_draw(self):
        for player in range(len(self.players_list)):
            self.cameras[player].use()
            self.clear()
            self.play_zone.draw()
            self.players.draw()
            self.players_list[player].draw()
            self.healthBars.draw()
            self.bullets.draw()
            self.explosions.draw()
            self.scoreboard.on_draw()

        self.default_camera.use()
        self.divider.draw()

    def reset(self):
        self.players_list = []

        self.players = None
        self.setup_spritelists()
        self.setup_players()
        self.setup_players_cameras()
