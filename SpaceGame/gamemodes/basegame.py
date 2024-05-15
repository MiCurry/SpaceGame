import math
from typing import Optional, Tuple

import arcade

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


class BaseGame(arcade.View):
    def __init__(self):
        self.screen_width: int = SCREEN_WIDTH
        self.screen_height: int = SCREEN_HEIGHT

        super().__init__()

        arcade.set_background_color(BACKGROUND_COLOR)

    def setup(self):
        self.setup_spritelists()
        self.setup_physics_engine()
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
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING,
                                                         gravity=(0, 0))

    def resize_viewport(self):
        half_width = self.screen_width // 2
        self.cameras[PLAYER_ONE].viewport = (0, 0, half_width, self.screen_height)
        self.cameras[PLAYER_TWO].viewport = (half_width, 0, half_width, self.screen_height)
        self.cameras[PLAYER_ONE].equalise()
        self.cameras[PLAYER_TWO].equalise()

    def on_update(self, delta_time):
        self.physics_engine.step()
        self.play_zone.update()
        self.explosions.update()
        self.bullets.update()
        self.players.on_update(delta_time)


    def on_resize(self, width: float, height: float):
        self.screen_width = width
        self.screen_height = height
        self.window.on_resize(self.screen_width, self.screen_height)

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.R:
            for player in self.players:
                self.reset()

        for player in self.players:
            player.on_key_press(key, modifiers)

    def on_key_release(self, key: int, modifers: int):
        for player in self.players:
            player.on_key_release(key, modifers)

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
