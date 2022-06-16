from pydantic.dataclasses import dataclass
from models.actor import Actor
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Player(Actor):
    pass
