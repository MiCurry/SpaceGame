import datetime
from typing import List, Optional

import logging
logger = logging.getLogger('space_game')

from SpaceGame.gametypes.Player import Player
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
    def __init__(self, players: List[Player], settings):
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
        self.player_info = players  # Store the player info passed in

    def setup(self):
        super().setup()

        logger.debug("Setting up spriteLists")
        self.setup_playzone()
        logger.debug("Setting up Players")
        self.setup_players()
        logger.debug("Setting up Player Cameras")
        self.setup_players_cameras()
        logger.debug("Setting up Split Screen")
        self.setup_splitscreen_sprite()
        logger.debug("Setting up Collision Handlers")
        self.setup_collision_handlers()
        logger.debug("Setting up Scoreboard")
        self.setup_scoreboard()

    def setup_scoreboard(self):
        self.scoreboard = PvPScoreboard('pvp',
                                     self.players_list,
                                     starting_lives=10,
                                     time=datetime.timedelta(minutes=1, seconds=10),
                                     )
        self.scoreboard.setup()
        self.score = self.scoreboard

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
        # Setup both players from the player_info list
        for i, player in enumerate(self.player_info):
            # Create updated ShipData with the correct settings
            shipData = ShipData(
                status=ALIVE,
                sprite=player._shipData.sprite,
                hitpoints=self.settings['SHIP_STARTING_HITPOINTS'],
                mass=self.settings['SHIP_MASS'],
                friction=self.settings['SHIP_FRICTION'],
                elasticity=self.settings['SHIP_ELASTICITY'],
                scaling=self.settings['SHIP_SCALING'],
                movement_speed=self.settings['MOVEMENT_SPEED'],
                rotation_speed=self.settings['ROTATION_SPEED']
            )

            # Update player attributes
            player.hitpoints = self.settings['SHIP_STARTING_HITPOINTS']
            player.max_hitpoints = self.settings['SHIP_STARTING_HITPOINTS']
            player.main = self
            player.data = shipData
            player.player_number = i  # Set player number based on order

            # Add player to the game
            position = (200, 200) if i == 0 else (300, 300)  # Different start positions for each player
            input_source = KEYBOARD if i == 0 else CONTROLLER  # First player keyboard, second controller
            
            self.add_player(player,
                          position,
                          input_source)

    def on_key_press(self, key: int, modifiers: int):
        super().on_key_press(key, modifiers)

        if key == arcade.key.O:
            logger.info("O key pressed - Ending Game")
            self.end_game()

    def end_game(self):
        logger.info("Game Over - Ending PvP Game")
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
        logger.debug("Resetting Game")
        self.players_list = []

        self.players = None
        logger.debug("Resetting sprite lists")
        self.setup_spritelists()
        logger.debug("Resetting Players")
        self.setup_players()
        logger.debug("Resetting Player Cameras")
        self.setup_players_cameras()
