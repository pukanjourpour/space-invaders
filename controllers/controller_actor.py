from time import time
from typing import List, Sequence

import pygame
from gamestate import GameState

from models.actor import Actor
from models.enemy_stage_1 import EnemyStage1
from models.enemy_stage_2 import EnemyStage2
from models.enemy_stage_3 import EnemyStage3
from models.enemy_bonus import EnemyBonus
from models.player import Player
from models.projectile import Projectile
from settings import Settings


class ControllerActor:
    _last_shot_time: float = 0

    @staticmethod
    def act(
        actors: List[Actor],
        inputs: Sequence[bool],
        gamestate: GameState,
        delta_time: float,
    ):
        player: Player = None
        enemies: List[Actor] = []

        for actor in actors:
            if isinstance(actor, Player):
                if inputs[pygame.K_a]:
                    ControllerActor._move(actor, -1, delta_time)
                if inputs[pygame.K_d]:
                    ControllerActor._move(actor, 1, delta_time)

                if inputs[pygame.K_SPACE]:
                    ControllerActor._shoot(actor, gamestate)
            else:
                enemies.append(actor)

    @staticmethod
    def _move(player: Player, direction: int, delta_time: float):
        new_player_x = player.x + Settings.PLAYER_SPEED * direction * delta_time
        if (
            new_player_x + player.width <= Settings.SCREEN_WIDTH - 10
            and new_player_x >= 10
        ):
            player.x = int(new_player_x)
        if new_player_x <= 10:
            player.x = 10
        if new_player_x + player.width >= Settings.SCREEN_WIDTH - 10:
            player.x = Settings.SCREEN_WIDTH - 10 - player.width

    @staticmethod
    def _shoot(player: Player, gamestate: GameState):
        current_time = time()
        if (
            current_time - ControllerActor._last_shot_time >= 0.5
            or ControllerActor._last_shot_time == 0
        ):
            projectile = Projectile(
                int(player.x + player.width / 2 - Settings.PROJECTILE_WIDTH / 2),
                player.y,
                Settings.PROJECTILE_WIDTH,
                Settings.PROJECTILE_HEIGHT,
                Settings.PROJECTILE_SPEED,
                -1,
            )
            gamestate.projectiles.append(projectile)
            ControllerActor._last_shot_time = current_time
