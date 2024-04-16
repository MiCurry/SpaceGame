import math
from typing import Optional, Tuple
from pathlib import Path

import arcade

import Controller
from SpaceGameTypes.SpaceGameTypes import CollisionTypes
from SpaceGameDiags import SpaceGameDiagnostics
from SpaceGameTypes.Explosion import Explosion, ExplosionSize
from SpaceGameTypes.Bullet import Bullet
from SpaceGameTypes.HealthBar import HealthBar
from PlayZone import PlayZone, SpaceObject
from PlayZone import Background

from space import distance, squared_distance
from player import Player
from ship import Ship

# Left, Right, Width, Height
PLAY_ZONE = (4, 4)

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000
SCREEN_SPLIT_WIDTH = SCREEN_WIDTH / 2.0

TITLE = "SPACE"
BACKGROUND_COLOR = arcade.color.AIR_SUPERIORITY_BLUE
BACKGROUND_IMAGE = "./resources/png/backgrounds/stars.png"

DEFAULT_BACKGROUND = Background(BACKGROUND_IMAGE,
                                1024,
                                1024,
                                1.0)

PLAYER_ONE = 0

MOVEMENT_SPEED = 500.0

DEAD_ZONE_LEFT_STICK = 0.05
DEAD_ZONE_RIGHT_STICK = 0.1

SHIP_SCALING = 0.5

GRAVITY = 0.0
SHIP_MASS = 1.0
SHIP_FRICTION = 0.0
SHIP_ELASTICITY = 0.1

DEFAULT_DAMPING = 1.0
SHIP_DAMPING = 1.0

CONTROLLER = 'controller'
KEYBOARD = 'keyboard'

ROTATION_SPEED = 0.05
KEYBOARD_THRUSTER_FORCE = 200.0
KEYBOARD_ROTATION_FORCE = 0.05

SHIP_STARTING_HITPOINTS = 5

ALIVE = True
DEAD = False

def ship_bullet_hit_handler(bullet: Bullet, ship: Ship, arbiter, space, data):
    if bullet.creator != ship.player_number:
        bullet.remove_from_sprite_lists()
        ship.damage(bullet.damage)
        window.add_explosion(bullet.body.position, ExplosionSize.SMALL)

def spaceObject_bullet_hit_handler(bullet: Bullet, junk: SpaceObject, arbiter, space, data):
    bullet.remove_from_sprite_lists()
    window.add_explosion(bullet.body.position, ExplosionSize.SMALL)
    junk.damage(bullet.damage)

class Tester(arcade.Window):
    def __init__(self):
        self.screen_width: int = SCREEN_WIDTH
        self.screen_height: int = SCREEN_HEIGHT
        super().__init__(self.screen_width, self.screen_height,
                         TITLE, resizable=True)
        arcade.set_background_color(arcade.color.SPACE_CADET)
        self.players: Optional[Player] = None
        self.bullets: Optional[Bullet] = None
        self.explosions: Optional[Explosion] = None
        self.healthBars: Optional[HealthBar] = None
        self.diag: Optional[SpaceGameDiagnostics] = SpaceGameDiagnostics(self)
        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None
        self.player_viewport: Optional[Tuple[int, int, int, int]]  = []
        self.cameras: Optional[arcade.camera.Camera2D]= []
        self.players_list = []


    # Given an object and n spritelists, find the nearest sprite to the object found
    # within the spritelists
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
        
    def on_resize(self, width: float, height: float):
        self.screen_width = width
        self.screen_height = height
        super().on_resize(self.screen_width, self.screen_height)
        self.setup_players_cameras()

    def setup_spritelists(self):
        self.players = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        self.healthBars = arcade.SpriteList()

    def setup_playzone(self):
        self.play_zone = PlayZone(self, DEFAULT_BACKGROUND, PLAY_ZONE)
        self.play_zone.setup(spacejunk=False)

    def add_resources(self):
        arcade.resources.add_resource_handle("sprites", Path("./resources/").resolve())

    def setup_physics_engine(self):
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING,
                                                         gravity=(0,0))

    def setup_players_cameras(self):
        self.player_one_viewport = (0.0, 0.0,
                                    self.screen_width, self.screen_height)

        self.cameras = []
        self.cameras.append(arcade.camera.Camera2D(viewport=self.player_one_viewport,
                                                 window=self))

        self.center_camera_on_player(PLAYER_ONE)

    def setup_players(self):
        self.players.append(Player(self, "Star Shooter",
                                   (100.0, 100.0),
                                   0,
                                   input_source=KEYBOARD))
        self.players[PLAYER_ONE].center_x = 100.0
        self.players[PLAYER_ONE].center_y = 100.0

        self.physics_engine.add_sprite(self.players[PLAYER_ONE],
                                       friction=self.players[PLAYER_ONE].friction,
                                       elasticity=self.players[PLAYER_ONE].elasticity,
                                       mass=self.players[PLAYER_ONE].mass,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type=CollisionTypes.SHIP.value)
        self.players_list.append(self.players[PLAYER_ONE])

        for player in self.players:
            player.setup()

    def setup_collision_handlers(self):
        self.physics_engine.add_collision_handler(CollisionTypes.BULLET.value,
                                                  CollisionTypes.SHIP.value,
                                                  post_handler=ship_bullet_hit_handler)
        self.physics_engine.add_collision_handler(CollisionTypes.BULLET.value,
                                                  CollisionTypes.SPACE_JUNK.value,
                                                  post_handler=spaceObject_bullet_hit_handler)

    def setup(self):
        self.add_resources()
        self.setup_spritelists()
        self.setup_physics_engine()
        self.setup_playzone()
        self.setup_players()
        self.setup_players_cameras()
        self.setup_collision_handlers()
        self.diag.setup()

    def reset(self):
        for player in self.players:
            player.reset()
            self.physics_engine.remove_sprite(player)
        
        while (len(self.players) != 0):
            self.players.pop()

        self.players = None
        self.setup_spritelists()
        self.setup_players()

    def on_key_press(self, key: int, modifiers: int):
        self.diag.on_key_press(key, modifiers) 

        if key == arcade.key.R:
            for player in self.players:
                self.reset()

        for player in self.players:
            player.on_key_press(key, modifiers)

    def on_key_release(self, key: int, modifers: int):
        for player in self.players:
            player.on_key_release(key, modifers)


    def on_update(self, delta_time: float):
        self.players.on_update(delta_time)
        self.physics_engine.step()
        self.explosions.update()
        self.bullets.update()
        self.play_zone.update()

        if self.players_list[PLAYER_ONE].status != DEAD:
            self.center_camera_on_player(PLAYER_ONE)

    def center_camera_on_player(self, player_num):
        self.cameras[player_num].position = (self.players_list[player_num].center_x + SCREEN_SPLIT_WIDTH / 2.0,
                                            self.players_list[player_num].center_y)

    def on_draw(self):
        for player in range(len(self.players_list)):
            self.cameras[player].use()
            self.clear()
            self.play_zone.draw()
            self.players.draw()
            self.healthBars.draw()
            self.bullets.draw()
            self.diag.on_draw()
            self.explosions.draw()

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
                                       collision_type=object.type)



window = Tester()
window.setup()
arcade.run()