import time
import pygame
from models.actor import Actor
from models.player import Player
from models.projectile import Projectile
from settings import Settings


class ActorController:
    __last_shot_time: float = -1

    @staticmethod
    def draw(screen: pygame.Surface, actors: list[Actor]) -> None:
        for a in actors:
            pygame.draw.rect(screen, (0, 180, 0), a.get_rectangle())

    @staticmethod
    def move(player: Player, direction: str) -> None:
        if direction == "left" and player.get_x_pos() - player.get_x_speed() >= 0:
            player.move(-1)
        if (
            direction == "right"
            and player.get_x_pos() + player.get_width() + player.get_x_speed()
            <= Settings.SCREEN_WIDTH
        ):
            player.move(1)

    @staticmethod
    def shoot(player: Player, projectiles: list[Projectile]) -> None:
        current_shot_time: float = time.time()
        if (
            ActorController.__last_shot_time == -1
            or current_shot_time - ActorController.__last_shot_time >= 0.5
        ):
            projectile: Projectile = Projectile(
                player.get_x_pos() + player.get_width() / 2,
                player.get_y_pos(),
                -1 * Settings.PROJECTILE_SPEED,
                [""],
            )
            projectiles.append(projectile)
            ActorController.__last_shot_time = current_shot_time
