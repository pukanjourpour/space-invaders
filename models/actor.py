from dataclasses import dataclass


@dataclass
class Actor:
    __x_pos: int
    __y_pos: int
    __x_speed: int
    __textures: list[str]
    __width: int = 50
    __height: int = 30

    def get_rectangle(self) -> tuple[int,int,int,int]:
        return (self.__x_pos, self.__y_pos, self.__width, self.__height)

    def move(self, direction: int) -> None:
        self.__x_pos += self.__x_speed * direction

    def get_x_pos(self) -> int:
        return self.__x_pos

    def set_x_pos(self, x_pos) -> None:
        self.__x_pos = x_pos

    def get_y_pos(self) -> int:
        return self.__y_pos

    def set_y_pos(self, y_pos) -> None:
        self.__y_pos = y_pos

    def get_width(self) -> int:
        return self.__width
    
    def set_width(self, width) -> None:
        self.__width = width

    def get_x_speed(self) -> int:
        return self.__x_speed
