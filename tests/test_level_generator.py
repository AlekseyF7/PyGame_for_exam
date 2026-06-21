import random
import unittest

from src.config.constants import PLATFORM_MIN_GAP_Y, PLATFORM_WIDTH, SCREEN_WIDTH
from src.models.level_generator import LevelGenerator


class LevelGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = LevelGenerator(SCREEN_WIDTH, rng=random.Random(42))

    def test_platforms_stay_within_screen(self) -> None:
        for _ in range(200):
            x = self.generator.random_x()
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x + PLATFORM_WIDTH, SCREEN_WIDTH)

    def test_next_platform_is_reachable(self) -> None:
        highest = 1000.0
        for _ in range(200):
            platform = self.generator.next_platform(highest)
            gap = highest - platform.y
            self.assertGreaterEqual(gap, PLATFORM_MIN_GAP_Y)
            self.assertLessEqual(gap, self.generator.max_gap_y + 1e-6)
            highest = platform.y

    def test_initial_platforms_count_and_order(self) -> None:
        platforms = self.generator.initial_platforms(start_y=600.0, count=10)
        self.assertEqual(len(platforms), 11)  # base + 10
        ys = [p.y for p in platforms]
        self.assertEqual(ys, sorted(ys, reverse=True))  # each next is higher (smaller y)


if __name__ == "__main__":
    unittest.main()
