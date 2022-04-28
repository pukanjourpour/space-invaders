import pygame
from settings import Settings
from models.player import Player


class PlayerController:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.settings = Settings()

        textures = ["url", "url"]
        width = 50
        height = 30
        x_pos: int = self.settings.screen_width / 2 - width / 2
        y_pos: int = self.settings.screen_height / 2 - height / 2
        x_speed = 2

        self.player = Player(textures, x_speed, x_pos, y_pos, width, height)

    def draw(self) -> None:
        pygame.draw.rect(
            self.screen,
            (100, 0, 0),
            (
                self.player.x_pos,
                self.player.y_pos,
                self.player.width,
                self.player.height,
            ),
            3,
        )

    def move(self, direction: int) -> None:
        self.player.x_pos += direction * self.player.x_speed

    def shoot(self) -> None:
        pass
