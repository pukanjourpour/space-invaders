from typing import List, Tuple

from models.actor import Actor
from models.enemy_stage_1 import EnemyStage1
from models.obstacle import Obstacle
from models.player import Player
from settings import Settings


class ControllerLevel:
    @staticmethod
    def generate_level(level: int) -> Tuple[List[Actor], List[Obstacle]]:
        if level == 1:
            player: Player = Player(
                Settings.SCREEN_WIDTH / 2 - 25,
                Settings.SCREEN_HEIGHT - 70,
                50,
                50,
                Settings.PLAYER_SPEED,
            )
            # testing
            enemy: EnemyStage1 = EnemyStage1(
                Settings.SCREEN_WIDTH / 2 - 25, 30, 50, 50, Settings.PLAYER_SPEED, 1
            )
        actors: List[Actor] = [player, enemy]
        obstacles: List[Obstacle] = [
            Obstacle(
                Settings.SCREEN_WIDTH / 2 - 25, Settings.SCREEN_HEIGHT - 150, 50, 50
            )
        ]

        return actors, obstacles
