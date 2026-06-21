import random
import unittest

from src.config.constants import SCREEN_HEIGHT
from src.models.game_model import GameModel


class GameModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = GameModel(rng=random.Random(7))

    def test_starts_not_game_over(self) -> None:
        self.assertFalse(self.model.is_game_over)
        self.assertEqual(self.model.score, 0)

    def test_score_increases_when_climbing(self) -> None:
        self.model.player.y -= 500  # simulate climbing up
        self.model.update(0.016, move_dir=0)
        self.assertGreater(self.model.score, 0)

    def test_game_over_when_falling_below_screen(self) -> None:
        self.model.player.y = self.model.camera_y + SCREEN_HEIGHT + 50
        self.model.player.vy = 100.0
        self.model.update(0.016, move_dir=0)
        self.assertTrue(self.model.is_game_over)

    def test_update_keeps_platforms_above_camera(self) -> None:
        for _ in range(120):
            self.model.player.y -= 30
            self.model.update(0.016, move_dir=0)
        self.assertTrue(len(self.model.platforms) > 0)

    def test_reset_restores_initial_state(self) -> None:
        self.model.player.y = 99999
        self.model.update(0.016, move_dir=0)
        self.model.reset()
        self.assertFalse(self.model.is_game_over)
        self.assertEqual(self.model.score, 0)


if __name__ == "__main__":
    unittest.main()
