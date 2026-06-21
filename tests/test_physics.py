import unittest

from src.config.constants import GRAVITY, JUMP_VELOCITY, SCREEN_WIDTH
from src.models import physics
from src.models.entities import Platform, PlatformKind, Player


class PhysicsTests(unittest.TestCase):
    def test_gravity_increases_downward_velocity(self) -> None:
        player = Player(x=100.0, y=100.0, vy=0.0)
        physics.integrate(player, dt=0.1)
        self.assertAlmostEqual(player.vy, GRAVITY * 0.1)

    def test_wrap_left_to_right(self) -> None:
        player = Player(x=-60.0, y=0.0)
        physics.wrap_horizontal(player, SCREEN_WIDTH)
        self.assertEqual(player.x, SCREEN_WIDTH)

    def test_landing_only_when_falling(self) -> None:
        platform = Platform(x=100.0, y=200.0)
        player = Player(x=110.0, y=190.0, vy=50.0, height=20.0)
        prev_bottom = 195.0  # was above the platform top last frame
        landed = physics.try_land(player, platform, prev_bottom)
        self.assertTrue(landed)
        self.assertEqual(player.vy, JUMP_VELOCITY)

    def test_no_landing_when_moving_up(self) -> None:
        platform = Platform(x=100.0, y=200.0)
        player = Player(x=110.0, y=210.0, vy=-50.0, height=20.0)
        landed = physics.try_land(player, platform, prev_bottom=260.0)
        self.assertFalse(landed)

    def test_spring_gives_stronger_bounce(self) -> None:
        spring = Platform(x=100.0, y=200.0, kind=PlatformKind.SPRING)
        normal = Platform(x=100.0, y=200.0, kind=PlatformKind.STATIC)
        self.assertLess(spring.bounce_velocity(), normal.bounce_velocity())

    def test_breakable_disappears_after_landing(self) -> None:
        platform = Platform(x=100.0, y=200.0, kind=PlatformKind.BREAKABLE)
        player = Player(x=110.0, y=190.0, vy=50.0, height=20.0)
        physics.try_land(player, platform, prev_bottom=195.0)
        self.assertFalse(platform.alive)


if __name__ == "__main__":
    unittest.main()
