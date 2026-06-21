import random
import unittest

from src.models.entities import Weapon, WeaponKind
from src.models.game_model import GameModel


class WeaponTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = GameModel(rng=random.Random(1))

    def test_weapon_pickup_equips_player(self) -> None:
        weapon = Weapon(x=self.model.player.x, y=self.model.player.y, kind=WeaponKind.PISTOL)
        self.model.items = [weapon]
        self.model.update(0.016, move_dir=0)
        self.assertIs(self.model.current_weapon, WeaponKind.PISTOL)

    def test_new_weapon_replaces_previous(self) -> None:
        self.model.equip_weapon(WeaponKind.BOW)
        self.model.equip_weapon(WeaponKind.RIFLE)
        self.assertIs(self.model.current_weapon, WeaponKind.RIFLE)

    def test_cannot_shoot_without_weapon(self) -> None:
        self.assertFalse(self.model.try_shoot())
        self.assertEqual(len(self.model.projectiles), 0)

    def test_shooting_spawns_projectile(self) -> None:
        self.model.equip_weapon(WeaponKind.PISTOL)
        self.assertTrue(self.model.try_shoot())
        self.assertEqual(len(self.model.projectiles), 1)
        self.assertLess(self.model.projectiles[0].vy, 0)  # flies up

    def test_cooldown_blocks_rapid_fire(self) -> None:
        self.model.equip_weapon(WeaponKind.PISTOL)
        self.assertTrue(self.model.try_shoot())
        self.assertFalse(self.model.try_shoot())  # still on cooldown
        self.assertEqual(len(self.model.projectiles), 1)

    def test_cooldown_differs_by_weapon(self) -> None:
        self.model.equip_weapon(WeaponKind.BOW)
        self.model.try_shoot()
        bow_cd = self.model.fire_cooldown_remaining
        self.model.equip_weapon(WeaponKind.RIFLE)
        self.model.try_shoot()
        rifle_cd = self.model.fire_cooldown_remaining
        self.assertGreater(bow_cd, rifle_cd)

    def test_cooldown_recovers_over_time(self) -> None:
        self.model.equip_weapon(WeaponKind.RIFLE)  # 0.5s cooldown
        self.model.try_shoot()
        for _ in range(40):  # ~0.64s
            self.model.update(0.016, move_dir=0)
        self.assertEqual(self.model.fire_cooldown_remaining, 0.0)

    def test_projectile_flies_up_and_is_culled(self) -> None:
        self.model.equip_weapon(WeaponKind.RIFLE)
        self.model.try_shoot()
        start_y = self.model.projectiles[0].y
        self.model.update(0.016, move_dir=0)
        self.assertLess(self.model.projectiles[0].y, start_y)
        for _ in range(300):
            self.model.update(0.016, move_dir=0)
            if not self.model.projectiles:
                break
        self.assertEqual(len(self.model.projectiles), 0)

    def test_weapons_spawn_once_at_heights(self) -> None:
        self.model.camera_y = -60000.0  # far above the 5000 height threshold
        self.model._spawn_above()
        spawned = {item.kind for item in self.model.items if isinstance(item, Weapon)}
        self.assertEqual(spawned, set(WeaponKind))
        self.assertEqual(len(self.model._weapons_pending), 0)


if __name__ == "__main__":
    unittest.main()
