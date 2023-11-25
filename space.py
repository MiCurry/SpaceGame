from typing import Optional
import arcade
import math



SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TITLE = "SPACE"
BACKGROUND_COLOR = arcade.color.AIR_SUPERIORITY_BLUE

MOVEMENT_SPEED = 500.0

DEFAULT_DEAD_ZONE = 0.05
DEAD_ZONE_LEFT_STICK = 0.05
DEAD_ZONE_RIGHT_STICK = 0.1

SHIP_SCALING = 0.5

GRAVITY = 0.0
SHIP_MASS = 1.0
SHIP_FRICTION = 1.0

DEFAULT_DAMPING = 1.0
SHIP_DAMPING = 1.0

ROTATE_OFFSET = -90

ROTATION_SPEED = 0.05

CONTROLLER = 'controller'
KEYBOARD = 'keyboard'

KEYBOARD_THRUSTER_FORCE = 200.0
KEYBOARD_ROTATION_FORCE = 0.05

BULLET_MASS = 0.01
BULLET_FRICTION = 0.0
BULLET_VELOCITY = 1500.0
BULLET_ROTATION_OFFSET = math.pi / 2.0
BULLET_SPAWN_OFFSET = 65.0

CONTROLLER_RIGHT_BUMPER = 7


class Ship(arcade.Sprite):
    def __init__(self, sprite_file):
        self.sprite_file = sprite_file
        self.mass = SHIP_MASS
        self.friction = SHIP_FRICTION
        super().__init__(sprite_file)
        self.texture = arcade.load_texture(sprite_file, hit_box_algorithm="Detailed")



def apply_deadzone(v, dead_zone=DEFAULT_DEAD_ZONE):
    if abs(v) < dead_zone:
        return 0
    return v



class Bullet(arcade.Sprite):
    def __init__(self, main, start_position, angle):
        self.sprite_file = ":resources:images/space_shooter/laserBlue01.png"
        super().__init__(self.sprite_file)
        self.main = main
        self.mass = BULLET_MASS
        self.friction = BULLET_FRICTION
        self.center_x = start_position[0] + BULLET_SPAWN_OFFSET * math.cos(angle + BULLET_ROTATION_OFFSET)
        self.center_y = start_position[1] + BULLET_SPAWN_OFFSET * math.sin(angle + BULLET_ROTATION_OFFSET)
        self.main.physics_engine.add_sprite(self,
                                friction=self.friction,
                                mass=self.mass,
                                moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                collision_type="bullet")

        self.texture = arcade.load_texture(self.sprite_file, hit_box_algorithm="Detailed")
        self.body = self.main.physics_engine.get_physics_object(self).body
        self.body.angle = angle + BULLET_ROTATION_OFFSET

        self.dy = math.cos(angle) * BULLET_VELOCITY
        self.dx = math.sin(angle) * BULLET_VELOCITY
        self.body.apply_force_at_world_point((-self.dx, self.dy), (self.center_x, self.center_y))
        self.main.bullets.append(self)


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

        self.w_pressed = 0.0
        self.s_pressed = 0.0
        self.a_pressed = 0.0
        self.d_pressed = 0.0 
        self.left_pressed = 0.0
        self.right_pressed = 0.0

        if do_we_haz_controller() and self.input_source == CONTROLLER:
            add_controller_to_player(self)
        
        super().__init__(self.sprite_filename)


    def setup(self):
        self.body = self.main.physics_engine.get_physics_object(self).body       


    def on_update(self, delta_time):
        if self.input_source == CONTROLLER:
            self.dx = apply_deadzone(self.controller.x, dead_zone=DEAD_ZONE_LEFT_STICK) * MOVEMENT_SPEED
            self.dy = apply_deadzone(self.controller.y, dead_zone=DEAD_ZONE_LEFT_STICK) * MOVEMENT_SPEED
            self.applied_rotational_vel = apply_deadzone(-self.controller.z, dead_zone=DEAD_ZONE_RIGHT_STICK) * ROTATION_SPEED 

        if self.input_source == KEYBOARD:
            self.dx = self.a_pressed + self.d_pressed
            self.dy = self.w_pressed + self.s_pressed
            self.applied_rotational_vel = self.left_pressed - self.right_pressed

        self.body.angular_velocity += self.applied_rotational_vel
        self.body.apply_force_at_world_point((self.dx, -self.dy), (self.center_x, self.center_y))

    def on_joybutton_press(self, joystick, button):
        if button == CONTROLLER_RIGHT_BUMPER:
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

    def shoot(self):
        Bullet(self.main, (self.center_x, self.center_y), self.body.angle)

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
        self.body.angular_velocity = 0.0
        self.applied_rotational_vel = 0


