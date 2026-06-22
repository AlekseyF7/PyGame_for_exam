"""Процедурная генерация платформ с гарантией достижимости (без pygame)."""

import random

from src.config.constants import (
    COIN_SIZE,
    COIN_SPAWN_CHANCE,
    ELYTRA_SIZE,
    ELYTRA_SPAWN_CHANCE,
    ENEMY_MIN_HEIGHT,
    ENEMY_SIZE,
    JUMP_VELOCITY,
    MOVING_PLATFORM_SPEED,
    PLATFORM_MAX_GAP_RATIO,
    PLATFORM_MIN_GAP_Y,
    PLATFORM_WIDTH,
    PORTAL_EDGE_MARGIN,
    PORTAL_SIZE,
    PORTAL_SPAWN_CHANCE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SKELETON_SPAWN_CHANCE,
    SPIDER_SPAWN_CHANCE,
    ZOMBIE_SPAWN_CHANCE,
)
from src.models.entities import (
    Coin,
    Elytra,
    Enemy,
    Platform,
    PlatformKind,
    Portal,
    Skeleton,
    Spider,
    Zombie,
)
from src.models.physics import max_jump_height


class LevelGenerator:
    """Создаёт платформы над игроком, сохраняя их достижимость."""

    def __init__(self, screen_width: int = SCREEN_WIDTH, rng: random.Random | None = None) -> None:
        self._screen_width = screen_width
        self._rng = rng or random.Random()
        # Жёсткое ограничение: платформа не выше, чем можно допрыгнуть.
        self._max_gap_y = max_jump_height(JUMP_VELOCITY) * PLATFORM_MAX_GAP_RATIO

    @property
    def max_gap_y(self) -> float:
        return self._max_gap_y

    def random_x(self) -> float:
        return self._rng.uniform(0, self._screen_width - PLATFORM_WIDTH)

    def _pick_kind(self, height_climbed: float) -> PlatformKind:
        """Чем выше поднялся игрок, тем чаще встречаются сложные типы платформ."""
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
        """Создать одну платформу над `highest_y` на достижимом расстоянии."""
        gap = self._rng.uniform(PLATFORM_MIN_GAP_Y, self._max_gap_y)
        new_y = highest_y - gap
        kind = self._pick_kind(height_climbed)
        platform = Platform(x=self.random_x(), y=new_y, kind=kind)
        if kind is PlatformKind.MOVING:
            platform.vx = MOVING_PLATFORM_SPEED
        return platform

    def maybe_item(self, platform: Platform) -> Coin | Elytra | None:
        """Возможно, положить предмет на верх данной платформы."""
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
        """Возможно, поставить смертельный портал у края экрана на данной высоте."""
        if self._rng.random() >= PORTAL_SPAWN_CHANCE:
            return None
        if self._rng.random() < 0.5:
            x = PORTAL_EDGE_MARGIN
        else:
            x = SCREEN_WIDTH - PORTAL_SIZE - PORTAL_EDGE_MARGIN
        return Portal(x=x, y=near_y)

    def maybe_enemy(self, near_y: float, height_score: float) -> Enemy | None:
        """Возможно, создать врага. `height_score` — высота платформы в очках
        (та же шкала, что и счёт на экране), поэтому порог совпадает с высотами
        спавна оружия (1000/2000/5000)."""
        if height_score < ENEMY_MIN_HEIGHT:
            return None
        roll = self._rng.random()
        if roll < ZOMBIE_SPAWN_CHANCE:
            return Zombie(x=self.random_x(), y=near_y)
        if roll < ZOMBIE_SPAWN_CHANCE + SPIDER_SPAWN_CHANCE:
            return Spider(x=self.random_x(), y=near_y)
        if roll < ZOMBIE_SPAWN_CHANCE + SPIDER_SPAWN_CHANCE + SKELETON_SPAWN_CHANCE:
            return self._make_skeleton(near_y)
        return None

    def _make_skeleton(self, near_y: float) -> Skeleton:
        """Скелет держится края и стреляет к центру."""
        if self._rng.random() < 0.5:
            x = 0.0
            direction = 1            # слева — стреляет вправо
        else:
            x = SCREEN_WIDTH - ENEMY_SIZE
            direction = -1           # справа — стреляет влево
        # Вертикальный патруль длиной в высоту экрана с центром в точке спавна.
        min_y = near_y - SCREEN_HEIGHT / 2
        max_y = near_y + SCREEN_HEIGHT / 2
        return Skeleton(x=x, y=near_y, direction=direction, min_y=min_y, max_y=max_y)

    def initial_platforms(self, start_y: float, count: int) -> list[Platform]:
        """Построить первый столбец платформ — все простые и достижимые."""
        platforms = [Platform(x=self._screen_width / 2 - PLATFORM_WIDTH / 2, y=start_y)]
        highest = start_y
        for _ in range(count):
            gap = self._rng.uniform(PLATFORM_MIN_GAP_Y, self._max_gap_y)
            highest -= gap
            platforms.append(Platform(x=self.random_x(), y=highest))
        return platforms
