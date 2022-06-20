from random import randint, random, choice
from time import time
from typing import List, Sequence
import pygame
from gamestate import GameState

from models.actor import Actor
from models.enemy_basic import EnemyBasic
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
        enemies: List[EnemyBasic] = []
        # current_time = time()
        for actor in gamestate.actors:
            if actor:
                if isinstance(actor, Player):
                    if inputs[pygame.K_a]:
                        ControllerActor._move_player(actor, -1, delta_time)
                    if inputs[pygame.K_d]:
                        ControllerActor._move_player(actor, 1, delta_time)
                    if inputs[pygame.K_SPACE]:
                        ControllerActor._shoot_player(actor, gamestate)
                elif isinstance(actor, EnemyBasic):
                    enemies.append(actor)
        ControllerActor._move_enemies(enemies, gamestate, delta_time)
        ControllerActor._shoot_enemies(enemies, gamestate)

    @staticmethod
    def _move_player(player: Player, direction: int, delta_time: float):
        new_player = player.x + Settings.PLAYER_SPEED * direction * delta_time
        if (
            new_player + player.width <= Settings.GAME_WINDOW_WIDTH -  Settings.GAME_WINDOW_PADDING
            and new_player >=  Settings.GAME_WINDOW_PADDING
        ):
            player.x = int(new_player)
        if new_player <=  Settings.GAME_WINDOW_PADDING:
            player.x = Settings.GAME_WINDOW_PADDING
        if new_player + player.width >= Settings.GAME_WINDOW_WIDTH -  Settings.GAME_WINDOW_PADDING:
            player.x = Settings.GAME_WINDOW_WIDTH - Settings.GAME_WINDOW_PADDING - player.width

    @staticmethod
    def _move_enemies(enemies: List[EnemyBasic], gamestate: GameState, delta_time: float):
        current_time = time()
        change_dir: bool = False
        pixels_past_border: int = 0
        can_move_y = True
        moved_x = False
        moved_y = False
        for enemy in enemies:
            if enemy.x <  Settings.GAME_WINDOW_PADDING:
                new_pixels_past_border =  Settings.GAME_WINDOW_PADDING - enemy.x
                if new_pixels_past_border > pixels_past_border:
                    pixels_past_border = new_pixels_past_border
                change_dir = True
            elif enemy.x + enemy.width > Settings.GAME_WINDOW_WIDTH -  Settings.GAME_WINDOW_PADDING:
                new_pixels_past_border = Settings.GAME_WINDOW_WIDTH -  Settings.GAME_WINDOW_PADDING - enemy.x - enemy.width
                if new_pixels_past_border < pixels_past_border:
                    pixels_past_border = new_pixels_past_border
                change_dir = True
            if enemy.y + enemy.height > Settings.GAME_WINDOW_HEIGHT - 230:
                can_move_y = False

        if change_dir:
            for enemy in enemies:
                enemy.direction *= -1
                new_enemy_x = enemy.x + pixels_past_border 
                enemy.x = int(new_enemy_x)
        else:
            for enemy in enemies:
                if current_time - gamestate.enemy_last_x_movement_time >= gamestate.enemy_x_movement_timeout:
                    new_enemy_x = enemy.x + enemy.speed * delta_time * enemy.direction
                    enemy.x = int(new_enemy_x)
                    moved_x = True
                if can_move_y and current_time - gamestate.enemy_last_y_movement_time >= gamestate.enemy_y_movement_timeout:
                    new_enemy_y = enemy.y + enemy.speed * delta_time
                    enemy.y = int(new_enemy_y) 
                    moved_y = True           
        if moved_x:
            gamestate.enemy_last_x_movement_time = current_time
        if moved_y:
            gamestate.enemy_last_y_movement_time = current_time

    @staticmethod
    def _shoot_player(player: Player, gamestate: GameState):
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
                Settings.PROJECTILE_SPEED_PLAYER,
                -1,
            )
            gamestate.projectiles.append(projectile)
            gamestate.player_last_shot_time = current_time

    @staticmethod
    def _shoot_enemies(enemies: List[EnemyBasic], gamestate: GameState):
        enemy = choice(enemies)
        current_time = time()
        if enemy and enemy.can_shoot:
            projectile = Projectile(
            int(enemy.x + enemy.width / 2 - Settings.PROJECTILE_WIDTH / 2),
            enemy.y + enemy.height,
            Settings.PROJECTILE_WIDTH,
            Settings.PROJECTILE_HEIGHT,
            Settings.PROJECTILE_SPEED_ENEMY,
            1,
            )
            if isinstance(enemy, EnemyStage1):
                if current_time - gamestate.enemy_last_shot_time >= gamestate.enemy_shoot_timeout and random() <= 0.1:
                    gamestate.projectiles.append(projectile)
                    gamestate.enemy_last_shot_time = current_time
            elif isinstance(enemy, EnemyStage2):
                if current_time - gamestate.enemy_last_shot_time >= gamestate.enemy_shoot_timeout - gamestate.enemy_shoot_timeout / 3 and  random() <= 0.2:
                    gamestate.projectiles.append(projectile)
                    gamestate.enemy_last_shot_time = current_time
            elif isinstance(enemy, EnemyStage3):
                if current_time - gamestate.enemy_last_shot_time >= gamestate.enemy_shoot_timeout - gamestate.enemy_shoot_timeout / 2 and random() <= 0.3:
                    gamestate.projectiles.append(projectile)
                    gamestate.enemy_last_shot_time = current_time

    @staticmethod
    def receive_hit(actor: Actor, gamestate: GameState):
        if isinstance(actor, Player):
            gamestate.lives_count -= 1
            if gamestate.lives_count == 0:
                gamestate.game_over = True
        elif isinstance(actor, EnemyBasic):
            idx = gamestate.actors.index(actor)
            if idx > Settings.ENEMY_COLUMN_COUNT:
                next_enemy: EnemyBasic = gamestate.actors[idx - Settings.ENEMY_COLUMN_COUNT]
                if next_enemy:
                    next_enemy.can_shoot = True
            gamestate.actors[gamestate.actors.index(actor)] = None
            if isinstance(actor, EnemyStage1):
                gamestate.score += 10
            elif isinstance(actor, EnemyStage2):
                gamestate.score += 50
            elif isinstance(actor, EnemyStage3):
                gamestate.score += 100
