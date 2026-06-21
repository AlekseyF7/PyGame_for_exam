"""Game entities as pure data + geometry (no pygame)."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

from src.config.constants import (
    COIN_SIZE,
    ELYTRA_SIZE,
    JUMP_VELOCITY,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
    PLATFORM_HEIGHT,
    PLATFORM_WIDTH,
    PORTAL_SIZE,
    SPRING_JUMP_VELOCITY,
)

if TYPE_CHECKING:
    from src.models.game_model import GameModel


class PlatformKind(Enum):
    STATIC = auto()
    MOVING = auto()
    BREAKABLE = auto()
    SPRING = auto()


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
