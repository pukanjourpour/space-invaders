from dataclasses import dataclass
from models.drawable import Drawable


@dataclass
class Obstacle(Drawable):
    _hit_count: int = 0

    @property
    def hit_count(self):
        return self._hit_count

    @hit_count.setter
    def hit_count(self, value):
        self._hit_count = value
