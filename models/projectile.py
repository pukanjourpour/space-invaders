from pydantic.dataclasses import dataclass
from models.drawable import Drawable
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Projectile(Drawable):
    _speed: int
    _direction: int

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, value) -> None:
        self._speed = value

    @property
    def direction(self) -> int:
        return self._direction

    @direction.setter
    def direction(self, value) -> None:
        self._direction = value
