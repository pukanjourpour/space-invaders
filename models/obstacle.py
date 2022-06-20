from pydantic.dataclasses import dataclass
from models.drawable import Drawable
from dataclasses_json import dataclass_json

from settings import Settings


@dataclass_json
@dataclass
class Obstacle(Drawable):
    _hit_count: int = Settings.OBSTACLE_HIT_COUNT

    @property
    def hit_count(self) -> int:
        return self._hit_count

    @hit_count.setter
    def hit_count(self, value) -> None:
        self._hit_count = value
