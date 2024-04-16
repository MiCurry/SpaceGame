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
PLAYER_TWO = 1

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


class Ship(arcade.Sprite):
    HEALTHBAR_OFFSET = 32

    def __init__(self, sprite_file: str, main):
        self.sprite_file = sprite_file
        super().__init__(self.sprite_file)
        self.mass = SHIP_MASS
        self.friction = SHIP_FRICTION
        self.elasticity = SHIP_ELASTICITY
        self.status = ALIVE
        self.scale = SHIP_SCALING
        self.texture = arcade.load_texture(sprite_file, hit_box_algorithm=arcade.hitbox.PymunkHitBoxAlgorithm())
        self.hitpoints = SHIP_STARTING_HITPOINTS
        self.main = main
        self.healthBar = HealthBar(
            self, self.main.healthBars, (self.center_x, self.center_y)
        )

    def update(self):
        if self.hitpoints <= 0:
            self.explode()

        self.healthBar.position = (
            self.center_x,
            self.center_y + Ship.HEALTHBAR_OFFSET,
        )

    def shoot(self):
        if self.status is ALIVE:
            Bullet(self.main,
                   (self.center_x, self.center_y),
                   self.body.angle,
                   self.body.velocity[0],
                   self.body.velocity[1],
                   self.player_number)

    def explode(self):
        self.remove_from_sprite_lists()
        self.healthBar.remove()
        self.main.add_explosion(self.position, ExplosionSize.NORMAL)
        self.status = DEAD

    def damage(self, damage: int):
        self.hitpoints -= damage
        self.healthBar.fullness = (self.hitpoints / SHIP_STARTING_HITPOINTS)


def ship_bullet_hit_handler(bullet: Bullet, ship: Ship, arbiter, space, data):
    if bullet.creator != ship.player_number:
        bullet.remove_from_sprite_lists()
        ship.damage(bullet.damage)
        window.add_explosion(bullet.body.position, ExplosionSize.SMALL)


def spaceObject_bullet_hit_handler(bullet: Bullet, junk: SpaceObject, arbiter, space, data):
    bullet.remove_from_sprite_lists()
    window.add_explosion(bullet.body.position, ExplosionSize.SMALL)
    junk.damage(bullet.damage)


