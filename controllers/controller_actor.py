from cmath import e
from time import time
from typing import List, Sequence, Union
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
    @staticmethod
    def act(
        gamestate: GameState,
        inputs: Sequence[bool],
        delta_time: float,
    ):
        enemies: List[Actor] = []
        # current_time = time()
        for actor in gamestate.actors:
            if isinstance(actor, Player):
                if inputs[pygame.K_a]:
                    ControllerActor._move_player(actor, -1, delta_time)
                if inputs[pygame.K_d]:
                    ControllerActor._move_player(actor, 1, delta_time)

                if inputs[pygame.K_SPACE]:
                    ControllerActor._shoot(actor, gamestate)
            elif isinstance(actor, (EnemyStage1, EnemyStage2, EnemyStage3)):
                enemies.append(actor)
        ControllerActor._move_enemies(enemies, gamestate, delta_time)

    @staticmethod
    def _move_player(player: Player, direction: int, delta_time: float):
        new_player = player.x + Settings.PLAYER_SPEED * direction * delta_time
        if (
            new_player + player.width <= Settings.GAME_WINDOW_WIDTH - 10
            and new_player >= 10
        ):
            player.x = int(new_player)
        if new_player <= 10:
            player.x = 10
        if new_player + player.width >= Settings.GAME_WINDOW_WIDTH - 10:
            player.x = Settings.GAME_WINDOW_WIDTH - 10 - player.width

    @staticmethod
    def _move_enemies(enemies: List[Actor], gamestate: GameState, delta_time: float):
        current_time = time()
        if current_time - gamestate.enemy_last_movement_time >= 0.4:
            for enemy in enemies:
                if enemy.x <= 10:
                    enemy.x = 10
                    ControllerActor._change_enemies_direction(enemies)
                    break
                if enemy.x + enemy.width >= Settings.GAME_WINDOW_WIDTH - 10:
                    enemy.x = Settings.GAME_WINDOW_WIDTH - 10 - enemy.width
                    ControllerActor._change_enemies_direction(enemies)
                    break

            for enemy in enemies:
                new_enemy_x = enemy.x + enemy.speed * delta_time * enemy.direction
                enemy.x = int(new_enemy_x)

            gamestate.enemy_last_movement_time = current_time

    @staticmethod
    def _change_enemies_direction(enemies: List[Actor]):
        for enemy in enemies:
            enemy.direction *= -1

    @staticmethod
    def _shoot(player: Player, gamestate: GameState):
        current_time = time()
        if (
            current_time - gamestate.player_last_shot_time >= 0.5
            or gamestate.player_last_shot_time == 0
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
            gamestate.player_last_shot_time = current_time

    @staticmethod
    def receive_hit(actor: Actor, gamestate: GameState):
        if isinstance(actor, Player):
            actor.lives_count -= 1
            # TODO handle game over
        elif isinstance(actor, EnemyStage1):
            gamestate.score += 10
            gamestate.actors.remove(actor)
        elif isinstance(actor, EnemyStage2):
            gamestate.score += 50
            gamestate.actors.remove(actor)
        elif isinstance(actor, EnemyStage3):
            gamestate.score += 100
            gamestate.actors.remove(actor)
