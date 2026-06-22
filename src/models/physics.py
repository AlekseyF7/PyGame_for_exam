"""Помощники физики: интегрирование, переход через край, одностороннее приземление (без pygame)."""

from src.config.constants import GRAVITY
from src.models.entities import Platform, Player


def max_jump_height(jump_velocity: float, gravity: float = GRAVITY) -> float:
    """Максимальная высота прыжка (нужна, чтобы платформы оставались достижимыми)."""
    return (jump_velocity * jump_velocity) / (2.0 * gravity)


def integrate(player: Player, dt: float, gravity: float = GRAVITY) -> None:
    """Полуявное интегрирование Эйлера; не зависит от FPS за счёт dt."""
    player.vy += gravity * dt
    player.x += player.vx * dt
    player.y += player.vy * dt


def wrap_horizontal(player: Player, screen_width: int) -> None:
    """Игрок, ушедший за один край, появляется с противоположного."""
    if player.right < 0:
        player.x = screen_width
    elif player.left > screen_width:
        player.x = -player.width


def try_land(player: Player, platform: Platform, prev_bottom: float) -> bool:
    """Приземление только при падении и пересечении верха платформы сверху."""
    if player.vy <= 0 or not platform.alive:
        return False
    crossed_top = prev_bottom <= platform.top <= player.bottom
    if crossed_top and player.overlaps_x(platform):
        player.y = platform.top - player.height
        player.vy = platform.bounce_velocity()
        platform.on_landed()
        return True
    return False
