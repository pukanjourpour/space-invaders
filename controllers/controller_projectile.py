from turtle import Screen
from typing import List

from models.projectile import Projectile
from settings import Settings


class ControllerProjectile:
    @staticmethod
    def move(projectiles: List[Projectile], delta_time: float):
        for projectile in projectiles:
            projectile.y = int(projectile.y + Settings.PROJECTILE_SPEED * projectile.direction * delta_time)
            if projectile.y < 0 or projectile.y + projectile.height > Settings.SCREEN_HEIGHT: 
                projectiles.remove(projectile)