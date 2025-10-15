from typing import Optional

from SpaceGame.PlayZone import PlayZone
from typing import Optional

import arcade

from SpaceGame.gamemodes.basegame import BaseGame
from SpaceGame.PlayZone import PlayZone
from SpaceGame.gametypes.Ship import ShipData
from SpaceGame.settings import ALIVE, PLAYER_ONE, PLAYER_TWO, CONTROLLER, KEYBOARD, DEAD
from SpaceGame.gametypes.PlayZoneTypes import CollisionTypes
from SpaceGame.shared.physics import ship_bullet_hit_handler, spaceObject_bullet_hit_handler

class SinglePlayerTest(BaseGame):
    def __init__(self, settings):
        super().__init__(settings)
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
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=self.settings['DEFAULT_DAMPING'],
                                                         gravity=(0, 0))

    def setup_playzone(self):
        self.play_zone = PlayZone(self, self.settings['DEFAULT_BACKGROUND'], self.settings['PLAY_ZONE'])
        self.play_zone.setup(background=True,
                             boundry=False,
                             spacejunk=False,
                             ufo=False
                            )

    def setup_players(self):
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
                        ((self.play_zone.width / 2) - 50, (self.play_zone.height / 2) - 50),
                        KEYBOARD,
                        "orange",
                        player_data)

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        for player in range(len(self.players)):
            if self.players[player].status != DEAD:
                self.center_camera_on_player(player)

    def on_hide_view(self):
        pass

    def on_draw(self):
        for player in range(len(self.players)):
            self.cameras[player].use()
            self.clear()
            self.play_zone.draw()
            self.players.draw()
            self.healthBars.draw()
            self.bullets.draw()
            self.explosions.draw()

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