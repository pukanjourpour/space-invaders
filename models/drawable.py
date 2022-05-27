from dataclasses import dataclass


@dataclass
class Drawable:
    _x: int
    _y: int
    _width: int
    _height: int

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @x.setter
    def height(self, value):
        self._height = value
