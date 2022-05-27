import pygame
from models.projectile import Projectile


class ProjectileController:
    @staticmethod
    def draw(screen: pygame.Surface, projectiles) -> None:
        for p in projectiles:
            pygame.draw.rect(screen, (180, 0, 0), pygame.Rect(p.get_x_pos(), p.get_y_pos(), p.get_width(), p.get_height()))

    @staticmethod
    def move(projectiles) -> None:
        for p in projectiles:
            p.move()
            if p.get_y_pos() < 0:
                ProjectileController.remove(p, projectiles)

    @staticmethod
    def remove(p: Projectile, projectiles) -> None:
        projectiles.remove(p)
