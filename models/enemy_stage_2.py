from pydantic.dataclasses import dataclass
from models.actor import Actor
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class EnemyStage2(Actor):
    _direction: int

    @property
    def direction(self) -> int:
        return self._direction

    @direction.setter
    def direction(self, value: int) -> None:
        self._direction = value
