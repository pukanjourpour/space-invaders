from dataclasses import dataclass
from actor import Actor

@dataclass
class Stage1Enemy(Actor):
    __points: int = 30
    
    