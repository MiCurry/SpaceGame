import arcade

from SpaceGame.gametypes.Bullet import Bullet
from SpaceGame.gametypes.Explosion import ExplosionSize
from SpaceGame.gametypes.HealthBar import HealthBar
from SpaceGame.settings import SHIP_MASS, SHIP_FRICTION, SHIP_ELASTICITY, ALIVE, SHIP_SCALING, SHIP_STARTING_HITPOINTS, \
    DEAD


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
