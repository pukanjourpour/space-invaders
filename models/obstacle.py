from pydantic.dataclasses import dataclass
from models.drawable import Drawable
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Obstacle(Drawable):
    _hit_count: int = 3

    @property
    def hit_count(self) -> int:
        return self._hit_count

    @hit_count.setter
    def hit_count(self, value) -> None:
        self._hit_count = value
