from typing import List, Tuple

from models.actor import Actor
from models.enemy_stage_1 import EnemyStage1
from models.enemy_stage_2 import EnemyStage2
from models.enemy_stage_3 import EnemyStage3
from models.obstacle import Obstacle
from models.player import Player
from settings import Settings


class ControllerLevel:
    @staticmethod
    def generate_level(level: int) -> Tuple[List[Actor], List[Obstacle]]:
        actors: List[Actor] = []
        obstacles: List[Obstacle] = []

        if level == 1:
            col_count = 3
            player: Player = Player(
                Settings.GAME_WINDOW_WIDTH / 2 - Settings.ACTOR_WIDTH / 2,
                Settings.GAME_WINDOW_HEIGHT - 70,
                Settings.ACTOR_WIDTH,
                Settings.ACTOR_HEIGHT,
                Settings.PLAYER_SPEED,
            )
            actors.append(player)
            for r in range(3):
                for c in range(col_count + r):
                    if r == 0:
                        enemy: EnemyStage3 = EnemyStage3(
                            int(
                                (Settings.GAME_WINDOW_WIDTH / (col_count + r)) * c
                                + Settings.GAME_WINDOW_WIDTH / ((col_count + r) * 2)
                                - Settings.ACTOR_WIDTH / 2
                            ),
                            100,
                            Settings.ACTOR_WIDTH,
                            Settings.ACTOR_HEIGHT,
                            Settings.BASIC_ENEMY_SPEED,
                            1,
                        )
                        actors.append(enemy)

                    if r == 1:
                        enemy: EnemyStage2 = EnemyStage2(
                            int(
                                (Settings.GAME_WINDOW_WIDTH / (col_count + r)) * c
                                + Settings.GAME_WINDOW_WIDTH / ((col_count + r) * 2)
                                - Settings.ACTOR_WIDTH / 2
                            ),
                            180,
                            Settings.ACTOR_WIDTH,
                            Settings.ACTOR_HEIGHT,
                            Settings.BASIC_ENEMY_SPEED,
                            1,
                        )
                        actors.append(enemy)

                    if r == 2:
                        enemy: EnemyStage1 = EnemyStage1(
                            int(
                                (Settings.GAME_WINDOW_WIDTH / (col_count + r)) * c
                                + Settings.GAME_WINDOW_WIDTH / ((col_count + r) * 2)
                                - Settings.ACTOR_WIDTH / 2
                            ),
                            260,
                            Settings.ACTOR_WIDTH,
                            Settings.ACTOR_HEIGHT,
                            Settings.BASIC_ENEMY_SPEED,
                            1,
                        )
                        actors.append(enemy)

            for r in range(3):
                obstacle: Obstacle = Obstacle(
                    int(
                        (Settings.GAME_WINDOW_WIDTH / 3) * r
                        + Settings.GAME_WINDOW_WIDTH / 6
                        - 35
                    ),
                    Settings.SCREEN_HEIGHT - 200,
                    Settings.OBSTACLE_WIDTH,
                    Settings.OBSTACLE_HEIGHT,
                )
                obstacles.append(obstacle)

        return actors, obstacles
