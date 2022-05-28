from pydantic.dataclasses import dataclass
from models.drawable import Drawable
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Actor(Drawable):
    _speed: int

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, value) -> None:
        self._speed = value
