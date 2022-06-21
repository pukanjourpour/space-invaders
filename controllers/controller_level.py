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
    def generate_level(level: int) -> Tuple[List[Actor], List[Obstacle], int, float, float, float]:
        actors: List[Actor] = []
        obstacles: List[Obstacle] = []
        enemy_count = 0
        enemy_x_movement_timeout: float = 0
        enemy_y_movement_timeout: float = 0
        enemy_shoot_timeout: float = 0

        if level == 1:
            player: Player = Player(
                Settings.GAME_WINDOW_WIDTH / 2 - Settings.PLAYER_WIDTH / 2,
                Settings.GAME_WINDOW_HEIGHT - 70,
                Settings.PLAYER_WIDTH,
                Settings.PLAYER_HEIGHT,
                Settings.PLAYER_SPEED,
            )
            actors.append(player)
            for r in range(3):
                for c in range(Settings.ENEMY_COLUMN_COUNT):
                    if r == 0:
                        enemy: EnemyStage3 = EnemyStage3(
                            int(
                                Settings.GAME_WINDOW_PADDING
                                + (
                                    (Settings.GAME_WINDOW_WIDTH - Settings.GAME_WINDOW_PADDING * 2)
                                    / Settings.ENEMY_COLUMN_COUNT
                                )
                                * c
                                + Settings.GAME_WINDOW_WIDTH
                                / (Settings.ENEMY_COLUMN_COUNT * 2)
                                - Settings.BASIC_ENEMY_WIDTH / 2
                            ),
                            100,
                            Settings.BASIC_ENEMY_WIDTH,
                            Settings.BASIC_ENEMY_HEIGHT,
                            Settings.BASIC_ENEMY_SPEED,
                            1,
                            False,
                        )
                        enemy_count += 1
                        actors.append(enemy)

                    if r == 1:
                        enemy: EnemyStage2 = EnemyStage2(
                            int(
                                Settings.GAME_WINDOW_PADDING
                                + (
                                    (Settings.GAME_WINDOW_WIDTH - Settings.GAME_WINDOW_PADDING * 2)
                                    / Settings.ENEMY_COLUMN_COUNT
                                )
                                * c
                                + Settings.GAME_WINDOW_WIDTH
                                / (Settings.ENEMY_COLUMN_COUNT * 2)
                                - Settings.BASIC_ENEMY_WIDTH / 2
                            ),
                            180,
                            Settings.BASIC_ENEMY_WIDTH,
                            Settings.BASIC_ENEMY_HEIGHT,
                            Settings.BASIC_ENEMY_SPEED,
                            1,
                            False,
                        )
                        enemy_count += 1
                        actors.append(enemy)

                    if r == 2:
                        enemy: EnemyStage1 = EnemyStage1(
                            int(
                                Settings.GAME_WINDOW_PADDING
                                + (
                                    (Settings.GAME_WINDOW_WIDTH - Settings.GAME_WINDOW_PADDING * 2)
                                    / Settings.ENEMY_COLUMN_COUNT
                                )
                                * c
                                + Settings.GAME_WINDOW_WIDTH
                                / (Settings.ENEMY_COLUMN_COUNT * 2)
                                - Settings.BASIC_ENEMY_WIDTH / 2
                            ),
                            260,
                            Settings.BASIC_ENEMY_WIDTH,
                            Settings.BASIC_ENEMY_HEIGHT,
                            Settings.BASIC_ENEMY_SPEED,
                            1,
                            True,
                        )
                        enemy_count += 1
                        actors.append(enemy)

            for c in range(4):
                obstacle: Obstacle = Obstacle(
                    int(
                        ((Settings.GAME_WINDOW_WIDTH - Settings.GAME_WINDOW_PADDING * 2) / 4) * c
                        + Settings.GAME_WINDOW_WIDTH / 8
                        - Settings.OBSTACLE_WIDTH / 2
                    ),
                    Settings.SCREEN_HEIGHT - 200,
                    Settings.OBSTACLE_WIDTH,
                    Settings.OBSTACLE_HEIGHT,
                )
                obstacles.append(obstacle)
            enemy_x_movement_timeout = 0.4
            enemy_y_movement_timeout = 3
            enemy_shoot_timeout = 0.4
        
        elif level == 2:
            for r in range(4):
                for c in range(Settings.ENEMY_COLUMN_COUNT):
                    if r == 0:
                        enemy: EnemyStage3 = EnemyStage3(
                            int(
                                Settings.GAME_WINDOW_PADDING
                                + (
                                    (Settings.GAME_WINDOW_WIDTH - Settings.GAME_WINDOW_PADDING * 2)
                                    / Settings.ENEMY_COLUMN_COUNT
                                )
                                * c
                                + Settings.GAME_WINDOW_WIDTH
                                / (Settings.ENEMY_COLUMN_COUNT * 2)
                                - Settings.BASIC_ENEMY_WIDTH / 2
                            ),
                            100,
                            Settings.BASIC_ENEMY_WIDTH,
                            Settings.BASIC_ENEMY_HEIGHT,
                            Settings.BASIC_ENEMY_SPEED,
                            1,
                            False,
                        )
                        enemy_count += 1
                        actors.append(enemy)

                    if r == 1:
                        enemy: EnemyStage2 = EnemyStage2(
                            int(
                                Settings.GAME_WINDOW_PADDING
                                + (
                                    (Settings.GAME_WINDOW_WIDTH - Settings.GAME_WINDOW_PADDING * 2)
                                    / Settings.ENEMY_COLUMN_COUNT
                                )
                                * c
                                + Settings.GAME_WINDOW_WIDTH
                                / (Settings.ENEMY_COLUMN_COUNT * 2)
                                - Settings.BASIC_ENEMY_WIDTH / 2
                            ),
                            180,
                            Settings.BASIC_ENEMY_WIDTH,
                            Settings.BASIC_ENEMY_HEIGHT,
                            Settings.BASIC_ENEMY_SPEED,
                            1,
                            False,
                        )
                        enemy_count += 1
                        actors.append(enemy)

                    if r == 2:
                        enemy: EnemyStage2 = EnemyStage2(
                            int(
                                Settings.GAME_WINDOW_PADDING
                                + (
                                    (Settings.GAME_WINDOW_WIDTH - Settings.GAME_WINDOW_PADDING * 2)
                                    / Settings.ENEMY_COLUMN_COUNT
                                )
                                * c
                                + Settings.GAME_WINDOW_WIDTH
                                / (Settings.ENEMY_COLUMN_COUNT * 2)
                                - Settings.BASIC_ENEMY_WIDTH / 2
                            ),
                            260,
                            Settings.BASIC_ENEMY_WIDTH,
                            Settings.BASIC_ENEMY_HEIGHT,
                            Settings.BASIC_ENEMY_SPEED,
                            1,
                            False,
                        )
                        enemy_count += 1
                        actors.append(enemy)
                    if r == 3:
                        enemy: EnemyStage1 = EnemyStage1(
                            int(
                                Settings.GAME_WINDOW_PADDING
                                + (
                                    (Settings.GAME_WINDOW_WIDTH - Settings.GAME_WINDOW_PADDING * 2)
                                    / Settings.ENEMY_COLUMN_COUNT
                                )
                                * c
                                + Settings.GAME_WINDOW_WIDTH
                                / (Settings.ENEMY_COLUMN_COUNT * 2)
                                - Settings.BASIC_ENEMY_WIDTH / 2
                            ),
                            340,
                            Settings.BASIC_ENEMY_WIDTH,
                            Settings.BASIC_ENEMY_HEIGHT,
                            Settings.BASIC_ENEMY_SPEED,
                            1,
                            True,
                        )
                        enemy_count += 1
                        actors.append(enemy)


            for c in range(3):
                obstacle: Obstacle = Obstacle(
                    int(
                        ((Settings.GAME_WINDOW_WIDTH - Settings.GAME_WINDOW_PADDING * 2) / 3) * c
                        + Settings.GAME_WINDOW_WIDTH / 6
                        - Settings.OBSTACLE_WIDTH / 2
                    ),
                    Settings.SCREEN_HEIGHT - 200,
                    Settings.OBSTACLE_WIDTH,
                    Settings.OBSTACLE_HEIGHT,
                )
                obstacles.append(obstacle)
            enemy_x_movement_timeout = 0.3
            enemy_y_movement_timeout = 2.5
            enemy_shoot_timeout = 0.25

        return actors, obstacles, enemy_count, enemy_x_movement_timeout, enemy_y_movement_timeout, enemy_shoot_timeout
