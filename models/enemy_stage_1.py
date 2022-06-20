from pydantic.dataclasses import dataclass
from dataclasses_json import dataclass_json
from models.enemy_basic import EnemyBasic


@dataclass_json
@dataclass
class EnemyStage1(EnemyBasic):
    pass
