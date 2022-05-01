from dataclasses import dataclass
from turtle import width
from typing import Tuple


@dataclass
class Projectile:
    __x_pos: int
    __y_pos: int
    __y_speed: int
    __textures: list[str]
    __width: int = 5
    __height: int = 10

    def move(self) -> None:
        self.__y_pos += self.__y_speed

    def get_x_pos(self) -> int:
        return self.__x_pos

    def set_x_pos(self, x_pos) -> None:
        self.__x_pos = x_pos

    def get_y_pos(self) -> int:
        return self.__y_pos

    def set_y_pos(self, y_pos) -> None:
        self.__y_pos = y_pos

    def get_rectangle(self) -> tuple[int,int,int,int]:
        return (self.__x_pos, self.__y_pos, self.__width, self.__height)