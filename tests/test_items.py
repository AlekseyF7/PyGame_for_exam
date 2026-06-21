import random
import unittest

from src.config.constants import ELYTRA_BOOST_HEIGHT
from src.models.entities import Coin, Elytra, Portal
from src.models.game_model import GameModel


class ItemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = GameModel(rng=random.Random(1))

    def test_coin_collection_increments_coins(self) -> None:
        coin = Coin(x=self.model.player.x, y=self.model.player.y)
        self.model.items = [coin]
        self.model.update(0.016, move_dir=0)
        self.assertEqual(self.model.coins, 1)
        self.assertTrue(coin.collected)

    def test_collected_coin_is_removed(self) -> None:
        coin = Coin(x=self.model.player.x, y=self.model.player.y)
        self.model.items = [coin]
        self.model.update(0.016, move_dir=0)
        self.assertEqual(len(self.model.items), 0)

    def test_elytra_starts_flight(self) -> None:
        elytra = Elytra(x=self.model.player.x, y=self.model.player.y)
        self.model.items = [elytra]
        self.model.update(0.016, move_dir=0)
        self.assertTrue(self.model.is_flying)

    def test_flight_lifts_player_up(self) -> None:
        start_y = self.model.player.y
        self.model.start_flight()
        for _ in range(120):
            self.model.update(0.016, move_dir=0)
        self.assertLess(self.model.player.y, start_y)

    def test_flight_stops_after_boost_height(self) -> None:
        start_y = self.model.player.y
        self.model.start_flight()
        for _ in range(600):
            self.model.update(0.016, move_dir=0)
            if not self.model.is_flying:
                break
        climbed = start_y - self.model.player.y
        self.assertGreaterEqual(climbed, ELYTRA_BOOST_HEIGHT - 50)

    def test_portal_kills_player(self) -> None:
        portal = Portal(x=self.model.player.x, y=self.model.player.y)
        self.model.portals = [portal]
        self.model.update(0.016, move_dir=0)
        self.assertTrue(self.model.is_game_over)

    def test_climbing_spawns_items_and_portals(self) -> None:
        self.model.camera_y = -8000.0
        self.model._spawn_above()
        self.assertGreater(len(self.model.items), 0)
        self.assertGreater(len(self.model.portals), 0)


if __name__ == "__main__":
    unittest.main()
