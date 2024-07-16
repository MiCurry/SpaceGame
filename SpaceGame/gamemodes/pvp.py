from typing import Optional

import arcade

from SpaceGame.gamemodes.basegame import BaseGame
from SpaceGame.PlayZone import PlayZone
from SpaceGame.scoreboard.scoreboard import Scoreboard
from SpaceGame.settings import PLAY_ZONE, DEFAULT_BACKGROUND, PLAYER_ONE, \
    PLAYER_TWO, \
    DEFAULT_DAMPING, CONTROLLER, KEYBOARD, DEAD
from SpaceGame.gametypes.PlayZoneTypes import CollisionTypes
from SpaceGame.shared.physics import ship_bullet_hit_handler, spaceObject_bullet_hit_handler
from SpaceGame.shared.timer import TimerManager

SPAWNED = 0
RESPAWNING = 1

class PvpGame(BaseGame):
    def __init__(self):
        super().__init__()
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
        self.setup_collision_handlers()
        self.setup_scoreboard()

    def setup_scoreboard(self):
        self.scoreboard = Scoreboard('pvp',
                                     self.players_list,
                                     starting_lives=10,
                                     time=60 * .5,
                                     )
        self.scoreboard.setup()

    def setup_collision_handlers(self):
        data = {'window': self}

        self.physics_engine.add_collision_handler(CollisionTypes.BULLET.value,
                                                  CollisionTypes.SHIP.value,
                                                  post_handler=ship_bullet_hit_handler,
                                                  collision_data=data)
        self.physics_engine.add_collision_handler(CollisionTypes.BULLET.value,
                                                  CollisionTypes.SPACE_JUNK.value,
                                                  post_handler=spaceObject_bullet_hit_handler,
                                                  collision_data=data)

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

    def setup_players(self, players=-1):

        if players == -1:
            self.setup_player_one()
            self.setup_player_two()
        elif players == 0:
            self.setup_player_one()
        elif players == 1:
            self.setup_player_two()

    def setup_player_one(self):
        self.add_player("Player One",
                        PLAYER_ONE,
                        (199, 200),
                        KEYBOARD,
                        "orange")

    def setup_player_two(self):
        self.add_player("Player Two",
                        PLAYER_TWO,
                        #(self.play_zone.width - 100.0, self.play_zone.height - 100.0),
                        (300, 300),
                        CONTROLLER,
                        "blue")


    def on_update(self, delta_time: float):
        super().on_update(delta_time)

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
            self.healthBars.draw()
            self.bullets.draw()
            self.explosions.draw()
            self.scoreboard.on_draw()


    def reset(self):
        self.players_list = []

        self.players = None
        self.setup_spritelists()
        self.setup_players()
        self.setup_players_cameras()