class Player(Ship):
    def __str__(self):
        return f"Player: {self.player_number} - {self.player_name}"

    def __init__(self, main, player_name,
                 start_position: Tuple,
                 player_number=0,
                 input_source=CONTROLLER,
                 ship_color='orange'):
        self.player_name = player_name
        self.input_source = input_source
        self.controller = None
        self.player_number = player_number
        self.sprite_filename = None

        if ship_color == "orange":
            self.sprite_filename = "./resources/png/sprites/Ships/playerShip1_orange.png"
        elif ship_color == "blue":
            self.sprite_filename = "./resources/png/sprites/Ships/playerShip1_blue.png"
        else:
            self.sprite_filename = "./resources/png/sprites/Ships/playerShip1_orange.png"

        self.main = main
        self.dx = 0.0
        self.dy = 0.0
        self.force = 0.0
        self.applied_rotational_vel = 0
        self.body = None
        self.start_position = start_position
        self.friction = SHIP_FRICTION

        self.w_pressed = 0.0
        self.s_pressed = 0.0
        self.a_pressed = 0.0
        self.d_pressed = 0.0
        self.left_pressed = 0.0
        self.right_pressed = 0.0

        self.status = ALIVE

        if Controller.do_we_haz_controller() and self.input_source == CONTROLLER:
            Controller.add_controller_to_player(self)

        super().__init__(self.sprite_filename, self.main)

    def setup(self):
        self.body = self.main.physics_engine.get_physics_object(self).body
        self.shape = self.main.physics_engine.get_physics_object(self).shape

    def apply_angle_damping(self):
        self.body.angular_velocity /= 1.05

    def on_update(self, delta_time: float):
        super().update()

        if self.input_source == CONTROLLER and self.controller:
            self.dx = Controller.apply_deadzone(self.controller.x,
                                                dead_zone=DEAD_ZONE_LEFT_STICK) * MOVEMENT_SPEED
            self.dy = Controller.apply_deadzone(self.controller.y,
                                                dead_zone=DEAD_ZONE_LEFT_STICK) * MOVEMENT_SPEED
            self.applied_rotational_vel = Controller.apply_deadzone(-self.controller.z,
                                                                    dead_zone=DEAD_ZONE_RIGHT_STICK) * ROTATION_SPEED

        if self.input_source == KEYBOARD:
            self.dx = self.a_pressed + self.d_pressed
            self.dy = self.w_pressed + self.s_pressed
            self.applied_rotational_vel = self.left_pressed - self.right_pressed

        if self.applied_rotational_vel == 0.0:
            self.apply_angle_damping()

        self.body.angular_velocity += self.applied_rotational_vel
        self.body.apply_force_at_world_point((self.dx, -self.dy), (self.center_x, self.center_y))

    def on_joybutton_press(self, joystick, button: int):
        if button == Controller.CONTROLLER_RIGHT_BUMPER:
            self.shoot()

    def on_key_press(self, key: int, modifiers: int):
        if self.input_source == KEYBOARD:
            if key == arcade.key.W:
                self.w_pressed = -KEYBOARD_THRUSTER_FORCE
            elif key == arcade.key.S:
                self.s_pressed = KEYBOARD_THRUSTER_FORCE
            elif key == arcade.key.A:
                self.a_pressed = -KEYBOARD_THRUSTER_FORCE
            elif key == arcade.key.D:
                self.d_pressed = KEYBOARD_THRUSTER_FORCE
            elif key == arcade.key.LEFT:
                self.left_pressed = KEYBOARD_ROTATION_FORCE
            elif key == arcade.key.RIGHT:
                self.right_pressed = KEYBOARD_ROTATION_FORCE

            if key == arcade.key.SPACE:
                self.shoot()

    def on_key_release(self, key: int, modifiers: int):
        if self.input_source == KEYBOARD:
            if key == arcade.key.W:
                self.w_pressed = 0.0
            elif key == arcade.key.S:
                self.s_pressed = 0.0
            elif key == arcade.key.A:
                self.a_pressed = 0.0
            elif key == arcade.key.D:
                self.d_pressed = 0.0
            elif key == arcade.key.LEFT:
                self.left_pressed = 0.0
            elif key == arcade.key.RIGHT:
                self.right_pressed = 0.0

    def reset(self):
        self.body.apply_force_at_world_point((0.0, 0.0), (self.center_x, self.center_y))
        self.dx = 0.0
        self.dy = 0.0
        self.body.velocity = (0.0, 0.0)
        self.body.position = (self.start_position)
        self.center_x = self.start_position[0]
        self.center_y = self.start_position[1]
        self.body.angular_velocity = 0.0
        self.applied_rotational_vel = 0
        if self.controller:
            self.controller.remove_handlers(self)


# We can save some compute time by using the squared distance.
def squared_distance(a, b) -> float:
    return ((a.center_x - b.center_x) ** 2 + (a.center_y - b.center_y) ** 2)


def distance(a, b) -> float:
    return math.sqrt(squared_distance(a, b))


class Game(arcade.Window):
    def __init__(self):
        self.cameras = []
        self.player_one_projection_data = None
        self.player_one_viewport = None
        self.player_two_projection_data = None
        self.player_two_viewport = None
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
        self.player_viewport: Optional[Tuple[int, int, int, int]] = []

    def setup_players_cameras(self):
        half_width = self.screen_width // 2

        self.player_one_viewport = (0, 0, half_width, SCREEN_HEIGHT)  # left, bottom, width, height
        self.player_two_viewport = (half_width, 0, half_width, SCREEN_HEIGHT)  # left, bottom, width, height

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
        self.play_zone.setup()

    def setup_physics_engine(self):
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING,
                                                         gravity=(0, 0))

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

    def setup_collision_handlers(self):
        self.physics_engine.add_collision_handler(CollisionTypes.BULLET.value,
                                                  CollisionTypes.SHIP.value,
                                                  post_handler=ship_bullet_hit_handler)
        self.physics_engine.add_collision_handler(CollisionTypes.BULLET.value,
                                                  CollisionTypes.SPACE_JUNK.value,
                                                  post_handler=spaceObject_bullet_hit_handler)

    def setup(self):
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

        if self.players_list[PLAYER_TWO].status != DEAD:
            self.center_camera_on_player(PLAYER_TWO)

    def center_camera_on_player(self, player_num):
        self.cameras[player_num].position = (self.players_list[player_num].center_x,
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


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
