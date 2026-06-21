"""Rendering of menus and the game-over screen (Russian UI)."""

import pygame

from src.config.constants import (
    COLOR_OVERLAY,
    COLOR_TEXT,
    COLOR_TEXT_DIM,
    FONT_SIZE_NORMAL,
    FONT_SIZE_SMALL,
    FONT_SIZE_TITLE,
    IMAGE_MENU_BACKGROUND,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from src.views.assets import AssetManager


class MenuView:
    def __init__(self, screen: pygame.Surface, assets: AssetManager) -> None:
        self._screen = screen
        self._assets = assets
        self._title_font = assets.font(FONT_SIZE_TITLE)
        self._font = assets.font(FONT_SIZE_NORMAL)
        self._small_font = assets.font(FONT_SIZE_SMALL)
        self._menu_bg = assets.image(
            IMAGE_MENU_BACKGROUND, size=(SCREEN_WIDTH, SCREEN_HEIGHT), smooth=True
        )

    def render_main_menu(self, best_score: int, total_coins: int) -> None:
        self._screen.blit(self._menu_bg, (0, 0))
        self._blit_centered("JUMP OR DIE", 150, self._title_font)
        self._blit_centered("Enter — играть", 320, self._font)
        self._blit_centered("Esc — выход", 370, self._font)
        self._blit_centered(f"Рекорд: {best_score}", 460, self._small_font, COLOR_TEXT_DIM)
        self._blit_centered(f"Монеты: {total_coins}", 495, self._small_font, COLOR_TEXT_DIM)
        self._blit_centered("Управление: ← → или A / D", 540, self._small_font, COLOR_TEXT_DIM)

    def render_pause(self) -> None:
        self._dim()
        self._blit_centered("ПАУЗА", 280, self._title_font)
        self._blit_centered("Esc — продолжить", 380, self._font)

    def render_game_over(self, score: int, best_score: int) -> None:
        self._dim()
        self._blit_centered("ИГРА ОКОНЧЕНА", 240, self._title_font)
        self._blit_centered(f"Счёт: {score}", 340, self._font)
        self._blit_centered(f"Рекорд: {best_score}", 390, self._font)
        self._blit_centered("Enter — заново", 470, self._font)
        self._blit_centered("Esc — в меню", 520, self._font)

    def _dim(self) -> None:
        overlay = pygame.Surface(self._screen.get_size(), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        self._screen.blit(overlay, (0, 0))

    def _blit_centered(
        self,
        text: str,
        y: int,
        font: pygame.font.Font,
        color: tuple[int, int, int] = COLOR_TEXT,
    ) -> None:
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(self._screen.get_width() // 2, y))
        self._screen.blit(surface, rect)
