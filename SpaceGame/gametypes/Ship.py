from dataclasses import dataclass
import arcade
import pymunk

from SpaceGame.gametypes.Bullet import Bullet
from SpaceGame.gametypes.Explosion import ExplosionSize
from SpaceGame.gametypes.HealthBar import HealthBar
from SpaceGame.settings import ALIVE, DEAD, Setting


def pick_ship_file_from_color(color: str) -> str:
    if color == "orange":
        filename = ":sprites:png/sprites/Ships/playerShip1_orange.png"
    elif color == "blue":
        filename = ":sprites:png/sprites/Ships/playerShip1_blue.png"
    else:
        filename = ":sprites:png/sprites/Ships/playerShip1_orange.png"

    return filename

DEFAULT_SHIP_FRICTION = 1.0
DEFAULT_SHIP_MASS = 1.0
DEFAULT_SHIP_SCALING = 0.5
DEFAULT_SHIP_HITPOINTS = 10
DEFAULT_SHIP_ELASTICITY = 0.1
DEFAULT_MOVEMENT_SPEED = 450.0
DEFAULT_ROTATION_SPEED = 0.05

@dataclass
class ShipData:
    status : str
    hitpoints : int
    mass : float
    friction : float
    elasticity : float
    scaling : float
    movement_speed : float
    rotation_speed : float

class Ship(arcade.Sprite):
    HEALTHBAR_OFFSET = 32

    def __init__(self,
                 color: str,
                 main,
                 start_position: (int, int),
                 data : ShipData):

        self.sprite_file = pick_ship_file_from_color(color)
        super().__init__(self.sprite_file)
        self.texture = arcade.load_texture(self.sprite_file,
                                           hit_box_algorithm=arcade.hitbox.PymunkHitBoxAlgorithm())


        # Ship physic stuff
        self.body : pymunk.Body = None
        self.shape : pymunk.Shape = None
        self.movement_speed = data.movement_speed
        self.rotation_speed = data.rotation_speed
        self.friction = data.friction
        self.mass = data.mass
        self.elasticity = data.elasticity
        self.status = data.status
        self.scale = data.scaling
        self.hitpoints = data.hitpoints
        self.max_hitpoints = data.hitpoints

        self.start_position = start_position
        self.position = start_position

        # Applied Forces
        self.dx = 0.0
        self.dy = 0.0
        self.force = 0.0
        self.applied_rotational_vel = 0.0

        self.main = main
        self.setup_healthbar()
        self.register_with_settings()


    def setup_healthbar(self):
        self.healthBar = HealthBar(
            self, self.main.healthBars, (self.center_x, self.center_y)
        )

    def register_with_settings(self):
        self._register_handle('SHIP_STARTING_HITPOINTS')
        self._register_handle('SHIP_MASS')
        self._register_handle('SHIP_FRICTION')
        self._register_handle('SHIP_ELASTICITY')

    def _register_handle(self, setting_name : str):
        setting : Setting = self.main.settings.get(setting_name)
        setting.register_handle(self.signal_handler)

    def signal_handler(self, setting : Setting):
        if setting.name == 'SHIP_MASS':
            self.mass = setting.value
            self.body.mass = setting.value
        elif setting.name == 'SHIP_STARTING_HITPOINTS':
            self.hitpoints = setting.value
            self.max_hitpoints = setting.value
        elif setting.name == 'SHIP_FRICTION':
            self.shape.friction = setting.value
        elif setting.name == 'SHIP_ELASTICITY':
            self.shape.elasticity = setting.value

    def setup(self):
        self.body = self.main.physics_engine.get_physics_object(self).body
        self.shape = self.main.physics_engine.get_physics_object(self).shape

    def update(self):
        if self.status == DEAD:
            return

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
                   self)

    def explode(self):
        self.visible = False
        self.status = DEAD
        self.healthBar.remove()
        self.main.add_explosion(self.position, ExplosionSize.NORMAL)
        self.main.physics_engine.remove_sprite(self)

    def damage(self, bullet):
        self.hitpoints -= bullet.damage
        self.healthBar.fullness = (self.hitpoints / self.max_hitpoints)
        self.last_hit_buy = bullet.creator

    def reset(self):
        self.respawn()

    def respawn(self):
        self.body.apply_force_at_world_point((0.0, 0.0), (self.center_x, self.center_y))
        self.dx = 0.0
        self.dy = 0.0
        self.body.velocity = (0.0, 0.0)
        self.body.position = (self.start_position)
        self.center_x = self.start_position[0]
        self.center_y = self.start_position[1]
        self.body.angular_velocity = 0.0
        self.applied_rotational_vel = 0
        self.visible = True
        self.main.add_player_class(self)
        self.hitpoints = self.max_hitpoints
        self.status = ALIVE
        self.setup_healthbar()

