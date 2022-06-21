from typing import Dict, Sequence, Tuple, List
import pygame, time
from controllers.controller_actor import ControllerActor
from controllers.controller_level import ControllerLevel
from controllers.controller_obstacle import ControllerObstacle
from controllers.controller_projectile import ControllerProjectile
from gamestate import GameState
from models.enemy_basic import EnemyBasic
from models.enemy_stage_1 import EnemyStage1
from models.enemy_stage_2 import EnemyStage2
from models.enemy_stage_3 import EnemyStage3
from models.player import Player
from models.projectile import Projectile
from settings import Settings
from tkinter import filedialog as fd, Tk


class ViewPyGame(object):
    _instance = None

    @property
    def instance(self):
        return self._instance

    def __init__(self):
        if ViewPyGame._instance == None:
            ViewPyGame._instance = self
            self._running: bool = True
            self._gamestate: GameState = None
            self._pause: bool = False
            self._main_menu: bool = True
            self._in_file_browser = False
            self._basic_enemy_count = -1
            self._hit_count = 0
            pygame.init()
            self._screen: pygame.Surface = pygame.display.set_mode(
                (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
            )
            pygame.display.set_caption("Space Invaders")

            self._init_buttons()
        else: 
            raise Exception("Singleton cannot have multiple instances.")

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
        if self._gamestate and self._gamestate.game_over:
            self._main_menu = True
            self._gamestate.game_over = False
        elif not self._pause and not self._main_menu:
            self._check_collisions()
            if self._hit_count == self._basic_enemy_count:
                if self._gamestate.level + 1 > 2:
                    self._gamestate.game_over = True
                else:
                    self._gamestate.level += 1
                    self._set_level(self._gamestate.level)
                    self._hit_count = 0
            else:
                ControllerActor.act(self._gamestate, keyboard_input, delta_time)
                ControllerProjectile.move(self._gamestate, delta_time)
            
        self._check_events()

    def _count_enemies(self) -> int:
        count = 0
        for actor in self._gamestate.actors:
            if isinstance(actor, EnemyBasic):
                count += 1
        return count

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
                        response = self._save_game()
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
                        and p.y <= o.y + o.height
                        and o.x <= p.x
                        and o.x + o.width >= p.x + p.width
                    ):
                        ControllerObstacle.receive_hit(o, self._gamestate)
                        ControllerProjectile.receive_hit(p, self._gamestate)
                for a in self._gamestate.actors:
                    if (
                        a
                        and isinstance(a, Player)
                        and p.y + p.height >= a.y
                        and p.y <= a.y + a.height
                        and a.x <= p.x
                        and a.x + a.width >= p.x + p.width
                    ):
                        ControllerActor.receive_hit(a, self._gamestate)
                        ControllerProjectile.receive_hit(p, self._gamestate)
            elif p.direction == -1:
                for o in self._gamestate.obstacles:
                    if (
                        p.y <= o.y + o.height
                        and p.y + p.height >= o.y
                        and o.x <= p.x
                        and o.x + o.width >= p.x + p.width
                    ):
                        ControllerObstacle.receive_hit(o, self._gamestate)
                        ControllerProjectile.receive_hit(p, self._gamestate)
                for a in self._gamestate.actors:
                    if (
                        a
                        and not isinstance(a, Player)
                        and p.y <= a.y + a.height
                        and p.y + p.height >= a.y
                        and a.x <= p.x
                        and a.x + a.width >= p.x + p.width
                    ):
                        self._hit_count += 1
                        ControllerActor.receive_hit(a, self._gamestate)
                        ControllerProjectile.receive_hit(p, self._gamestate)
            for p2 in self._gamestate.projectiles:
                if not p == p2 and p.y <= p2.y + p2.height and p.y + p.height >= p2.y and p2.x <= p.x and p2.x + p2.width >= p.x + p.width:
                    ControllerProjectile.receive_hit(p, self._gamestate)
                    ControllerProjectile.receive_hit(p2, self._gamestate)

    def _init_gamestate(self, new_game: bool) -> int:
        response = 1
        if new_game:
            self._set_level(1)
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

    def _set_level(self, new_level: int):
        new_actors, new_obstacles, enemy_count, new_enemy_x_movement_timeout, new_enemy_y_movement_timeout, new_enemy_shoot_timeout = ControllerLevel.generate_level(new_level)
        new_lives_count = 3
        if new_level > 1:
            for a in self._gamestate.actors:
                if isinstance(a, Player):
                    new_actors.append(a)
                    break
            new_lives_count: int = self._gamestate.lives_count
        new_projectiles: List[Projectile] = []
        self._basic_enemy_count = enemy_count
        self._gamestate = GameState(
            new_actors, new_projectiles, new_obstacles, new_level, new_enemy_x_movement_timeout, new_enemy_y_movement_timeout, new_enemy_shoot_timeout, new_lives_count
        )

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

    def _select_file(self) -> str:
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
                if actor:
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
                    elif isinstance(actor, EnemyStage2):
                        pygame.draw.rect(
                                self._screen,
                                (250, 50, 100),
                                [actor.x, actor.y, actor.width, actor.height],
                            )
                    elif isinstance(actor, EnemyStage3):
                        pygame.draw.rect(
                            self._screen,
                            (250, 0, 0),
                            [actor.x, actor.y, actor.width, actor.height],
                        )
            for obstacle in self._gamestate.obstacles:
                pygame.draw.rect(
                    self._screen,
                    (
                        100 - (50 / Settings.OBSTACLE_HIT_COUNT) * obstacle.hit_count,
                        (130 / Settings.OBSTACLE_HIT_COUNT) * obstacle.hit_count,
                        (50 / Settings.OBSTACLE_HIT_COUNT) * obstacle.hit_count,
                    ),
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
        pygame.draw.rect(
            self._screen,
            (30, 30, 30),
            [
                Settings.SCREEN_WIDTH - Settings.SIDE_MENU_WIDTH,
                0,
                Settings.SIDE_MENU_WIDTH,
                Settings.SIDE_MENU_HEIGHT,
            ],
        )
        smallfont = pygame.font.SysFont("Corbel", Settings.SMALL_FONT_SIZE)
        text_level = smallfont.render("Level " + str(self._gamestate.level), True, (155, 255, 255))
        text_score = smallfont.render("Score: " + str(self._gamestate.score), True, (155, 255, 255))
        text_lives_count = smallfont.render("Lives: " +
            str(self._gamestate.lives_count), True, (155, 255, 255)
        )

        self._screen.blit(
            text_level,
            (
                Settings.SCREEN_WIDTH
                - Settings.SIDE_MENU_WIDTH / 2
                - text_score.get_width() / 2,
                100,
            ),
        )
        self._screen.blit(
            text_score,
            (
                Settings.SCREEN_WIDTH
                - Settings.SIDE_MENU_WIDTH / 2
                - text_score.get_width() / 2,
                Settings.SIDE_MENU_HEIGHT / 2,
            ),
        )
        self._screen.blit(
            text_lives_count,
            (
                Settings.SCREEN_WIDTH
                - Settings.SIDE_MENU_WIDTH / 2
                - text_score.get_width() / 2,
                Settings.SIDE_MENU_HEIGHT - 100,
            ),
        )

    def _check_hover(self, mouse: Tuple[int, int], btn: Dict[str, any]) -> bool:
        mouse_x, mouse_y = mouse
        btn_x = btn["btn_x"]
        btn_y = btn["btn_y"]
        btn_width = btn["btn_width"]
        btn_height = btn["btn_height"]
        return (
            btn_x <= mouse_x <= btn_x + btn_width
            and btn_y <= mouse_y <= btn_y + btn_height
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
        self._btn_load_game: Dict[str, any] = {
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
        self._btn_quit_game: Dict[str, any] = {
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
        self._btn_restart: Dict[str, any] = {
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
        self._btn_save_and_quit: Dict[str, any] = {
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
