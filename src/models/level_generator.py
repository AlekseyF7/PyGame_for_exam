"""Procedural platform generation with guaranteed reachability (no pygame)."""

import random

from src.config.constants import (
    COIN_SIZE,
    COIN_SPAWN_CHANCE,
    ELYTRA_SIZE,
    ELYTRA_SPAWN_CHANCE,
    JUMP_VELOCITY,
    MOVING_PLATFORM_SPEED,
    PLATFORM_MAX_GAP_RATIO,
    PLATFORM_MIN_GAP_Y,
    PLATFORM_WIDTH,
    PORTAL_EDGE_MARGIN,
    PORTAL_SIZE,
    PORTAL_SPAWN_CHANCE,
    SCREEN_WIDTH,
)
from src.models.entities import Coin, Elytra, Platform, PlatformKind, Portal
from src.models.physics import max_jump_height


class LevelGenerator:
    """Creates platforms above the player while keeping each one reachable."""

    def __init__(self, screen_width: int = SCREEN_WIDTH, rng: random.Random | None = None) -> None:
        self._screen_width = screen_width
        self._rng = rng or random.Random()
        # Hard constraint: never place a platform higher than a jump can reach.
        self._max_gap_y = max_jump_height(JUMP_VELOCITY) * PLATFORM_MAX_GAP_RATIO

    @property
    def max_gap_y(self) -> float:
        return self._max_gap_y

    def random_x(self) -> float:
        return self._rng.uniform(0, self._screen_width - PLATFORM_WIDTH)

    def _pick_kind(self, height_climbed: float) -> PlatformKind:
        """Harder platform types become more likely the higher you climb."""
        difficulty = min(height_climbed / 5000.0, 1.0)
        roll = self._rng.random()
        if roll < 0.10 + 0.10 * difficulty:
            return PlatformKind.MOVING
        if roll < 0.18 + 0.17 * difficulty:
            return PlatformKind.BREAKABLE
        if roll < 0.24:
            return PlatformKind.SPRING
        return PlatformKind.STATIC

    def next_platform(self, highest_y: float, height_climbed: float = 0.0) -> Platform:
        """Spawn one platform above `highest_y` within reachable distance."""
        gap = self._rng.uniform(PLATFORM_MIN_GAP_Y, self._max_gap_y)
        new_y = highest_y - gap
        kind = self._pick_kind(height_climbed)
        platform = Platform(x=self.random_x(), y=new_y, kind=kind)
        if kind is PlatformKind.MOVING:
            platform.vx = MOVING_PLATFORM_SPEED
        return platform

    def maybe_item(self, platform: Platform) -> Coin | Elytra | None:
        """Maybe place a collectible sitting on top of the given platform."""
        roll = self._rng.random()
        if roll < ELYTRA_SPAWN_CHANCE:
            return self._item_on(platform, Elytra, ELYTRA_SIZE)
        if roll < ELYTRA_SPAWN_CHANCE + COIN_SPAWN_CHANCE:
            return self._item_on(platform, Coin, COIN_SIZE)
        return None

    @staticmethod
    def _item_on(platform: Platform, item_cls: type, size: int) -> Coin | Elytra:
        x = platform.center_x - size / 2
        y = platform.top - size - 4
        return item_cls(x=x, y=y)

    def maybe_portal(self, near_y: float) -> Portal | None:
        """Maybe place a deadly portal near a screen edge at the given height."""
        if self._rng.random() >= PORTAL_SPAWN_CHANCE:
            return None
        if self._rng.random() < 0.5:
            x = PORTAL_EDGE_MARGIN
        else:
            x = SCREEN_WIDTH - PORTAL_SIZE - PORTAL_EDGE_MARGIN
        return Portal(x=x, y=near_y)

    def initial_platforms(self, start_y: float, count: int) -> list[Platform]:
        """Build the first column of platforms, all easy and reachable."""
        platforms = [Platform(x=self._screen_width / 2 - PLATFORM_WIDTH / 2, y=start_y)]
        highest = start_y
        for _ in range(count):
            gap = self._rng.uniform(PLATFORM_MIN_GAP_Y, self._max_gap_y)
            highest -= gap
            platforms.append(Platform(x=self.random_x(), y=highest))
        return platforms
