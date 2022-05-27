from dataclasses import dataclass
from models.actor import Actor


@dataclass
class Player(Actor):
    _lives_count: int = 3

    @property
    def lives_count(self):
        return self.lives_count

    @lives_count.getter
    def lives_count(self, value):
        self._lives_count = value
