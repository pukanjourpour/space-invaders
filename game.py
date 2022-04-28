import pygame, sys
from controllers.actor_controller import ActorController
from controllers.projectile_controller import ProjectileController
from models.actor import Actor
from models.player import Player
from models.projectile import Projectile
from settings import Settings


class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Space Invaders")

        self.actors: list[Actor]= []
        self.projectiles: list[Projectile] = []
        player = Player(
            [""],
            self.settings.player_speed,
            self.settings.screen_width / 2,
            self.settings.screen_height - 50,
            50,
            30,
        )
        self.actors.append(player)

    def run_game(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.settings.fps)
            self._check_events()
            self._check_input()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _check_input(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            ActorController.move(self.actors[0], -1)
        elif keys_pressed[pygame.K_RIGHT]:
            ActorController.move(self.actors[0], 1)
        elif keys_pressed[pygame.K_SPACE]:
            ActorController.shoot(self.actors[0], self.projectiles)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        ProjectileController.draw(self.screen, self.projectiles)
        ActorController.draw(self.screen, self.actors)

        ProjectileController.move(self.projectiles)

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run_game()
