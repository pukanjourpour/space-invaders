from turtle import Screen
from typing import List
from gamestate import GameState

from models.projectile import Projectile
from settings import Settings


class ControllerProjectile:
    @staticmethod
    def move(gamestate: GameState, delta_time: float):
        for projectile in gamestate.projectiles:
            projectile.y = int(
                projectile.y + projectile.speed * projectile.direction * delta_time
            )
            if (
                projectile.y < 0
                or projectile.y + projectile.height > Settings.GAME_WINDOW_HEIGHT
            ):
                gamestate.projectiles.remove(projectile)

    @staticmethod
    def receive_hit(projectile: Projectile, gamestate: GameState):
        gamestate.projectiles.remove(projectile)
