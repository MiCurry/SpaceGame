import copy
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from PIL import Image
import arcade
import pymunk

from SpaceGame.gametypes.Explosion import ExplosionSize

__all__ = [
    "SpaceObjectData",
    "Background",
    "Wall",
    "SpaceObject",
    "CollisionTypes"
]


@dataclass
class SpaceObjectData:
    spritefile: str
    health: int
    mass: float
    friction: float
    elasticity: float
    radius: float
    type: str
    scale: float
    score: int


@dataclass
class Background:
    image: str
    width: float
    height: float
    scale: float


class Wall:
    def __init__(self,
                 start: Tuple[float, float],
                 end: Tuple[float, float],
                 radius=1.0,
                 friction=0.9,
                 elasticity=0.9):
        self.segment = pymunk.Segment(pymunk.Body(body_type=pymunk.Body.STATIC),
                                      start,
                                      end,
                                      radius)
        self.segment.friction = friction
        self.segment.elasticity = elasticity


class SpaceObject(arcade.Sprite):
    def __init__(self, properties: SpaceObjectData, main):
        self.shape = None
        self._data = copy.deepcopy(properties)
        self.main = main
        self.body = None
        width, height = self._calulate_sprite_dims(self._data.spritefile)
        super().__init__(self._data.spritefile,
                         hit_box_algorithm=arcade.hitbox.PymunkHitBoxAlgorithm(detail=10.0),
                         width=width,
                         height=height,
                         scale=self._data.scale)
        self.sync_hit_box_to_texture()

    def _calulate_sprite_dims(self, spritefile):
        image = Image.open(arcade.resources.resolve(spritefile))
        width = image.width
        height = image.height
        image.close()
        return width, height

    def setup(self):
        self.main.add_sprite_to_pymunk(self,
                                       moment_of_inertia=pymunk.moment_for_box(self.mass, (self.width, self.height)))
        self.body = self.main.physics_engine.get_physics_object(self).body
        self.shape = self.main.physics_engine.get_physics_object(self).shape

    def update(self, delta):
        if self.health <= 0:
            self.explode()

    def damage(self, bullet):
        self._data.health -= bullet.damage
        self.last_hit_by = bullet.creator

    def explode(self):
        self.remove_from_sprite_lists()
        self.main.add_explosion(self.position, ExplosionSize.NORMAL)
        self.main.scoreboard.add_score(self.last_hit_by, self.score)

    @property
    def score(self) -> int:
        return self._data.score

    @property
    def health(self) -> int:
        return self._data.health

    @property
    def spritefile(self) -> str:
        return self._data.spritefile

    @property
    def mass(self) -> float:
        return self._data.mass

    @property
    def friction(self) -> float:
        return self._data.friction

    @property
    def elasticity(self) -> float:
        return self._data.elasticity

    @property
    def scale(self) -> float:
        return self._data.scale

    @property
    def type(self) -> str:
        return self._data.type


class CollisionTypes(Enum):
    SHIP = "SHIP"
    BULLET = "BULLET"
    SPACE_JUNK = "SPACEJUNK"
    ASTROID = "ASTROID"
    UFO = "UFO"
    BUG = "BUG"
