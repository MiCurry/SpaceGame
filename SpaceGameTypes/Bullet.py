from SpaceGameTypes.SpaceGameTypes import CollisionTypes
import arcade
import math

BULLET_MASS = 0.005
BULLET_FRICTION = 0.0
BULLET_VELOCITY = 500.0
BULLET_ROTATION_OFFSET = math.pi / 2.0
BULLET_SPAWN_OFFSET = 65.0
BULLET_DAMAGE = 1

class Bullet(arcade.Sprite):
    def __init__(self, main, start_position, angle, start_dx, start_dy, creator, spawn_offset=BULLET_SPAWN_OFFSET):
        self.sprite_file = "./resources/png/sprites/Lasers/laserBlue01.png"
        super().__init__(self.sprite_file)
        self.main = main
        self.creator = creator 
        self.mass = BULLET_MASS
        self.damage = BULLET_DAMAGE
        self.friction = BULLET_FRICTION
        self.center_x = start_position[0] + spawn_offset * math.cos(angle + BULLET_ROTATION_OFFSET)
        self.center_y = start_position[1] + spawn_offset * math.sin(angle + BULLET_ROTATION_OFFSET)
        self.main.physics_engine.add_sprite(self,
                                friction=self.friction,
                                mass=self.mass,
                                moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                collision_type=CollisionTypes.BULLET.value)

        self.body = self.main.physics_engine.get_physics_object(self).body
        self.shape = self.main.physics_engine.get_physics_object(self).shape

        self.angle = angle
        self.body.angle = angle

        self.dy = (math.cos(angle) * (BULLET_VELOCITY))
        self.dx = - (math.sin(angle) * (BULLET_VELOCITY))
        self.body.apply_force_at_world_point((self.dx, self.dy), (self.center_x, self.center_y))

        self.main.bullets.append(self)

    def update(self):
        # This should be a collision handler, but for now just remove
        # it when it gets close to the edges
        if (self.center_y < 29.0 or self.center_y > 4065.0
                or self.center_x < 29.0 or self.center_x > 4065.0):
            self.remove_from_sprite_lists()
