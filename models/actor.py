from dataclasses import dataclass


@dataclass
class Actor:
    textures: list[str]
    x_speed: int
    x_pos: int
    y_pos: int
    width: int
    height: int
