from dataclasses import dataclass
from models.drawable import Drawable


@dataclass
class Actor(Drawable):
    _speed: int

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value
