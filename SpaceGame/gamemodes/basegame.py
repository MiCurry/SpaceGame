import math
from typing import Optional, Tuple

import arcade

from SpaceGame.gametypes.Bullet import Bullet
from SpaceGame.gametypes.Explosion import Explosion
import SpaceGame.menus.pause_menu
from SpaceGame.gametypes.HealthBar import HealthBar
from SpaceGame.gametypes.Player import Player
from SpaceGame.settings import PLAYER_ONE, PLAYER_TWO, CONTROLLER, KEYBOARD, DEAD, Setting, SettingsManager
from SpaceGame.gametypes.PlayZoneTypes import CollisionTypes
from SpaceGame.shared.maths import squared_distance, x_y_distance
from SpaceGame.shared.physics import bullet_bug_hit_handler, bullet_ufo_hit_handler, ship_bullet_hit_handler, spaceObject_bullet_hit_handler


class BaseGame(arcade.View):
    def __init__(self, settings):
        self.settings : SettingsManager = settings
        self.default_camera = None
        self.divider_sprite = None
        self.divider = None
        self.play_zone = None
        self.cameras = None
        self.players_viewports = []
        self.players_list = []
        self.screen_width: int = self.settings['SCREEN_WIDTH']
        self.screen_height: int = self.settings['SCREEN_HEIGHT']

        # Sprite Lists
        self.players: Optional[Player] = None
        self.bullets: Optional[Bullet] = None
        self.explosions: Optional[Explosion] = None
        self.healthBars: Optional[HealthBar] = None

        super().__init__()
        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None
        arcade.set_background_color(self.settings['BACKGROUND_COLOR'])
        self.register_with_settings()

    def setup(self):
        self.screen_width = self.window.width
        self.screen_height = self.window.height
        self.setup_spritelists()
        self.setup_physics_engine()
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

        self.physics_engine.add_collision_handler(CollisionTypes.BULLET.value,
                                                  CollisionTypes.UFO.value,
                                                  post_handler=bullet_ufo_hit_handler,
                                                  collision_data=data
                                                  )
                                                  
        self.physics_engine.add_collision_handler(CollisionTypes.BULLET.value,
                                                  CollisionTypes.BUG.value,
                                                  post_handler=bullet_bug_hit_handler,
                                                  collision_data=data
                                                  )


    def setup_physics_engine(self):
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=self.settings['DEFAULT_DAMPING'],
                                                         gravity=(self.settings['GRAVITY_X'], 
                                                                  self.settings['GRAVITY_Y']))

    def on_update(self, delta_time):
        self.physics_engine.step()
        self.play_zone.update()
        self.explosions.update()
        self.bullets.update()
        self.players.on_update(delta_time)

    def resize_divider(self, width, height):
        if self.divider:
            self.divider_sprite.height = height
            self.divider_sprite.center_x = width / 2
            self.divider_sprite.center_y = height / 2

    def resize_viewports(self):
        if self.num_players() == 2:
            half_width = self.screen_width // 2
            self.cameras[PLAYER_ONE].viewport = (0, 0, half_width, self.screen_height)
            self.cameras[PLAYER_TWO].viewport = (half_width, 0, half_width, self.screen_height)
            self.cameras[PLAYER_ONE].equalise()
            self.cameras[PLAYER_TWO].equalise()
        else:
            self.cameras[PLAYER_ONE].viewport = (0, 0, self.screen_width, self.screen_height)
            self.cameras[PLAYER_ONE].equalise()

    def on_resize(self, width: float, height: float):
        self.screen_width = width
        self.screen_height = height
        super().on_resize(width, height)
        self.resize_viewports()
        self.resize_divider(width, height)

    def num_players(self):
        return len(self.players)

    def setup_single_player_camera(self):
        player_one_camera = arcade.camera.Camera2D()
        self.players_viewports.append(player_one_camera.viewport)
        self.cameras.append(player_one_camera)
        self.center_camera_on_player(PLAYER_ONE)

    def setup_two_player_cameras(self):
        half_width = self.screen_width // 2

        player_one_camera = arcade.camera.Camera2D()
        player_one_camera.viewport = (-1, 0, half_width, self.screen_height)
        player_one_camera.equalise()

        player_two_camera = arcade.camera.Camera2D()
        player_two_camera.viewport = (half_width, 0, half_width, self.screen_height)
        player_two_camera.equalise()

        self.cameras.append(player_one_camera)
        self.cameras.append(player_two_camera)

        self.center_camera_on_player(PLAYER_ONE)
        self.center_camera_on_player(PLAYER_TWO)

        self.default_camera = arcade.camera.Camera2D()
        self.default_camera.viewport = (0, 0, self.screen_width, self.screen_height)

    def setup_splitscreen_sprite(self):
        self.divider = arcade.SpriteList()
        self.divider_sprite = arcade.sprite.SpriteSolidColor(
            center_x=self.screen_width / 2,
            center_y=self.screen_height / 2,
            width=2.5,
            height=self.screen_height,
            color=arcade.color.Color(255, 255, 255))
        self.divider.append(self.divider_sprite)

    def center_camera_on_player(self, player_num):
        self.cameras[player_num].position = (self.players_list[player_num].center_x,
                                             self.players_list[player_num].center_y)

    def setup_players_cameras(self):
        if self.num_players() == 1:
            self.setup_single_player_camera()
        elif self.num_players() == 2:
            self.setup_two_player_cameras()
        else:
            raise ValueError("Too many players expected! Can only handle 1 or 2 players.")

    def add_player_class(self, player: Player):
        player.visible = True
        self.add_player_to_pymunk(player)
        player.setup()

    def add_player(self,
                   player_name: str,
                   player_number: int,
                   start_position: Tuple[int, int],
                   input_source: str,
                   ship_color: str,
                   data):

        self.players.append(Player(self,
                                   player_name,
                                   data,
                                   start_position,
                                   player_number,
                                   input_source=input_source,
                                   ship_color=ship_color,
                                   ))

        self.physics_engine.add_sprite(self.players[player_number],
                                       friction=self.players[player_number].friction,
                                       elasticity=self.players[player_number].elasticity,
                                       mass=self.players[player_number].mass,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type=CollisionTypes.SHIP.value)

        self.players_list.append(self.players[player_number])
        self.players[player_number].setup()

    def register_with_settings(self):
        self._register_handle('GRAVITY_X')
        self._register_handle('GRAVITY_Y')

    def _register_handle(self, setting_name : str):
        setting : Setting = self.settings.get(setting_name)
        setting.register_handle(self.signal_handler)

    def signal_handler(self, setting : Setting):
        if setting.name == "GRAVITY_X":
            self.update_gravity(gravity_x=setting.value)
        elif setting.name == 'GRAVITY_Y':
            self.update_gravity(gravity_y=setting.value)

    def update_gravity(self, gravity_x=None, gravity_y=None):
        cur_g_x, cur_g_y = self.physics_engine.space.gravity

        if gravity_x is not None:
            new_g_x = gravity_x
        else:
            new_g_x = cur_g_x

        if gravity_y is not None:
            new_g_y = gravity_y
        else:
            new_g_y = cur_g_y

        self.physics_engine.space.gravity = (new_g_x, new_g_y)

    def do_pause(self):
        pause_screen = SpaceGame.menus.pause_menu.PauseMenu(self, self.settings)
        self.window.show_view(pause_screen)

    def zoom_camera_out(self):
        for camera in self.cameras:
            camera.zoom -= 0.1

    def zoom_camera_in(self):
        for camera in self.cameras:
            camera.zoom += 0.1

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.R:
            for player in self.players:
                player.reset()
        elif key == arcade.key.ESCAPE:
            self.do_pause()
        elif key == arcade.key.NUM_SUBTRACT or key == arcade.key.MINUS:
            self.zoom_camera_out()
        elif key == arcade.key.NUM_ADD or key == arcade.key.EQUAL:
            self.zoom_camera_in()

    # Given an object and n spritelists, find the nearest sprite to the object found
    # within the spritelists
    def find_nearest_sprite(self, object, *spritelists):
        sprites = []
        for s in spritelists:
            sprites += s

        min_distance = float('inf')
        nearest_sprite = None
        for sprite in sprites:
            if object == sprite:
                continue

            dis = squared_distance(object, sprite)
            if dis < min_distance:
                min_distance = dis
                nearest_sprite = sprite

        return nearest_sprite, math.sqrt(min_distance), x_y_distance(object, nearest_sprite)

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

    def add_player_to_pymunk(self, player):
        self.physics_engine.add_sprite(player,
                                       friction=player.friction,
                                       elasticity=player.elasticity,
                                       mass=player.mass,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type=CollisionTypes.SHIP.value)
