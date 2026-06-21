"""Game entities as pure data + geometry (no pygame)."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

from src.config.constants import (
    BOW_COOLDOWN,
    COIN_SIZE,
    ELYTRA_SIZE,
    ENEMY_SIZE,
    JUMP_VELOCITY,
    PISTOL_COOLDOWN,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
    PLATFORM_HEIGHT,
    PLATFORM_WIDTH,
    PORTAL_SIZE,
    PROJECTILE_HEIGHT,
    PROJECTILE_WIDTH,
    RIFLE_COOLDOWN,
    SCREEN_WIDTH,
    SKELETON_ARROW_SPEED,
    SKELETON_HP,
    SKELETON_SHOOT_COOLDOWN,
    SKELETON_SPEED,
    SPIDER_HP,
    SPIDER_SPEED,
    SPRING_JUMP_VELOCITY,
    WEAPON_HEIGHT_BOW,
    WEAPON_HEIGHT_PISTOL,
    WEAPON_HEIGHT_RIFLE,
    WEAPON_SIZE,
    ZOMBIE_HP,
)

if TYPE_CHECKING:
    from src.models.game_model import GameModel


class PlatformKind(Enum):
    STATIC = auto()
    MOVING = auto()
    BREAKABLE = auto()
    SPRING = auto()


class WeaponKind(Enum):
    BOW = auto()
    PISTOL = auto()
    RIFLE = auto()

    @property
    def cooldown(self) -> float:
        return _WEAPON_COOLDOWNS[self]

    @property
    def spawn_height(self) -> int:
        return _WEAPON_SPAWN_HEIGHTS[self]


_WEAPON_COOLDOWNS = {
    WeaponKind.BOW: BOW_COOLDOWN,
    WeaponKind.PISTOL: PISTOL_COOLDOWN,
    WeaponKind.RIFLE: RIFLE_COOLDOWN,
}

_WEAPON_SPAWN_HEIGHTS = {
    WeaponKind.BOW: WEAPON_HEIGHT_BOW,
    WeaponKind.PISTOL: WEAPON_HEIGHT_PISTOL,
    WeaponKind.RIFLE: WEAPON_HEIGHT_RIFLE,
}


class _AxisAlignedBox:
    """Mixin providing AABB edges from (x, y, width, height)."""

    x: float
    y: float
    width: float
    height: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2

    def overlaps_x(self, other: "_AxisAlignedBox") -> bool:
        return self.left < other.right and self.right > other.left

    def overlaps(self, other: "_AxisAlignedBox") -> bool:
        return (
            self.left < other.right
            and self.right > other.left
            and self.top < other.bottom
            and self.bottom > other.top
        )


@dataclass
class Player(_AxisAlignedBox):
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    width: float = PLAYER_WIDTH
    height: float = PLAYER_HEIGHT


@dataclass
class Platform(_AxisAlignedBox):
    x: float
    y: float
    kind: PlatformKind = PlatformKind.STATIC
    vx: float = 0.0
    alive: bool = True
    width: float = PLATFORM_WIDTH
    height: float = PLATFORM_HEIGHT

    def bounce_velocity(self) -> float:
        """Upward velocity given to a player landing on this platform."""
        if self.kind is PlatformKind.SPRING:
            return SPRING_JUMP_VELOCITY
        return JUMP_VELOCITY

    def on_landed(self) -> None:
        """Hook applied when a player lands; breakable platforms disappear."""
        if self.kind is PlatformKind.BREAKABLE:
            self.alive = False


@dataclass
class Collectible(_AxisAlignedBox, ABC):
    """Base class for items the player can pick up (OOP polymorphism)."""

    x: float
    y: float
    collected: bool = False
    width: float = COIN_SIZE
    height: float = COIN_SIZE

    @abstractmethod
    def apply(self, model: "GameModel") -> None:
        """Apply this item's effect to the game model when picked up."""
        raise NotImplementedError


@dataclass
class Coin(Collectible):
    width: float = COIN_SIZE
    height: float = COIN_SIZE

    def apply(self, model: "GameModel") -> None:
        model.add_coin()


@dataclass
class Elytra(Collectible):
    width: float = ELYTRA_SIZE
    height: float = ELYTRA_SIZE

    def apply(self, model: "GameModel") -> None:
        model.start_flight()


@dataclass
class Portal(_AxisAlignedBox):
    """Deadly hazard near a screen edge; touching it ends the run."""

    x: float
    y: float
    width: float = PORTAL_SIZE
    height: float = PORTAL_SIZE


@dataclass
class Weapon(Collectible):
    """A weapon pickup lying on a platform; equips the player when collected."""

    kind: WeaponKind = WeaponKind.BOW
    width: float = WEAPON_SIZE
    height: float = WEAPON_SIZE

    def apply(self, model: "GameModel") -> None:
        model.equip_weapon(self.kind)


@dataclass
class Projectile(_AxisAlignedBox):
    """A shot. Player shots fly up; enemy shots fly sideways."""

    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    weapon: WeaponKind = WeaponKind.BOW
    alive: bool = True
    width: float = PROJECTILE_WIDTH
    height: float = PROJECTILE_HEIGHT


@dataclass
class Enemy(_AxisAlignedBox, ABC):
    """Base enemy: kills the player on contact and has hit-point health."""

    x: float
    y: float
    hp: int = 1
    alive: bool = True
    width: float = ENEMY_SIZE
    height: float = ENEMY_SIZE

    def hit(self) -> None:
        """Take one shot, regardless of weapon type."""
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False

    @abstractmethod
    def update(self, dt: float, model: "GameModel") -> None:
        """Advance behaviour (movement / shooting) by dt seconds."""
        raise NotImplementedError


@dataclass
class Zombie(Enemy):
    """Static enemy; just stands where it spawned."""

    hp: int = ZOMBIE_HP

    def update(self, dt: float, model: "GameModel") -> None:
        return None


@dataclass
class Spider(Enemy):
    """Moves horizontally and bounces off the screen edges."""

    hp: int = SPIDER_HP
    vx: float = SPIDER_SPEED

    def update(self, dt: float, model: "GameModel") -> None:
        self.x += self.vx * dt
        if self.x <= 0:
            self.x = 0.0
            self.vx = abs(self.vx)
        elif self.x + self.width >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
            self.vx = -abs(self.vx)


@dataclass
class Skeleton(Enemy):
    """Edge enemy: patrols vertically and shoots arrows horizontally."""

    hp: int = SKELETON_HP
    vy: float = SKELETON_SPEED
    direction: int = 1            # +1 shoots right, -1 shoots left
    min_y: float = 0.0
    max_y: float = 0.0
    arrow_speed: float = SKELETON_ARROW_SPEED
    shoot_cooldown: float = SKELETON_SHOOT_COOLDOWN
    _shoot_timer: float = SKELETON_SHOOT_COOLDOWN

    def update(self, dt: float, model: "GameModel") -> None:
        self.y += self.vy * dt
        if self.y <= self.min_y:
            self.y = self.min_y
            self.vy = abs(self.vy)
        elif self.y >= self.max_y:
            self.y = self.max_y
            self.vy = -abs(self.vy)

        self._shoot_timer -= dt
        if self._shoot_timer <= 0.0:
            self._shoot_timer += self.shoot_cooldown
            model.spawn_enemy_projectile(
                self.center_x, self.center_y, self.direction * self.arrow_speed
            )
