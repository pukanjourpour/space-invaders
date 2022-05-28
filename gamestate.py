from typing import List
from controllers.controller_level import ControllerLevel
from models.actor import Actor
from models.player import Player
from models.projectile import Projectile
from models.obstacle import Obstacle


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
            new_actors, new_obstacles = ControllerLevel.generate_level(cls._INSTANCE._level)
            cls._INSTANCE._actors = new_actors
            cls._INSTANCE.projectiles = []
            cls._INSTANCE._obstacles = new_obstacles
        elif cls._INSTANCE == None:
            # initialize instance from json
            cls._load_from_json()

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

    def save_to_json(self):
        pass

    def _load_from_json(self):
        pass
