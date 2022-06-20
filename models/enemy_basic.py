from pydantic.dataclasses import dataclass
from models.actor import Actor
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class EnemyBasic(Actor):
    _direction: int
    _can_shoot: bool

    @property
    def direction(self) -> int:
        return self._direction

    @direction.setter
    def direction(self, value: int) -> None:
        self._direction = value

    @property
    def can_shoot(self) -> bool:
        return self._can_shoot

    @can_shoot.setter
    def can_shoot(self, value: bool) -> None:
        self._can_shoot = value
