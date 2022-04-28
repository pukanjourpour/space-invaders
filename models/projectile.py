from dataclasses import dataclass
from turtle import width


@dataclass
class Projectile:
    x_pos: int
    y_pos: int
    y_speed: int
    textures: list[str]
    width: int = 5
    height: int = 10

