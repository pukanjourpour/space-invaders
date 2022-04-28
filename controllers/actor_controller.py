import pygame
from models.actor import Actor
from models.player import Player
from models.projectile import Projectile 

class ActorController:
    @staticmethod
    def draw(screen: pygame.Surface, actors: list[Actor]):
        for a in actors:
            pygame.draw.rect(screen, (0, 180, 0), (a.x_pos, a.y_pos, a.width, a.height))
    
    @staticmethod
    def move(player: Player, direction):
        player.x_pos += player.x_speed * direction

    @staticmethod
    def shoot(player: Player, projectiles: list[Projectile]) -> None:
        projectile = Projectile(player.x_pos + player.width/ 2, player.y_pos, -1, [''])
        projectiles.append(projectile)

        return projectile
