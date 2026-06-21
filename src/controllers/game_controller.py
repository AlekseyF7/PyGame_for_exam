"""Main controller: owns the game loop and maps input to model changes."""

from enum import Enum, auto

import pygame

from src.config.constants import (
    FPS,
    SAVE_FILE_PATH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WINDOW_TITLE,
)
from src.models.game_model import GameModel
from src.services.save_service import SaveService
from src.views.assets import AssetManager
from src.views.game_view import GameView
from src.views.menu_view import MenuView

DEFAULT_VOLUME = 0.5


class SceneState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class GameController:
    def __init__(self) -> None:
        pygame.init()
        self._init_audio()
        pygame.display.set_caption(WINDOW_TITLE)
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._clock = pygame.time.Clock()

        self._assets = AssetManager()
        self._save_service = SaveService(SAVE_FILE_PATH)
        self._volume = self._save_service.load_volume(DEFAULT_VOLUME)
        self._assets.set_volume(self._volume)
        self._best_score = self._save_service.load_best_score()
        self._total_coins = self._save_service.load_total_coins()

        self._model = GameModel()
        self._game_view = GameView(self._screen, self._assets)
        self._menu_view = MenuView(self._screen, self._assets)

        self._scene_state = SceneState.MAIN_MENU
        self._running = True

    @staticmethod
    def _init_audio() -> None:
        try:
            pygame.mixer.init()
        except pygame.error:
            pass

    def run(self) -> None:
        while self._running:
            dt = self._clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._render()
            pygame.display.flip()
        pygame.quit()

    # --- Events ---------------------------------------------------------
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                return
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

    def _handle_keydown(self, key: int) -> None:
        handlers = {
            SceneState.MAIN_MENU: self._keys_main_menu,
            SceneState.PLAYING: self._keys_playing,
            SceneState.PAUSED: self._keys_paused,
            SceneState.GAME_OVER: self._keys_game_over,
        }
        handlers[self._scene_state](key)

    def _keys_main_menu(self, key: int) -> None:
        if key == pygame.K_RETURN:
            self._start_new_game()
        elif key == pygame.K_ESCAPE:
            self._running = False

    def _keys_playing(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self._scene_state = SceneState.PAUSED

    def _keys_paused(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self._scene_state = SceneState.PLAYING

    def _keys_game_over(self, key: int) -> None:
        if key == pygame.K_RETURN:
            self._start_new_game()
        elif key == pygame.K_ESCAPE:
            self._scene_state = SceneState.MAIN_MENU

    @staticmethod
    def _read_move_direction() -> int:
        keys = pygame.key.get_pressed()
        direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction += 1
        return direction

    # --- Flow -----------------------------------------------------------
    def _start_new_game(self) -> None:
        self._model.reset()
        self._scene_state = SceneState.PLAYING

    def _update(self, dt: float) -> None:
        if self._scene_state is not SceneState.PLAYING:
            return
        self._model.update(dt, self._read_move_direction())
        if self._model.is_game_over:
            self._on_game_over()

    def _on_game_over(self) -> None:
        if self._model.score > self._best_score:
            self._best_score = self._model.score
            self._save_service.save_best_score(self._best_score)
        if self._model.coins > 0:
            self._total_coins = self._save_service.add_coins(self._model.coins)
        self._scene_state = SceneState.GAME_OVER

    # --- Render ---------------------------------------------------------
    def _render(self) -> None:
        if self._scene_state is SceneState.MAIN_MENU:
            self._menu_view.render_main_menu(self._best_score, self._total_coins)
            return

        self._game_view.render(self._model)
        if self._scene_state is SceneState.PAUSED:
            self._menu_view.render_pause()
        elif self._scene_state is SceneState.GAME_OVER:
            self._menu_view.render_game_over(self._model.score, self._best_score)
