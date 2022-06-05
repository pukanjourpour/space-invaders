from typing import Dict, List
from controllers.controller_level import ControllerLevel
from models.actor import Actor
from models.player import Player
from models.enemy_stage_1 import EnemyStage1
from models.enemy_stage_2 import EnemyStage2
from models.enemy_stage_3 import EnemyStage3
from models.enemy_bonus import EnemyBonus
from models.projectile import Projectile
from models.obstacle import Obstacle
from tkinter import filedialog as fd, messagebox, Tk
import json


class GameState(object):
    _INSTANCE = None
    _actors: List[Actor]
    _projectiles: List[Projectile]
    _obstacles: List[Obstacle]
    _level: int

    def __new__(cls, new_game: bool):
        if new_game:
            if cls._INSTANCE == None:
                cls._INSTANCE = super(GameState, cls).__new__(cls)
            cls._INSTANCE._level = 1
            new_actors, new_obstacles = ControllerLevel.generate_level(
                cls._INSTANCE._level
            )
            cls._INSTANCE._actors = new_actors
            cls._INSTANCE.projectiles = []
            cls._INSTANCE._obstacles = new_obstacles
        elif cls._INSTANCE == None:
            # initialize instance from json
            cls._INSTANCE = super(GameState, cls).__new__(cls)
            cls._load_from_json(cls)

        return cls._INSTANCE

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
    def obstacles(self) -> List[Actor]:
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

    def set_level(self, new_level: int) -> None:
        if 0 < new_level and new_level < 3:
            self._level = new_level
            new_actors, new_obstacles = ControllerLevel.generate_level(self._level)
            if self._level != 1:
                for actor in self._actors:
                    if isinstance(actor, Player):
                        new_actors.append(actor)
                        break

            self._actors = new_actors
            self._obstacles = new_obstacles
            self._projectiles = []

    def _convert_to_json_string(self) -> str:
        json_string = "{\n"

        enemy_stage_1_json = '"EnemyStage1": ['
        enemy_stage_2_json = '"EnemyStage2": ['
        enemy_stage_3_json = '"EnemyStage3": ['
        enemy_bonus_json = '"EnemyBonus": ['

        for actor in self._actors:
            if isinstance(actor, Player):
                json_string += '"Player": '
                json_string += actor.to_json()
                json_string += ",\n"
            elif isinstance(actor, EnemyStage1):
                enemy_stage_1_json += actor.to_json()
                enemy_stage_1_json += ",\n"
            elif isinstance(actor, EnemyStage2):
                enemy_stage_2_json += actor.to_json()
                enemy_stage_2_json += ",\n"
            elif isinstance(actor, EnemyStage3):
                enemy_stage_3_json += actor.to_json()
                enemy_stage_3_json += ",\n"
            elif isinstance(actor, EnemyBonus):
                enemy_bonus_json += actor.to_json()
                enemy_bonus_json += ",\n"

        if enemy_stage_1_json.endswith(","):
            enemy_stage_1_json = enemy_stage_1_json[:-1]
        if enemy_stage_2_json.endswith(","):
            enemy_stage_2_json = enemy_stage_2_json[:-1]
        if enemy_stage_3_json.endswith(","):
            enemy_stage_3_json = enemy_stage_3_json[:-1]
        if enemy_bonus_json.endswith(","):
            enemy_bonus_json = enemy_bonus_json[:-1]

        enemy_stage_1_json += "],\n"
        enemy_stage_2_json += "],\n"
        enemy_stage_3_json += "],\n"
        enemy_bonus_json += "],\n"

        json_string += (
            enemy_stage_1_json
            + enemy_stage_2_json
            + enemy_stage_3_json
            + enemy_bonus_json
        )

        json_string += '"' + Projectile.__name__ + '": ['
        for idx, projectile in enumerate(self._projectiles):
            json_string += projectile.to_json()
            if idx < len(self._projectiles) - 1:
                json_string += ","
            json_string += "\n"
        json_string += "],\n"

        json_string += '"' + Obstacle.__name__ + '": ['
        for idx, obstacle in enumerate(self._obstacles):
            json_string += obstacle.to_json()
            if idx < len(self._obstacles) - 1:
                json_string += ","
            json_string += "\n"
        json_string += "],\n"

        json_string += '"level": ' + str(self._level)

        json_string += "\n}"

        return json_string

    def save_to_json(self):
        directory_name: str = self._select_directory()
        full_path: str = directory_name + "/save1.json"
        json_string = self._convert_to_json_string()

        try:
            with open(full_path, "w", encoding="utf8") as f:
                f.write(json_string)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _load_from_json(cls):
        full_path = cls._select_file(cls)
        json_string: str = None

        try:
            with open(full_path, "r", encoding="utf8") as f:
                json_string = f.read()
                parsed_json = json.loads(json_string)

                new_actors: List[Actor] = []
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

                new_projectiles: List[Projectile] = []
                for idx in range(len(parsed_json["Projectile"])):
                    new_projectiles.append(
                        Projectile.from_dict(parsed_json["Projectile"][idx])
                    )

                new_obstacles: List[Obstacle] = []
                for idx in range(len(parsed_json["Obstacle"])):
                    new_obstacles.append(
                        Obstacle.from_dict(parsed_json["Obstacle"][idx])
                    )

                new_level: int = parsed_json["level"]

                cls._INSTANCE._actors = new_actors
                cls._INSTANCE._projectiles = new_projectiles
                cls._INSTANCE._obstacles = new_obstacles
                cls._INSTANCE._level = new_level
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _select_file(cls) -> str:
        Tk().withdraw()
        filename: str = fd.askopenfilename(
            title="Select a save file",
            filetypes=(("Json File", "*.json"),),
        )
        return filename

    def _select_directory(self) -> str:
        Tk().withdraw()
        directory_name: str = fd.askdirectory(title="Select folder to save game")
        return directory_name
