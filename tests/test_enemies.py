import random
import unittest

from src.config.constants import SKELETON_HP, SPIDER_HP, ZOMBIE_HP
from src.models.entities import Projectile, Skeleton, Spider, WeaponKind, Zombie
from src.models.game_model import GameModel
from src.models.level_generator import LevelGenerator


class EnemyHealthTests(unittest.TestCase):
    def test_zombie_needs_two_hits(self) -> None:
        zombie = Zombie(x=0.0, y=0.0)
        self.assertEqual(zombie.hp, ZOMBIE_HP)
        zombie.hit()
        self.assertTrue(zombie.alive)
        zombie.hit()
        self.assertFalse(zombie.alive)

    def test_spider_dies_in_one_hit(self) -> None:
        spider = Spider(x=0.0, y=0.0)
        self.assertEqual(spider.hp, SPIDER_HP)
        spider.hit()
        self.assertFalse(spider.alive)

    def test_skeleton_needs_three_hits(self) -> None:
        skeleton = Skeleton(x=0.0, y=0.0)
        self.assertEqual(skeleton.hp, SKELETON_HP)
        for _ in range(2):
            skeleton.hit()
        self.assertTrue(skeleton.alive)
        skeleton.hit()
        self.assertFalse(skeleton.alive)


class EnemyMovementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = GameModel(rng=random.Random(1))

    def test_spider_bounces_off_right_edge(self) -> None:
        spider = Spider(x=1000.0, y=0.0, vx=100.0)
        spider.update(0.1, self.model)
        self.assertLess(spider.vx, 0)  # turned around at the wall

    def test_skeleton_patrols_within_bounds(self) -> None:
        skeleton = Skeleton(x=0.0, y=0.0, vy=200.0, min_y=-50.0, max_y=50.0)
        for _ in range(200):
            skeleton.update(0.05, self.model)
            self.assertGreaterEqual(skeleton.y, skeleton.min_y - 1)
            self.assertLessEqual(skeleton.y, skeleton.max_y + 1)

    def test_skeleton_shoots_periodically(self) -> None:
        skeleton = Skeleton(x=0.0, y=0.0, direction=1, min_y=-100.0, max_y=100.0)
        for _ in range(70):  # ~1.12s, past the 1s cooldown
            skeleton.update(0.016, self.model)
        self.assertGreaterEqual(len(self.model.enemy_projectiles), 1)
        self.assertGreater(self.model.enemy_projectiles[0].vx, 0)  # fires right


class EnemyCombatTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = GameModel(rng=random.Random(1))

    def test_player_shot_hits_enemy(self) -> None:
        enemy = Zombie(x=self.model.player.x, y=self.model.player.y)
        shot = Projectile(x=self.model.player.x, y=self.model.player.y, weapon=WeaponKind.RIFLE)
        self.model.enemies = [enemy]
        self.model.projectiles = [shot]
        self.model._hit_enemies_with_projectiles()
        self.assertEqual(enemy.hp, ZOMBIE_HP - 1)
        self.assertFalse(shot.alive)

    def test_contact_with_enemy_kills_player(self) -> None:
        self.model.enemies = [Zombie(x=self.model.player.x, y=self.model.player.y)]
        self.model.update(0.016, move_dir=0)
        self.assertTrue(self.model.is_game_over)

    def test_enemy_arrow_kills_player(self) -> None:
        arrow = Projectile(x=self.model.player.x, y=self.model.player.y, vx=0.0)
        self.model.enemy_projectiles = [arrow]
        self.model.update(0.016, move_dir=0)
        self.assertTrue(self.model.is_game_over)


class EnemySpawnTests(unittest.TestCase):
    def test_no_enemies_before_min_height(self) -> None:
        generator = LevelGenerator(rng=random.Random(5))
        for _ in range(50):
            self.assertIsNone(generator.maybe_enemy(near_y=-100.0, height_climbed=0.0))

    def test_skeleton_spawns_at_edge_facing_inward(self) -> None:
        generator = LevelGenerator(rng=random.Random(5))
        skeleton = generator._make_skeleton(near_y=-1000.0)
        on_left = skeleton.x == 0.0
        if on_left:
            self.assertEqual(skeleton.direction, 1)
        else:
            self.assertEqual(skeleton.direction, -1)

    def test_enemies_appear_when_climbing_high(self) -> None:
        model = GameModel(rng=random.Random(2))
        model.camera_y = -60000.0
        model._spawn_above()
        self.assertGreater(len(model.enemies), 0)


if __name__ == "__main__":
    unittest.main()
