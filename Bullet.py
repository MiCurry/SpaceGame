import arcade
import math

BULLET_MASS = 0.005
BULLET_FRICTION = 0.0
BULLET_VELOCITY = 500.0
BULLET_ROTATION_OFFSET = math.pi / 2.0
BULLET_SPAWN_OFFSET = 65.0
BULLET_DAMAGE = 1

class Bullet(arcade.Sprite):
    def __init__(self, main, start_position, angle, start_dx, start_dy, player_number):
        self.sprite_file = ":resources:images/space_shooter/laserBlue01.png"
        super().__init__(self.sprite_file)
        self.main = main
        self.player_number = player_number
        self.mass = BULLET_MASS
        self.damage = BULLET_DAMAGE
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

        self.angle = angle + BULLET_ROTATION_OFFSET
        self.body.angle = angle + BULLET_ROTATION_OFFSET

        self.dy = (math.cos(angle) * (BULLET_VELOCITY))
        self.dx = - (math.sin(angle) * (BULLET_VELOCITY))
        self.body.apply_force_at_world_point((self.dx, self.dy), (self.center_x, self.center_y))
        self.main.bullets.append(self)