from typing import Optional
import arcade
import math

import Controller
from SpaceGameDiags import SpaceGameDiagnostics
from Explosion import Explosion
from Bullet import Bullet
from HealthBar import HealthBar

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TITLE = "SPACE"
BACKGROUND_COLOR = arcade.color.AIR_SUPERIORITY_BLUE

MOVEMENT_SPEED = 500.0

DEAD_ZONE_LEFT_STICK = 0.05
DEAD_ZONE_RIGHT_STICK = 0.1

SHIP_SCALING = 0.5

GRAVITY = 0.0
SHIP_MASS = 1.0
SHIP_FRICTION = 0.0

DEFAULT_DAMPING = 1.0
SHIP_DAMPING = 1.0

ROTATION_SPEED = 0.05

CONTROLLER = 'controller'
KEYBOARD = 'keyboard'

KEYBOARD_THRUSTER_FORCE = 200.0
KEYBOARD_ROTATION_FORCE = 0.05

SHIP_STARTING_HITPOINTS = 5

ALIVE = True
DEAD = False


class Ship(arcade.Sprite):
    HEALTHBAR_OFFSET = 32

    def __init__(self, sprite_file):
        self.sprite_file = sprite_file
        self.mass = SHIP_MASS
        self.friction = SHIP_FRICTION
        self.status = ALIVE
        super().__init__(sprite_file)
        self.scale = SHIP_SCALING
        self.texture = arcade.load_texture(sprite_file, hit_box_algorithm="Detailed")
        self.hitpoints = SHIP_STARTING_HITPOINTS
        self.healthBar = HealthBar(
            self, window.healthBars, (self.center_x, self.center_y)
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
        window.add_explosion(self.position, Explosion.NORMAL)
        self.status = DEAD

    def damage(self, damage):
        self.hitpoints -= damage
        self.healthBar.fullness = (self.hitpoints / SHIP_STARTING_HITPOINTS)
    
def ship_bullet_hit_handler(bullet, ship, arbiter, space, data):
    if bullet.player_number != ship.player_number:
        bullet.remove_from_sprite_lists()
        ship.damage(bullet.damage)
        window.add_explosion(bullet.body.position, Explosion.SMALL)


class Player(Ship):
    def __init__(self, main, start_position, player_number=0, input_source=CONTROLLER, ship_color='orange'):
        self.input_source = input_source
        self.controller = None
        self.player_number = player_number
        self.sprite_filename = None

        if ship_color == "orange":
            self.sprite_filename = ":resources:images/space_shooter/playerShip1_orange.png"
        elif ship_color == "blue":
            self.sprite_filename = ":resources:images/space_shooter/playerShip1_blue.png" 
        else:
            self.sprite_filename = ":resources:images/space_shooter/playerShip1_orange.png"

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
        
        super().__init__(self.sprite_filename)

    def setup(self):
        self.body = self.main.physics_engine.get_physics_object(self).body       

    def apply_angle_damping(self):
        self.body.angular_velocity /= 1.05

    def on_update(self, delta_time):
        super().update()

        if self.input_source == CONTROLLER:
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

    def on_joybutton_press(self, joystick, button):
        if button == Controller.CONTROLLER_RIGHT_BUMPER:
            self.shoot()

    def on_key_press(self, key, modifiers):
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

    def on_key_release(self, key, modifiers):
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


        

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, resizable=True)
        arcade.set_background_color(arcade.color.SPACE_CADET)
        self.players: Optional[Player] = None
        self.bullets: Optional[Bullet] = None
        self.explosions: Optional[Explosion] = None
        self.healthBars: Optional[HealthBar] = None
        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None
        self.diag = SpaceGameDiagnostics(self)

    def on_resize(self, width, height):
        super().on_resize(width, height)

    def setup(self):
        self.players = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        self.healthBars = arcade.SpriteList()

        # Player 1 
        self.players.append(Player(self,
                                   (SCREEN_WIDTH - 100.0, SCREEN_HEIGHT - 100.0),
                                   0,
                                   input_source=CONTROLLER))

        self.players[0].center_x = SCREEN_WIDTH - 100.0
        self.players[0].center_y = SCREEN_HEIGHT - 100.0

        # Player 2
        self.players.append(Player(self,
                                   (100.0, 100.0),
                                   1,
                                   input_source=KEYBOARD,
                                   ship_color='blue'))

        self.players[1].center_x = 100.0
        self.players[1].center_y = 100.0

        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING,
                                                         gravity=(0,0))

        self.physics_engine.add_sprite(self.players[0],
                                       friction=self.players[0].friction,
                                       mass=self.players[0].mass,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="ship")

        self.physics_engine.add_sprite(self.players[1],
                                       friction=self.players[1].friction,
                                       mass=self.players[1].mass,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="ship")

        self.physics_engine.add_collision_handler("bullet", "ship", post_handler=ship_bullet_hit_handler)

        for player in self.players:
            player.setup()

        self.diag.setup()

    def reset(self):
        for player in self.players:
            player.reset()
            self.physics_engine.remove_sprite(player)
        
        while (len(self.players) != 0):
            self.players.pop()

        for player in self.players:
            print(player.player_number)

        self.players = None
        self.setup()

    def on_key_press(self, key, modifiers):
        self.diag.on_key_press(key, modifiers) 

        if key == arcade.key.R:
            for player in self.players:
                self.reset()

        for player in self.players:
            player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifers):
        for player in self.players:
            player.on_key_release(key, modifers)

    def on_update(self, delta_time):
        self.players.on_update(delta_time)
        self.physics_engine.step()
        self.explosions.update()

    def on_draw(self):
        self.clear()
        self.players.draw()
        self.healthBars.draw()
        self.bullets.draw()
        self.diag.on_draw()
        self.explosions.draw()

    def add_explosion(self, position, scale):
        self.explosions.append(Explosion(position, scale))
        




window = Game()
window.setup()
arcade.run()