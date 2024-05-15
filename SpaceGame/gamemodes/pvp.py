import math
from typing import Optional, Tuple

import arcade

from SpaceGame.gamemodes.basegame import BaseGame
from SpaceGame.gametypes.Explosion import Explosion
from SpaceGame.gametypes.Bullet import Bullet
from SpaceGame.gametypes.HealthBar import HealthBar
from SpaceGame.PlayZone import PlayZone
from SpaceGame.gametypes.Player import Player
from SpaceGame.settings import PLAY_ZONE, SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, DEFAULT_BACKGROUND, PLAYER_ONE, \
    PLAYER_TWO, \
    DEFAULT_DAMPING, CONTROLLER, KEYBOARD, DEAD, BACKGROUND_COLOR
from SpaceGame.gametypes.PlayZoneTypes import CollisionTypes
from SpaceGame.shared.maths import squared_distance
from SpaceGame.shared.physics import ship_bullet_hit_handler, spaceObject_bullet_hit_handler


class PvpGame(BaseGame):
    def __init__(self):
        self.screen_width: int = None
        self.screen_height: int = None

        super().__init__()

        arcade.set_background_color(BACKGROUND_COLOR)

        # Sprite Lists
        self.players: Optional[Player] = None
        self.bullets: Optional[Bullet] = None
        self.explosions: Optional[Explosion] = None
        self.healthBars: Optional[HealthBar] = None

        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None

        # Cameras
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

    def setup_spritelists(self):
        self.players = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        self.healthBars = arcade.SpriteList()

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
        self.play_zone.setup()

    def setup_players(self):
        self.players.append(Player(self, "Player 0",
                                   (100.0, 100.0),
                                   0,
                                   input_source=CONTROLLER))

        self.players[PLAYER_ONE].center_x = 100.0
        self.players[PLAYER_ONE].center_y = 100.0

        self.players.append(Player(self, "Player 1",
                                   (self.screen_width - 100.0, self.screen_height - 100.0),
                                   1,
                                   input_source=KEYBOARD,
                                   ship_color='blue'))

        self.players[PLAYER_TWO].center_x = self.screen_width - 100.0
        self.players[PLAYER_TWO].center_y = self.screen_height - 100.0
        self.players_list = [self.players[PLAYER_ONE], self.players[PLAYER_TWO]]

        self.physics_engine.add_sprite(self.players[PLAYER_ONE],
                                       friction=self.players[PLAYER_ONE].friction,
                                       elasticity=self.players[PLAYER_ONE].elasticity,
                                       mass=self.players[PLAYER_ONE].mass,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type=CollisionTypes.SHIP.value)

        self.physics_engine.add_sprite(self.players[PLAYER_TWO],
                                       friction=self.players[PLAYER_TWO].friction,
                                       elasticity=self.players[PLAYER_TWO].elasticity,
                                       mass=self.players[PLAYER_TWO].mass,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type=CollisionTypes.SHIP.value)

        for player in self.players:
            player.setup()

    def setup_players_cameras(self):
        half_width = self.screen_width // 2

        self.player_one_viewport = (0, 0, half_width, self.screen_height)  # left, bottom, width, height
        self.player_two_viewport = (half_width, 0, half_width, self.screen_height)  # left, bottom, width, height

        player_one_camera = arcade.camera.Camera2D()
        player_one_camera.viewport = self.player_one_viewport
        player_one_camera.equalise()

        player_two_camera = arcade.camera.Camera2D()
        player_two_camera.viewport = self.player_two_viewport
        player_two_camera.equalise()

        self.cameras.append(player_one_camera)
        self.cameras.append(player_two_camera)

        self.center_camera_on_player(PLAYER_ONE)
        self.center_camera_on_player(PLAYER_TWO)

    def center_camera_on_player(self, player_num):
        self.cameras[player_num].position = (self.players_list[player_num].center_x,
                                             self.players_list[player_num].center_y)

    def resize_viewport(self):
        half_width = self.screen_width // 2
        self.cameras[PLAYER_ONE].viewport = (0, 0, half_width, self.screen_height)
        self.cameras[PLAYER_TWO].viewport = (half_width, 0, half_width, self.screen_height)
        self.cameras[PLAYER_ONE].equalise()
        self.cameras[PLAYER_TWO].equalise()

    def on_resize(self, width: float, height: float):
        self.screen_width = width
        self.screen_height = height
        super().on_resize(self.screen_width, self.screen_height)
        self.resize_viewport()

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        if self.players_list[PLAYER_ONE].status != DEAD:
            self.center_camera_on_player(PLAYER_ONE)

        if self.players_list[PLAYER_TWO].status != DEAD:
            self.center_camera_on_player(PLAYER_TWO)

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

    # Given an object and n spritelists, find the nearest sprite to the object found
    # within the spritelists
    def find_nearest_sprite(self, object, *spritelists):
        sprites = []
        for s in spritelists:
            sprites += s

        min_distance = float('inf')
        nearest_sprite = None
        for sprite in sprites:
            dis = squared_distance(object, sprite)
            if dis < min_distance:
                min_distance = dis
                nearest_sprite = sprite

        return nearest_sprite, math.sqrt(min_distance)

    def reset(self):
        for player in self.players:
            player.reset()
            self.physics_engine.remove_sprite(player)

        while (len(self.players) != 0):
            self.players.pop()

        self.players = None
        self.setup_spritelists()
        self.setup_players()

    def add_explosion(self, position: Tuple, scale: float):
        self.explosions.append(Explosion(position, scale))

    def add_sprite_to_pymunk(self, object,
                             moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF):
        self.physics_engine.add_sprite(object,
                                       friction=object.friction,
                                       elasticity=object.elasticity,
                                       radius=object._data.radius,
                                       mass=object.mass,
                                       moment_of_inertia=moment_of_inertia,
                                       collision_type=object.type,
                                       )
