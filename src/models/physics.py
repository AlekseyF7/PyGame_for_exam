"""Physics helpers: integration, wrap-around, one-way landing (no pygame)."""

from src.config.constants import GRAVITY
from src.models.entities import Platform, Player


def max_jump_height(jump_velocity: float, gravity: float = GRAVITY) -> float:
    """Peak height reachable from a jump (used to keep platforms reachable)."""
    return (jump_velocity * jump_velocity) / (2.0 * gravity)


def integrate(player: Player, dt: float, gravity: float = GRAVITY) -> None:
    """Semi-implicit Euler integration; FPS-independent via dt."""
    player.vy += gravity * dt
    player.x += player.vx * dt
    player.y += player.vy * dt


def wrap_horizontal(player: Player, screen_width: int) -> None:
    """Player leaving one side reappears on the opposite side."""
    if player.right < 0:
        player.x = screen_width
    elif player.left > screen_width:
        player.x = -player.width


def try_land(player: Player, platform: Platform, prev_bottom: float) -> bool:
    """Land only while falling and crossing the platform top from above."""
    if player.vy <= 0 or not platform.alive:
        return False
    crossed_top = prev_bottom <= platform.top <= player.bottom
    if crossed_top and player.overlaps_x(platform):
        player.y = platform.top - player.height
        player.vy = platform.bounce_velocity()
        platform.on_landed()
        return True
    return False