class AI_SHIP(Ship):
    pass


class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
        self.players: Optional[Player] = None
        self.bullets: Optional[Bullet] = None
        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None
        arcade.set_background_color(arcade.color.SPACE_CADET)
        self.diag = SpaceGameDiagnostics(self)

    def setup(self):
        self.players = arcade.SpriteList()
        self.bullets = arcade.SpriteList()

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
                                       collision_type="player")


        self.physics_engine.add_sprite(self.players[1],
                                       friction=self.players[1].friction,
                                       mass=self.players[1].mass,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player")

        for player in self.players:
            player.setup()

        self.diag.setup()

    def on_key_press(self, key, modifiers):
        self.diag.on_key_press(key, modifiers) 

        if key == arcade.key.R:
            for player in self.players:
                player.reset()

        for player in self.players:
            player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifers):
        for player in self.players:
            player.on_key_release(key, modifers)

    def on_update(self, delta_time):
        self.players.on_update(delta_time)
        self.physics_engine.step()

    def on_draw(self):
        self.clear()
        self.players.draw()
        self.bullets.draw()
        self.diag.on_draw()
        

def do_we_haz_controller():
    return arcade.get_game_controllers()


def get_and_open_controller(controller_number):
    controller = arcade.get_game_controllers()[0]
    controller.open()
    return controller


def register_controller_to_player(player):
    player.controller.push_handlers(player)


def add_controller_to_player(player):
    player.controller = get_and_open_controller(player.player_number)
    register_controller_to_player(player)


class DiagnosticsController():
    def __init__(self, game):
        self.game = game
        self.START_HEIGHT_OFFSET = 20
        self.HEIGHT_OFFSET = 20
        self.WIDTH_OFFSET = 20
        self.num_active = 0
        self.diags = []
        self.active_diags = []

    # Convert a non f"str" to a f"str"
    def fstr(template):
        return eval(f"f'{template}'")

    def add_diagnostic(self, 
                        key,
                        output_message, 
                        display_at_start, 
                        text_color=arcade.color.WHITE):

        diag = {'key' : key,
                'output' : output_message,
                'text_color' : text_color,
                'display' : display_at_start}
        self.diags.append(diag)
        if display_at_start:
            self.active_diags.append(diag)

    def on_key_press(self, key, modifiers):
        for diag in self.diags:
            if key == diag['key'] and diag in self.active_diags:
                self.active_diags.remove(diag)
            elif key == diag['key'] and diag not in self.active_diags:
                self.active_diags.append(diag)

    def get_offset(self, display_number):
        return (display_number + 1) * self.HEIGHT_OFFSET

    def on_draw(self):
        for display_number, diag in enumerate(self.active_diags):
            self.display_diagnostics(diag, display_number)

    def display_diagnostics(self, diag, display_number):
        arcade.draw_text(diag['output'](self.game),
                         self.WIDTH_OFFSET, 
                         (self.game.height - self.START_HEIGHT_OFFSET) - self.get_offset(display_number),
                         diag['text_color'])


class SpaceGameDiagnostics(DiagnosticsController):
    def __init__(self, game):
        super().__init__(game)

    def setup(self):
        self.add_diagnostic(arcade.key.I,
                            lambda game: f"Left Stick: ({game.players[0].controller.x:.5f}, {game.players[0].controller.y:.5f})",
                            display_at_start=False)

        self.add_diagnostic(arcade.key.O,
                            lambda game: f"Right Stick: ({game.players[0].controller.z:.5f}, {game.players[0].controller.rz:.5f})",
                            display_at_start=False)

        self.add_diagnostic(arcade.key.U,
                            lambda game: f"Rotation: ({game.players[0].applied_rotational_vel:.5f}, {game.players[0].applied_rotational_vel:.5f})",
                            display_at_start=False)

        self.add_diagnostic(arcade.key.Y,
                            lambda game: f"Acceleration: ({game.players[0].dx:.5f}, {game.players[0].dy:.5f})",
                            display_at_start=False)

        self.add_diagnostic(arcade.key.H,
                            lambda game: f"Velocity: ({game.players[0].body.velocity[0]:.5f}, {game.players[0].body.velocity[1]:.5f})",
                            display_at_start=False)

        self.add_diagnostic(arcade.key.J,
                            lambda game: f"Angular Vel: ({game.players[0].body.angular_velocity:.5f})",
                            display_at_start=False)


window = Game()
window.setup()
arcade.run()