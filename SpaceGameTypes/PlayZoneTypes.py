from dataclasses import dataclass
from enum import Enum
from typing import Tuple

import arcade
import pymunk

@dataclass
class SpaceObjectData:
    spritefile: str
    health: int
    mass: float
    friction: float
    elasticit: float
    radius: float
    type: str
    scale: float
    
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
    def __init__(self, properties: SpaceObjectData):
                self._data = properties
                super().__init__(self._data.spritefile)

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

