"""Rendering of the gameplay scene (sky, ground, items, platforms, player, HUD)."""

import math

import pygame

from src.config.constants import (
    COIN_SIZE,
    COLOR_BACKGROUND,
    COLOR_TEXT,
    ELYTRA_SIZE,
    FONT_SIZE_NORMAL,
    GROUND_TOP_Y,
    IMAGE_BACKGROUND,
    IMAGE_COIN,
    IMAGE_ELYTRA,
    IMAGE_GROUND,
    IMAGE_PLATFORM_BREAKABLE,
    IMAGE_PLATFORM_MOVING,
    IMAGE_PLATFORM_SPRING,
    IMAGE_PLATFORM_STATIC,
    IMAGE_PLAYER,
    IMAGE_PLAYER_JUMP,
    IMAGE_PORTAL,
    PLATFORM_HEIGHT,
    PLATFORM_WIDTH,
    PLAYER_WIDTH,
    PORTAL_SIZE,
    SKY_DRIFT,
    SKY_DRIFT_FREQ,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from src.models.entities import Coin, Platform, PlatformKind
from src.models.game_model import GameModel
from src.views.assets import AssetManager

_PLATFORM_IMAGES = {
    PlatformKind.STATIC: IMAGE_PLATFORM_STATIC,
    PlatformKind.MOVING: IMAGE_PLATFORM_MOVING,
    PlatformKind.BREAKABLE: IMAGE_PLATFORM_BREAKABLE,
    PlatformKind.SPRING: IMAGE_PLATFORM_SPRING,
}


class GameView:
    def __init__(self, screen: pygame.Surface, assets: AssetManager) -> None:
        self._screen = screen
        self._assets = assets
        self._font = assets.font(FONT_SIZE_NORMAL)
        self._facing_left = False
        self._load_sprites(assets)

    def _load_sprites(self, assets: AssetManager) -> None:
        # Sky: a bit taller than the screen so it can drift without seams.
        self._sky = assets.image(
            IMAGE_BACKGROUND, size=(SCREEN_WIDTH, SCREEN_HEIGHT + 2 * SKY_DRIFT), smooth=True
        )

        self._ground = self._scale_to_width(IMAGE_GROUND, SCREEN_WIDTH, smooth=True)
        self._ground_h = self._ground.get_height()

        self._player_idle = self._scale_to_width(IMAGE_PLAYER, PLAYER_WIDTH, smooth=False)
        self._player_jump = self._scale_to_width(IMAGE_PLAYER_JUMP, PLAYER_WIDTH, smooth=False)
        self._player_idle_left = pygame.transform.flip(self._player_idle, True, False)
        self._player_jump_left = pygame.transform.flip(self._player_jump, True, False)

        platform_size = (PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self._platform_sprites = {
            kind: assets.image(name, size=platform_size, smooth=False)
            for kind, name in _PLATFORM_IMAGES.items()
        }

        self._coin_sprite = assets.image(IMAGE_COIN, size=(COIN_SIZE, COIN_SIZE), smooth=False)
        self._elytra_sprite = assets.image(IMAGE_ELYTRA, size=(ELYTRA_SIZE, ELYTRA_SIZE), smooth=False)
        self._portal_sprite = assets.image(IMAGE_PORTAL, size=(PORTAL_SIZE, PORTAL_SIZE), smooth=False)

    def _scale_to_width(self, name: str, target_width: int, smooth: bool) -> pygame.Surface:
        natural = self._assets.image(name)
        ratio = natural.get_height() / natural.get_width()
        target_height = max(1, int(target_width * ratio))
        return self._assets.image(name, size=(target_width, target_height), smooth=smooth)

    def render(self, model: GameModel) -> None:
        self._draw_sky(model.camera_y)
        self._draw_ground(model.camera_y)
        self._draw_portals(model)
        for platform in model.platforms:
            self._draw_platform(platform, model.camera_y)
        self._draw_items(model)
        self._draw_player(model)
        self._draw_hud(model)

    def _draw_sky(self, camera_y: float) -> None:
        self._screen.fill(COLOR_BACKGROUND)
        drift = SKY_DRIFT * math.sin(camera_y * SKY_DRIFT_FREQ)
        self._screen.blit(self._sky, (0, int(-SKY_DRIFT + drift)))

    def _draw_ground(self, camera_y: float) -> None:
        screen_top = int(GROUND_TOP_Y - camera_y)
        if screen_top >= SCREEN_HEIGHT:
            return
        y = screen_top
        while y < SCREEN_HEIGHT:
            self._screen.blit(self._ground, (0, y))
            y += self._ground_h

    def _draw_portals(self, model: GameModel) -> None:
        for portal in model.portals:
            self._screen.blit(self._portal_sprite, (int(portal.x), int(portal.y - model.camera_y)))

    def _draw_platform(self, platform: Platform, camera_y: float) -> None:
        sprite = self._platform_sprites[platform.kind]
        self._screen.blit(sprite, (int(platform.x), int(platform.y - camera_y)))

    def _draw_items(self, model: GameModel) -> None:
        for item in model.items:
            sprite = self._coin_sprite if isinstance(item, Coin) else self._elytra_sprite
            self._screen.blit(sprite, (int(item.x), int(item.y - model.camera_y)))

    def _draw_player(self, model: GameModel) -> None:
        player = model.player
        if player.vx < 0:
            self._facing_left = True
        elif player.vx > 0:
            self._facing_left = False
        rising = player.vy < 0  # negative vy means moving upward
        sprite = self._select_player_sprite(rising)
        x = int(player.x + (player.width - sprite.get_width()) / 2)
        y = int(player.bottom - sprite.get_height() - model.camera_y)
        self._screen.blit(sprite, (x, y))

    def _select_player_sprite(self, rising: bool) -> pygame.Surface:
        if rising:
            return self._player_jump_left if self._facing_left else self._player_jump
        return self._player_idle_left if self._facing_left else self._player_idle

    def _draw_hud(self, model: GameModel) -> None:
        score_text = self._font.render(f"Счёт: {model.score}", True, COLOR_TEXT)
        self._screen.blit(score_text, (16, 12))
        coin_text = self._font.render(f"Монеты: {model.coins}", True, COLOR_TEXT)
        self._screen.blit(coin_text, (16, 48))
