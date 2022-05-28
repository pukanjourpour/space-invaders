from turtle import update
from typing import Sequence, Set
import pygame, time
from controllers.controller_actor import ControllerActor
from controllers.controller_projectile import ControllerProjectile
from gamestate import GameState
from models.actor import Actor
from models.player import Player
from models.projectile import Projectile
from settings import Settings


class ViewPyGame:
    def __init__(self):

        self._running: bool = True
        self._gamestate: GameState = None
        self._pause: bool = False
        self._main_menu: bool = True

        pygame.init()
        self._screen: pygame.Surface = pygame.display.set_mode(
            (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Space Invaders")

        smallfont = pygame.font.SysFont("Corbel", Settings.SMALL_FONT_SIZE)
        self._text_new_game = smallfont.render("NEW GAME", True, (155, 255, 255))
        self._text_load_game = smallfont.render("LOAD GAME", True, (155, 255, 255))
        self._text_quit = smallfont.render("QUIT", True, (155, 255, 255))

    def run_game(self) -> None:
        start_time_millis = time.time()
        while self._running:
            if not self._main_menu:
                current_time_millis = time.time()
                if current_time_millis - start_time_millis >= 1 / Settings.FPS:
                    delta_time = current_time_millis - start_time_millis
                    self._update(delta_time)
                    start_time_millis = current_time_millis
            self._draw()
            self._check_events()

    def _draw(self):
        self._screen.fill(Settings.BG_COLOR)
        if self._main_menu:
            self._draw_main_menu()
        else:
            self._draw_side_menu()

            for projectile in self._gamestate.projectiles:
                pygame.draw.rect(
                    self._screen,
                    (50, 0, 130),
                    [projectile.x, projectile.y, projectile.width, projectile.height],
                )
            for actor in self._gamestate.actors:
                pygame.draw.rect(
                    self._screen,
                    (130, 0, 50),
                    [actor.x, actor.y, actor.width, actor.height],
                )
            for obstacle in self._gamestate.obstacles:
                pygame.draw.rect(
                    self._screen,
                    (0, 130, 50),
                    (obstacle.x, obstacle.y, obstacle.width, obstacle.height),
                )
        pygame.display.flip()

    def _update(self, delta_time: int) -> None:
        keyboard_input = self._get_keyboard_input()
        ControllerActor.act(
            self._gamestate.actors, keyboard_input, self._gamestate, delta_time
        )
        ControllerProjectile.move(self._gamestate.projectiles, delta_time)

    def _draw_main_menu(self) -> None:
        unit_height = Settings.SMALL_FONT_SIZE + Settings.BTN_PADDING * 2
        half_width = Settings.SCREEN_WIDTH / 2
        half_height = Settings.SCREEN_HEIGHT / 2
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # NEW GAME button
        if (
            half_width - 175 <= mouse_x <= half_width + 175
            and half_height - unit_height * 3 / 2
            <= mouse_y
            <= half_height - unit_height * 3 / 2 + unit_height
        ):
            pygame.draw.rect(
                self._screen,
                (130, 130, 130),
                [
                    half_width - 175,
                    half_height - unit_height * 3 / 2 - Settings.BTN_PADDING,
                    350,
                    unit_height,
                ],
            )
        self._screen.blit(
            self._text_new_game,
            (
                half_width - self._text_new_game.get_width() / 2,
                half_height - unit_height * 3 / 2,
            ),
        )

        # LOAD GAME button
        if (
            half_width - 175 <= mouse_x <= half_width + 175
            and half_height - unit_height * 3 / 2 + unit_height
            <= mouse_y
            <= half_height - unit_height * 3 / 2 + unit_height * 2
        ):
            pygame.draw.rect(
                self._screen,
                (130, 130, 130),
                [
                    half_width - 175,
                    half_height
                    - unit_height * 3 / 2
                    + unit_height
                    - Settings.BTN_PADDING,
                    350,
                    unit_height,
                ],
            )
        self._screen.blit(
            self._text_load_game,
            (
                half_width - self._text_load_game.get_width() / 2,
                half_height - unit_height * 3 / 2 + unit_height,
            ),
        )

        # QUIT button
        if (
            half_width - 175 <= mouse_x <= half_width + 175
            and half_height - unit_height * 3 / 2 + unit_height * 2
            <= mouse_y
            <= half_height - unit_height * 3 / 2 + unit_height * 3
        ):
            pygame.draw.rect(
                self._screen,
                (130, 130, 130),
                [
                    half_width - 175,
                    half_height
                    - unit_height * 3 / 2
                    + unit_height * 2
                    - Settings.BTN_PADDING,
                    350,
                    unit_height,
                ],
            )
        self._screen.blit(
            self._text_quit,
            (
                half_width - self._text_quit.get_width() / 2,
                half_height - unit_height * 3 / 2 + unit_height * 2,
            ),
        )

    def _draw_side_menu(self) -> None:
        pass

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if self._main_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    half_width = Settings.SCREEN_WIDTH / 2
                    half_height = Settings.SCREEN_HEIGHT / 2
                    unit_height = Settings.SMALL_FONT_SIZE + Settings.BTN_PADDING * 2
                    if (
                        mouse_x
                        >= half_width
                        - self._text_new_game.get_width() / 2
                        - Settings.BTN_PADDING
                        and mouse_x
                        <= half_width
                        + self._text_new_game.get_width() / 2
                        + Settings.BTN_PADDING
                        and mouse_y >= half_height - unit_height * 3 / 2
                        and mouse_y <= half_height - unit_height * 3 / 2 + unit_height
                    ):
                        self._gamestate = GameState(True)
                        self._main_menu = False
                    elif (
                        mouse_x
                        >= half_width
                        - self._text_load_game.get_width() / 2
                        - Settings.BTN_PADDING
                        and mouse_x
                        <= half_width
                        + self._text_load_game.get_width() / 2
                        + Settings.BTN_PADDING
                        and mouse_y >= half_height - unit_height * 3 / 2 + unit_height
                        and mouse_y
                        <= half_height - unit_height * 3 / 2 + unit_height * 2
                    ):
                        self._gamestate = GameState(False)
                        self._main_menu = False
                    elif (
                        mouse_x
                        >= half_width
                        - self._text_quit.get_width() / 2
                        - Settings.BTN_PADDING
                        and mouse_x
                        <= half_width
                        + self._text_quit.get_width() / 2
                        + Settings.BTN_PADDING
                        and mouse_y
                        >= half_height - unit_height * 3 / 2 + unit_height * 2
                        and mouse_y
                        <= half_height - unit_height * 3 / 2 + unit_height * 3
                    ):
                        self._running = False

    def _get_keyboard_input(self) -> Sequence[bool]:
        keyboard_input = pygame.key.get_pressed()
        return keyboard_input

    def _check_collisions(self) -> None:
        pass
