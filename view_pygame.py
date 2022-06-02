from typing import Dict, Sequence, Tuple, List
import pygame, time
from controllers.controller_actor import ControllerActor
from controllers.controller_projectile import ControllerProjectile
from gamestate import GameState
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

        self._init_buttons()

    def run_game(self) -> None:
        start_time_millis = time.time()
        start_time = time.time()
        timer =  0
        while self._running:
            current_time = time.time()
            timer += current_time- start_time
            start_time = current_time
            time_text = pygame.font.SysFont("Corbel", Settings.SMALL_FONT_SIZE).render(
                str(timer), True, (155, 255, 255)
            )
            self._screen.fill(Settings.BG_COLOR)
            self._screen.blit(time_text, (10, 10))
            if not self._main_menu:
                current_time_millis = time.time()
                if current_time_millis - start_time_millis >= 1 / Settings.FPS:
                    delta_time = current_time_millis - start_time_millis
                    self._update(delta_time)
                    start_time_millis = current_time_millis
            self._draw()
            self._check_events()

    def _update(self, delta_time: int) -> None:
        keyboard_input = self._get_keyboard_input()
        if not self._pause:
            ControllerActor.act(
                self._gamestate.actors, keyboard_input, self._gamestate, delta_time
            )
            ControllerProjectile.move(self._gamestate.projectiles, delta_time)

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if self._main_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self._check_hover((mouse_x, mouse_y), self._btn_new_game):
                        self._gamestate = GameState(True)
                        self._main_menu = False
                    elif self._check_hover((mouse_x, mouse_y), self._btn_load_game):
                        self._gamestate = GameState(False)
                        self._main_menu = False
                    elif self._check_hover((mouse_x, mouse_y), self._btn_quit_game):
                        self._running = False
            elif self._pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self._check_hover((mouse_x, mouse_y), self._btn_continue):
                        self._pause = False
                    elif self._check_hover((mouse_x, mouse_y), self._btn_restart):
                        self._gamestate = GameState(True)
                        self._pause = False
                    elif self._check_hover((mouse_x, mouse_y), self._btn_save_and_quit):
                        self._running = False

            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self._pause = not self._pause

    def _get_keyboard_input(self) -> Sequence[bool]:
        return pygame.key.get_pressed()

    def _check_collisions(self) -> None:
        pass

    def _draw(self):
        # self._screen.fill(Settings.BG_COLOR)
        if self._main_menu:
            self._draw_menu(0)
        elif self._pause:
            self._draw_menu(1)
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

    def _draw_menu(self, menu_type: int) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        buttons = self._buttons_main_menu if menu_type == 0 else self._buttons_pause
        for btn in buttons:
            if self._check_hover((mouse_x, mouse_y), btn):
                pygame.draw.rect(
                    self._screen,
                    (130, 130, 130),
                    [
                        btn["btn_x"],
                        btn["btn_y"],
                        btn["btn_width"],
                        btn["btn_height"],
                    ],
                )
            self._screen.blit(
                btn["text"],
                (btn["text_x"], btn["text_y"]),
            )

    def _draw_side_menu(self) -> None:
        pass

    def _check_hover(self, mouse: Tuple[int, int], btn: Dict[str, any]) -> bool:
        mouse_x, mouse_y = mouse
        return (
            btn["btn_x"] <= mouse_x <= btn["btn_x"] + btn["btn_width"]
            and btn["btn_y"] <= mouse_y <= btn["btn_y"] + btn["btn_height"]
        )

    def _init_buttons(self) -> None:
        smallfont = pygame.font.SysFont("Corbel", Settings.SMALL_FONT_SIZE)

        text_new_game = smallfont.render("NEW GAME", True, (155, 255, 255))
        text_load_game = smallfont.render("LOAD GAME", True, (155, 255, 255))
        text_quit = smallfont.render("QUIT", True, (155, 255, 255))
        text_continue = smallfont.render("CONTINUE", True, (155, 255, 255))
        text_restart = smallfont.render("RESTART", True, (155, 255, 255))
        text_save_and_quit = smallfont.render("SAVE AND QUIT", True, (155, 255, 255))

        self._btn_new_game: Dict[str, any] = {
            "text": text_new_game,
            "text_x": Settings.SCREEN_WIDTH / 2 - text_new_game.get_width() / 2,
            "text_y": Settings.SCREEN_HEIGHT / 2
            - (Settings.BTN_HEIGHT * 3 / 2)
            + Settings.BTN_PADDING,
            "btn_x": Settings.SCREEN_WIDTH / 2 - Settings.BTN_WIDTH / 2,
            "btn_y": Settings.SCREEN_HEIGHT / 2 - (Settings.BTN_HEIGHT * 3 / 2),
            "btn_width": Settings.BTN_WIDTH,
            "btn_height": Settings.BTN_HEIGHT,
        }
        self._btn_load_game: Dict(str, any) = {
            "text": text_load_game,
            "text_x": Settings.SCREEN_WIDTH / 2 - text_load_game.get_width() / 2,
            "text_y": Settings.SCREEN_HEIGHT / 2
            - (Settings.BTN_HEIGHT * 3 / 2)
            + Settings.BTN_HEIGHT
            + Settings.BTN_PADDING,
            "btn_x": Settings.SCREEN_WIDTH / 2 - Settings.BTN_WIDTH / 2,
            "btn_y": Settings.SCREEN_HEIGHT / 2
            - (Settings.BTN_HEIGHT * 3 / 2)
            + Settings.BTN_HEIGHT,
            "btn_width": Settings.BTN_WIDTH,
            "btn_height": Settings.BTN_HEIGHT,
        }
        self._btn_quit_game: Dict(str, any) = {
            "text": text_quit,
            "text_x": Settings.SCREEN_WIDTH / 2 - text_quit.get_width() / 2,
            "text_y": Settings.SCREEN_HEIGHT / 2
            - (Settings.BTN_HEIGHT * 3 / 2)
            + Settings.BTN_HEIGHT * 2
            + Settings.BTN_PADDING,
            "btn_x": Settings.SCREEN_WIDTH / 2 - Settings.BTN_WIDTH / 2,
            "btn_y": Settings.SCREEN_HEIGHT / 2
            - (Settings.BTN_HEIGHT * 3 / 2)
            + Settings.BTN_HEIGHT * 2,
            "btn_width": Settings.BTN_WIDTH,
            "btn_height": Settings.BTN_HEIGHT,
        }

        self._btn_continue: Dict[str, any] = {
            "text": text_continue,
            "text_x": Settings.SCREEN_WIDTH / 2 - text_continue.get_width() / 2,
            "text_y": Settings.SCREEN_HEIGHT / 2
            - (Settings.BTN_HEIGHT * 3 / 2)
            + Settings.BTN_PADDING,
            "btn_x": Settings.SCREEN_WIDTH / 2 - Settings.BTN_WIDTH / 2,
            "btn_y": Settings.SCREEN_HEIGHT / 2 - (Settings.BTN_HEIGHT * 3 / 2),
            "btn_width": Settings.BTN_WIDTH,
            "btn_height": Settings.BTN_HEIGHT,
        }
        self._btn_restart: Dict(str, any) = {
            "text": text_restart,
            "text_x": Settings.SCREEN_WIDTH / 2 - text_restart.get_width() / 2,
            "text_y": Settings.SCREEN_HEIGHT / 2
            - (Settings.BTN_HEIGHT * 3 / 2)
            + Settings.BTN_HEIGHT
            + Settings.BTN_PADDING,
            "btn_x": Settings.SCREEN_WIDTH / 2 - Settings.BTN_WIDTH / 2,
            "btn_y": Settings.SCREEN_HEIGHT / 2
            - (Settings.BTN_HEIGHT * 3 / 2)
            + Settings.BTN_HEIGHT,
            "btn_width": Settings.BTN_WIDTH,
            "btn_height": Settings.BTN_HEIGHT,
        }
        self._btn_save_and_quit: Dict(str, any) = {
            "text": text_save_and_quit,
            "text_x": Settings.SCREEN_WIDTH / 2 - text_save_and_quit.get_width() / 2,
            "text_y": Settings.SCREEN_HEIGHT / 2
            - (Settings.BTN_HEIGHT * 3 / 2)
            + Settings.BTN_HEIGHT * 2
            + Settings.BTN_PADDING,
            "btn_x": Settings.SCREEN_WIDTH / 2 - Settings.BTN_WIDTH / 2,
            "btn_y": Settings.SCREEN_HEIGHT / 2
            - (Settings.BTN_HEIGHT * 3 / 2)
            + Settings.BTN_HEIGHT * 2,
            "btn_width": Settings.BTN_WIDTH,
            "btn_height": Settings.BTN_HEIGHT,
        }

        self._buttons_main_menu: List[Dict[str, any]] = [
            self._btn_new_game,
            self._btn_load_game,
            self._btn_quit_game,
        ]
        self._buttons_pause: List[Dict[str, any]] = [
            self._btn_continue,
            self._btn_restart,
            self._btn_save_and_quit,
        ]
