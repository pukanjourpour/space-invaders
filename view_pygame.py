from typing import Dict, Sequence, Tuple, List
import pygame, time
from controllers.controller_actor import ControllerActor
from controllers.controller_level import ControllerLevel
from controllers.controller_obstacle import ControllerObstacle
from controllers.controller_projectile import ControllerProjectile
from gamestate import GameState
from models.enemy_stage_1 import EnemyStage1
from models.player import Player
from models.projectile import Projectile
from settings import Settings
from tkinter import filedialog as fd, Tk


class ViewPyGame(object):
    _instance = None

    def __new__(cls):
        if cls._instance == None:
            cls._instance = super(ViewPyGame, cls).__new__(cls)
            cls._running: bool = True
            cls._gamestate: GameState = None
            cls._pause: bool = False
            cls._main_menu: bool = True
            cls._in_file_browser = False
            pygame.init()
            cls._screen: pygame.Surface = pygame.display.set_mode(
                (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
            )
            pygame.display.set_caption("Space Invaders")

            cls._init_buttons(cls)

        return cls._instance

    def run_game(self) -> None:
        start_time = time.time()
        while self._running:
            current_time = time.time()
            if current_time - start_time >= 1 / Settings.FPS:
                delta_time = 0
                if not self._in_file_browser:
                    delta_time = current_time - start_time
                else:
                    self._in_file_browser = False

                self._update(delta_time)
                start_time = current_time
            self._draw()

    def _update(self, delta_time: int) -> None:
        keyboard_input = self._get_keyboard_input()
        if not self._pause and not self._main_menu:
            self._check_collisions()
            ControllerActor.act(self._gamestate, keyboard_input, delta_time)
            ControllerProjectile.move(self._gamestate, delta_time)
        self._check_events()

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if self._main_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self._check_hover((mouse_x, mouse_y), self._btn_new_game):
                        self._init_gamestate(new_game=True)
                        self._main_menu = False
                    elif self._check_hover((mouse_x, mouse_y), self._btn_load_game):
                        response = self._init_gamestate(new_game=False)
                        if response == 1:
                            self._main_menu = False
                    elif self._check_hover((mouse_x, mouse_y), self._btn_quit_game):
                        self._running = False
            elif self._pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self._check_hover((mouse_x, mouse_y), self._btn_continue):
                        self._pause = False
                    elif self._check_hover((mouse_x, mouse_y), self._btn_restart):
                        self._init_gamestate(new_game=True)
                        self._pause = False
                    elif self._check_hover((mouse_x, mouse_y), self._btn_save_and_quit):
                        self._save_game()
                        if response == 1:
                            self._running = False

            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self._pause = not self._pause
                # TODO time the pauses to prevent projectile cooldown bugs

    def _get_keyboard_input(self) -> Sequence[bool]:
        return pygame.key.get_pressed()

    def _check_collisions(self) -> None:
        for p in self._gamestate.projectiles:
            if p.direction == 1:
                for o in self._gamestate.obstacles:
                    if (
                        p.y + p.height >= o.y
                        and o.x <= p.x
                        and o.x + o.width >= p.x + p.width
                    ):
                        ControllerObstacle.receive_hit(o, self._gamestate)
                        ControllerProjectile.receive_hit(p, self._gamestate)
                for a in self._gamestate.actors:
                    if (
                        isinstance(a, Player)
                        and p.y + p.height >= a.y
                        and a.x <= p.x
                        and a.x + a.width >= p.x + p.width
                    ):
                        ControllerActor.receive_hit(a, self._gamestate)
                        ControllerProjectile.receive_hit(p, self._gamestate)
            elif p.direction == -1:
                for o in self._gamestate.obstacles:
                    if (
                        p.y <= o.y + o.height
                        and o.x <= p.x
                        and o.x + o.width >= p.x + p.width
                    ):
                        ControllerObstacle.receive_hit(o, self._gamestate)
                        ControllerProjectile.receive_hit(p, self._gamestate)
                for a in self._gamestate.actors:
                    if (
                        not isinstance(a, Player)
                        and p.y <= a.y + a.height
                        and a.x <= p.x
                        and a.x + a.width >= p.x + p.width
                    ):
                        ControllerActor.receive_hit(a, self._gamestate)
                        ControllerProjectile.receive_hit(p, self._gamestate)

    def _init_gamestate(self, new_game: bool) -> int:
        response = 1
        if new_game:
            level = 1
            new_actors, new_obstacles = ControllerLevel.generate_level(level)
            new_projectiles: List[Projectile] = []
            self._gamestate = GameState(new_actors, new_projectiles, new_obstacles, 1)
        else:
            full_path = self._select_file()
            self._in_file_browser = True
            try:
                with open(full_path, "r", encoding="utf8") as f:
                    json_string = f.read()
                    self._gamestate = GameState.from_json(json_string)
            except Exception as e:
                response = -1
                print(type(e).__name__)

            return response

    def _save_game(self) -> int:
        response = 1
        directory_name: str = self._select_directory()
        full_path: str = directory_name + "/save1.json"
        try:
            with open(full_path, "w", encoding="utf8") as f:
                f.write(self._gamestate.to_json())
        except Exception as e:
            response = -1
            print(type(e).__name__)

        return response

    def _select_file(cls) -> str:
        Tk().withdraw()
        filename: str = fd.askopenfilename(
            title="Select a save file",
            filetypes=(("Json File", "*.json"),),
        )
        return filename

    def _select_directory(self) -> str:
        Tk().withdraw()
        directory_name: str = fd.askdirectory(title="Select folder to save game")
        return directory_name

    def _draw(self):
        self._screen.fill((0, 0, 0))

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
                if isinstance(actor, Player):
                    pygame.draw.rect(
                        self._screen,
                        (130, 0, 50),
                        [actor.x, actor.y, actor.width, actor.height],
                    )
                elif isinstance(actor, EnemyStage1):
                    pygame.draw.rect(
                        self._screen,
                        (200, 50, 130),
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

    def _init_buttons(cls) -> None:
        smallfont = pygame.font.SysFont("Corbel", Settings.SMALL_FONT_SIZE)

        text_new_game = smallfont.render("NEW GAME", True, (155, 255, 255))
        text_load_game = smallfont.render("LOAD GAME", True, (155, 255, 255))
        text_quit = smallfont.render("QUIT", True, (155, 255, 255))
        text_continue = smallfont.render("CONTINUE", True, (155, 255, 255))
        text_restart = smallfont.render("RESTART", True, (155, 255, 255))
        text_save_and_quit = smallfont.render("SAVE AND QUIT", True, (155, 255, 255))

        cls._btn_new_game: Dict[str, any] = {
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
        cls._btn_load_game: Dict(str, any) = {
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
        cls._btn_quit_game: Dict(str, any) = {
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

        cls._btn_continue: Dict[str, any] = {
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
        cls._btn_restart: Dict(str, any) = {
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
        cls._btn_save_and_quit: Dict(str, any) = {
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

        cls._buttons_main_menu: List[Dict[str, any]] = [
            cls._btn_new_game,
            cls._btn_load_game,
            cls._btn_quit_game,
        ]
        cls._buttons_pause: List[Dict[str, any]] = [
            cls._btn_continue,
            cls._btn_restart,
            cls._btn_save_and_quit,
        ]
