from dataclasses import dataclass
from actor import Actor

@dataclass
class BonusEnemy(Actor):
    points: int