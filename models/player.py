from pydantic.dataclasses import dataclass
from models.actor import Actor
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Player(Actor):
    _lives_count: int = 3
    _score: int = 0

    @property
    def lives_count(self) -> int:
        return self._lives_count

    @lives_count.getter
    def lives_count(self, value) -> None:
        self._lives_count = value

    @property
    def score(self) -> int:
        return self._score

    @score.getter
    def score(self, value) -> None:
        self._score = value
