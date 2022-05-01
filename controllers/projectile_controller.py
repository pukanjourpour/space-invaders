import pygame
from models.projectile import Projectile


class ProjectileController:
    @staticmethod
    def draw(screen: pygame.Surface, projectiles: list[Projectile]) -> None:
        for p in projectiles:
            pygame.draw.rect(screen, (180, 0, 0), p.get_rectangle())

    @staticmethod
    def move(projectiles: list[Projectile]) -> None:
        for p in projectiles:
            p.move()
            if p.get_y_pos() < 0:
                ProjectileController.remove(p, projectiles)

    @staticmethod
    def remove(p: Projectile, projectiles: list[Projectile]):
        projectiles.remove(p)
