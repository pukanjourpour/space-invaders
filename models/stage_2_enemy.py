from dataclasses import dataclass
from actor import Actor

@dataclass
class Stage2Enemy(Actor):
    points: int
    