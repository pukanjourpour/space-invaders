from dataclasses import dataclass
from actor import Actor

@dataclass
class Stage3Enemy(Actor):
    points: int
