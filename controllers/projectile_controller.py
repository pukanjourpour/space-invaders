import pygame
from models.projectile import Projectile

class ProjectileController:
    @staticmethod
    def draw(screen: pygame.Surface, projectiles: list[Projectile]) -> None:
        for p in projectiles:
            pygame.draw.rect(
                screen, (180, 0, 0), (p.x_pos, p.y_pos, p.width, p.height)
            )

    @staticmethod
    def move(projectiles: list[Projectile]) -> None:
        for p in projectiles:
            p.y_pos += p.y_speed
