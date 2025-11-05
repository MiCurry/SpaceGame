import sys
from typing import Optional

import pymunk

import SpaceGame
from SpaceGame.PlayZone import PlayZone
from typing import Optional

from SpaceGame.gametypes.Player import Player
import arcade

from SpaceGame.gamemodes.basegame import BaseGame
from SpaceGame.PlayZone import PlayZone
from SpaceGame.gametypes.Ship import ShipData
from SpaceGame.scoreboard.scoreboard import Scoreboard, SinglePlayerScoreboard
from SpaceGame.settings import ALIVE, PLAYER_ONE, PLAYER_TWO, CONTROLLER, KEYBOARD, DEAD
from SpaceGame.gametypes.PlayZoneTypes import CollisionTypes
from SpaceGame.shared.physics import ship_bullet_hit_handler, spaceObject_bullet_hit_handler

MINUTES = 60

class SinglePlayer(BaseGame):
    def __init__(self, settings, players):
        super().__init__(settings)
        self.cameras = []
        self.play_zone: Optional[PlayZone] = None
        self.player_one_projection_data = None
        self.player_one_viewport = None
        self.player_two_projection_data = None
        self.player_two_viewport = None

        self.player_info = players

        self.time = self.settings['Time']

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
                                     time=self.time)
        self.scoreboard.setup()

    def setup_playzone(self):
        self.play_zone = PlayZone(self, 
                                  self.settings,
                                  self.settings['DEFAULT_BACKGROUND'],
                                  self.settings['PLAY_ZONE'])
        self.play_zone.setup(background=True,
                             boundry=True,
                             spacejunk=True,
                             ufo=True
                            )

    def setup_players(self):
        shipData = ShipData(status=ALIVE,
                            sprite=self.player_info._shipData.sprite,
                            hitpoints=self.settings['SHIP_STARTING_HITPOINTS'],
                            mass = self.settings['SHIP_MASS'],
                            friction = self.settings['SHIP_FRICTION'],
                            elasticity = self.settings['SHIP_ELASTICITY'],
                            scaling = self.settings['SHIP_SCALING'],
                            movement_speed = self.settings['MOVEMENT_SPEED'],
                            rotation_speed = self.settings['ROTATION_SPEED']
                        )

        player : Player = self.player_info

        player.hitpoints = self.settings['SHIP_STARTING_HITPOINTS']
        player.max_hitpoints = self.settings['SHIP_STARTING_HITPOINTS']

        player.main = self
        player.data = shipData
        player.player_number = 0

        self.add_player(player,
                        pymunk.Vec2d(200, 200),
                        KEYBOARD,
                        )

    def end_game(self):
        self.scoreboard.game_over()
        game_over = SpaceGame.menus.game_over_view.GameOverMenu(self, self.settings)
        self.window.show_view(game_over)

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        for player in range(len(self.players)):
            if self.players[player].status != DEAD:
                self.center_camera_on_player(player)

        if self.scoreboard.timer_elapsed():
            self.end_game()

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