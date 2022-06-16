from dataclasses import dataclass
import json
from typing import List
from dataclasses_json import DataClassJsonMixin
from models.actor import Actor
from models.player import Player
from models.enemy_stage_1 import EnemyStage1
from models.enemy_stage_2 import EnemyStage2
from models.enemy_stage_3 import EnemyStage3
from models.enemy_bonus import EnemyBonus
from models.projectile import Projectile
from models.obstacle import Obstacle


@dataclass
class GameState(DataClassJsonMixin):
    _actors: List[Actor]
    _projectiles: List[Projectile]
    _obstacles: List[Obstacle]
    _level: int
    _lives_count: int = 3
    _score: int = 0
    _player_last_shot_time: float = 0
    _enemy_last_movement_time: float = 0

    @property
    def actors(self) -> List[Actor]:
        return self._actors

    @actors.setter
    def actors(self, value: List[Actor]) -> None:
        self._actors = value

    @property
    def projectiles(self) -> List[Projectile]:
        return self._projectiles

    @projectiles.setter
    def projectiles(self, value: List[Projectile]) -> None:
        self._projectiles = value

    @property
    def obstacles(self) -> List[Obstacle]:
        return self._obstacles

    @obstacles.setter
    def obstacles(self, value: List[Obstacle]) -> None:
        self._obstacles = value

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        self._level = value

    @property
    def lives_count(self) -> int:
        return self._lives_count

    @lives_count.setter
    def lives_count(self, value) -> None:
        self._lives_count = value

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        self._score = value

    @property
    def player_last_shot_time(self) -> float:
        return self._player_last_shot_time

    @player_last_shot_time.setter
    def player_last_shot_time(self, value: float) -> None:
        self._player_last_shot_time = value

    @property
    def enemy_last_movement_time(self) -> float:
        return self._enemy_last_movement_time

    @enemy_last_movement_time.setter
    def enemy_last_movement_time(self, value: float) -> None:
        self._enemy_last_movement_time = value

    def to_json(self) -> str:
        json_string = "{"

        enemy_stage_1_json = '"EnemyStage1":['
        enemy_stage_2_json = '"EnemyStage2":['
        enemy_stage_3_json = '"EnemyStage3":['
        enemy_bonus_json = '"EnemyBonus":['

        for actor in self._actors:
            if isinstance(actor, Player):
                json_string += '"Player":'
                json_string += actor.to_json()
                json_string += ","
            elif isinstance(actor, EnemyStage1):
                enemy_stage_1_json += actor.to_json()
                enemy_stage_1_json += ","
            elif isinstance(actor, EnemyStage2):
                enemy_stage_2_json += actor.to_json()
                enemy_stage_2_json += ","
            elif isinstance(actor, EnemyStage3):
                enemy_stage_3_json += actor.to_json()
                enemy_stage_3_json += ","
            elif isinstance(actor, EnemyBonus):
                enemy_bonus_json += actor.to_json()
                enemy_bonus_json += ","

        if enemy_stage_1_json.endswith(","):
            enemy_stage_1_json = enemy_stage_1_json[:-1]
        if enemy_stage_2_json.endswith(","):
            enemy_stage_2_json = enemy_stage_2_json[:-1]
        if enemy_stage_3_json.endswith(","):
            enemy_stage_3_json = enemy_stage_3_json[:-1]
        if enemy_bonus_json.endswith(","):
            enemy_bonus_json = enemy_bonus_json[:-1]

        enemy_stage_1_json += "],"
        enemy_stage_2_json += "],"
        enemy_stage_3_json += "],"
        enemy_bonus_json += "],"

        json_string += (
            enemy_stage_1_json
            + enemy_stage_2_json
            + enemy_stage_3_json
            + enemy_bonus_json
        )

        json_string += '"' + Projectile.__name__ + '":['
        for idx, projectile in enumerate(self._projectiles):
            json_string += projectile.to_json()
            if idx < len(self._projectiles) - 1:
                json_string += ","
            json_string += ""
        json_string += "],"

        json_string += '"' + Obstacle.__name__ + '":['
        for idx, obstacle in enumerate(self._obstacles):
            json_string += obstacle.to_json()
            if idx < len(self._obstacles) - 1:
                json_string += ","
            json_string += ""
        json_string += "],"

        json_string += '"level":' + str(self._level) + ","
        json_string += '"lives_count":' + str(self._lives_count) + ","
        json_string += '"score":' + str(self._score) + ","
        json_string += (
            '"player_last_shot_time":' + str(self._player_last_shot_time) + ","
        )
        json_string += '"enemy_last_movement_time":' + str(
            self._enemy_last_movement_time
        )

        json_string += "}"

        return json_string

    @classmethod
    def from_json(cls, json_string: str):
        parsed_json = json.loads(json_string)

        new_actors: List[Actor] = []
        new_projectiles: List[Projectile] = []
        new_obstacles: List[Obstacle] = []

        player: Player = Player.from_dict(parsed_json["Player"])
        new_actors.append(player)

        for idx in range(len(parsed_json["EnemyStage1"])):
            enemy: EnemyStage1 = EnemyStage1.from_dict(parsed_json["EnemyStage1"][idx])
            new_actors.append(enemy)

        for idx in range(len(parsed_json["EnemyStage2"])):
            enemy: EnemyStage2 = EnemyStage2.from_dict(parsed_json["EnemyStage2"][idx])
            new_actors.append(enemy)

        for idx in range(len(parsed_json["EnemyStage3"])):
            enemy: EnemyStage3 = EnemyStage3.from_dict(parsed_json["EnemyStage3"][idx])
            new_actors.append(enemy)

        for idx in range(len(parsed_json["EnemyBonus"])):
            enemy: EnemyBonus = EnemyBonus.from_dict(parsed_json["EnemyBonus"][idx])
            new_actors.append(enemy)

        for idx in range(len(parsed_json["Projectile"])):
            new_projectiles.append(Projectile.from_dict(parsed_json["Projectile"][idx]))

        for idx in range(len(parsed_json["Obstacle"])):
            new_obstacles.append(Obstacle.from_dict(parsed_json["Obstacle"][idx]))

        new_level: int = parsed_json["level"]
        new_lives_count: int = parsed_json["lives_count"]
        new_score: int = parsed_json["score"]
        new_player_last_shot_time: int = parsed_json["player_last_shot_time"]
        new_enemy_last_movement_time: int = parsed_json["enemy_last_movement_time"]

        return cls(
            new_actors,
            new_projectiles,
            new_obstacles,
            new_level,
            new_lives_count,
            new_score,
            new_player_last_shot_time,
            new_enemy_last_movement_time,
        )
