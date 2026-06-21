"""Top-level game state for the jumper (pure logic, no pygame)."""

import random

from src.config.constants import (
    CAMERA_FOLLOW_RATIO,
    CULL_MARGIN,
    ELYTRA_BOOST_HEIGHT,
    ELYTRA_FLIGHT_VELOCITY,
    JUMP_VELOCITY,
    MOVE_SPEED,
    PLAYER_START_OFFSET_Y,
    PLAYER_WIDTH,
    PROJECTILE_HEIGHT,
    PROJECTILE_SPEED,
    PROJECTILE_WIDTH,
    SCORE_DIVISOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SPAWN_AHEAD,
    WEAPON_SIZE,
)
from src.models import physics
from src.models.entities import (
    Collectible,
    Enemy,
    Platform,
    PlatformKind,
    Player,
    Portal,
    Projectile,
    Weapon,
    WeaponKind,
)
from src.models.level_generator import LevelGenerator

INITIAL_PLATFORM_COUNT = 12


class GameModel:
    """Holds player, platforms, items, hazards, camera and score."""

    def __init__(self, rng: random.Random | None = None) -> None:
        self._generator = LevelGenerator(SCREEN_WIDTH, rng)
        self.player = Player(x=0.0, y=0.0)
        self.platforms: list[Platform] = []
        self.items: list[Collectible] = []
        self.portals: list[Portal] = []
        self.projectiles: list[Projectile] = []
        self.enemies: list[Enemy] = []
        self.enemy_projectiles: list[Projectile] = []
        self.current_weapon: WeaponKind | None = None
        self.fire_cooldown_remaining = 0.0
        self.camera_y = 0.0
        self.score = 0
        self.coins = 0
        self.is_game_over = False
        self.is_flying = False
        self._flight_target_y = 0.0
        self._start_y = 0.0
        self._weapons_pending: list[WeaponKind] = []
        self.reset()

    def reset(self) -> None:
        start_y = SCREEN_HEIGHT - PLAYER_START_OFFSET_Y
        self.player = Player(
            x=SCREEN_WIDTH / 2 - PLAYER_WIDTH / 2,
            y=start_y,
            vy=JUMP_VELOCITY,
        )
        self.platforms = self._generator.initial_platforms(
            start_y + self.player.height, INITIAL_PLATFORM_COUNT
        )
        self.items = []
        self.portals = []
        self.projectiles = []
        self.enemies = []
        self.enemy_projectiles = []
        self.current_weapon = None
        self.fire_cooldown_remaining = 0.0
        self.camera_y = 0.0
        self.score = 0
        self.coins = 0
        self.is_game_over = False
        self.is_flying = False
        self._flight_target_y = 0.0
        self._start_y = self.player.y
        # Weapons spawn once each, in ascending order of their height.
        self._weapons_pending = sorted(WeaponKind, key=lambda w: w.spawn_height)

    # --- Public effects used by collectibles ---------------------------
    def add_coin(self) -> None:
        self.coins += 1

    def start_flight(self) -> None:
        self.is_flying = True
        self._flight_target_y = self.player.y - ELYTRA_BOOST_HEIGHT

    def equip_weapon(self, kind: WeaponKind) -> None:
        """Equip a weapon; it stays until replaced. Ready to fire at once."""
        self.current_weapon = kind
        self.fire_cooldown_remaining = 0.0

    def try_shoot(self) -> bool:
        """Fire a projectile straight up if a weapon is ready. Returns success."""
        if self.current_weapon is None or self.fire_cooldown_remaining > 0.0:
            return False
        self.projectiles.append(
            Projectile(
                x=self.player.center_x - PROJECTILE_WIDTH / 2,
                y=self.player.top - PROJECTILE_HEIGHT,
                vy=PROJECTILE_SPEED,
                weapon=self.current_weapon,
            )
        )
        self.fire_cooldown_remaining = self.current_weapon.cooldown
        return True

    def spawn_enemy_projectile(self, x: float, y: float, vx: float) -> None:
        """Create a horizontal enemy arrow centred on (x, y)."""
        self.enemy_projectiles.append(
            Projectile(
                x=x - PROJECTILE_WIDTH / 2,
                y=y - PROJECTILE_HEIGHT / 2,
                vx=vx,
                weapon=WeaponKind.BOW,
            )
        )

    # --- Main loop ------------------------------------------------------
    def update(self, dt: float, move_dir: int) -> None:
        if self.is_game_over:
            return

        self.player.vx = move_dir * MOVE_SPEED
        prev_bottom = self.player.bottom

        if self.fire_cooldown_remaining > 0.0:
            self.fire_cooldown_remaining = max(0.0, self.fire_cooldown_remaining - dt)

        if self.is_flying:
            self._fly(dt)
        else:
            physics.integrate(self.player, dt)

        physics.wrap_horizontal(self.player, SCREEN_WIDTH)
        self._update_moving_platforms(dt)
        if not self.is_flying:
            self._resolve_landings(prev_bottom)
        self._collect_items()
        self._update_projectiles(dt)
        self._update_enemies(dt)
        self._hit_enemies_with_projectiles()
        self._follow_camera()
        self._update_score()
        self._recycle_objects()
        self._check_portals()
        self._check_enemy_contact()
        self._check_game_over()

    def _update_projectiles(self, dt: float) -> None:
        for projectile in self.projectiles:
            projectile.x += projectile.vx * dt
            projectile.y += projectile.vy * dt
        # Player shots: keep live ones still on/below the screen top.
        self.projectiles = [
            p for p in self.projectiles if p.alive and p.bottom >= self.camera_y
        ]

        for projectile in self.enemy_projectiles:
            projectile.x += projectile.vx * dt
            projectile.y += projectile.vy * dt
        # Enemy shots: drop those that flew off the sides.
        self.enemy_projectiles = [
            p for p in self.enemy_projectiles if p.alive and p.right > 0 and p.left < SCREEN_WIDTH
        ]

    def _update_enemies(self, dt: float) -> None:
        for enemy in self.enemies:
            enemy.update(dt, self)

    def _hit_enemies_with_projectiles(self) -> None:
        """Each player shot deals one hit; weapon type does not matter."""
        for projectile in self.projectiles:
            if not projectile.alive:
                continue
            for enemy in self.enemies:
                if enemy.alive and projectile.overlaps(enemy):
                    enemy.hit()
                    projectile.alive = False
                    break

    def _check_enemy_contact(self) -> None:
        """Any touch by an enemy or its arrow kills the player instantly."""
        for enemy in self.enemies:
            if enemy.alive and self.player.overlaps(enemy):
                self.is_game_over = True
                return
        for projectile in self.enemy_projectiles:
            if projectile.alive and self.player.overlaps(projectile):
                self.is_game_over = True
                return

    def _fly(self, dt: float) -> None:
        self.player.vy = ELYTRA_FLIGHT_VELOCITY
        self.player.x += self.player.vx * dt
        self.player.y += self.player.vy * dt
        if self.player.y <= self._flight_target_y:
            self.is_flying = False

    def _update_moving_platforms(self, dt: float) -> None:
        for platform in self.platforms:
            if platform.kind is not PlatformKind.MOVING:
                continue
            platform.x += platform.vx * dt
            if platform.left <= 0 or platform.right >= SCREEN_WIDTH:
                platform.vx = -platform.vx

    def _resolve_landings(self, prev_bottom: float) -> None:
        for platform in self.platforms:
            if physics.try_land(self.player, platform, prev_bottom):
                break

    def _collect_items(self) -> None:
        for item in self.items:
            if not item.collected and self.player.overlaps(item):
                item.apply(self)
                item.collected = True

    def _follow_camera(self) -> None:
        threshold = self.camera_y + SCREEN_HEIGHT * CAMERA_FOLLOW_RATIO
        if self.player.y < threshold:
            self.camera_y = self.player.y - SCREEN_HEIGHT * CAMERA_FOLLOW_RATIO

    def _update_score(self) -> None:
        climbed = self._start_y - self.player.y
        self.score = max(self.score, int(climbed / SCORE_DIVISOR))

    def _recycle_objects(self) -> None:
        cull_below = self.camera_y + SCREEN_HEIGHT + CULL_MARGIN
        self.platforms = [p for p in self.platforms if p.alive and p.top < cull_below]
        self.items = [i for i in self.items if not i.collected and i.top < cull_below]
        self.portals = [p for p in self.portals if p.top < cull_below]
        self.enemies = [e for e in self.enemies if e.alive and e.top < cull_below]
        self._spawn_above()

    def _spawn_above(self) -> None:
        spawn_until = self.camera_y - SPAWN_AHEAD
        highest_y = min((p.y for p in self.platforms), default=self.camera_y)
        height_climbed = self._start_y - self.camera_y
        while highest_y > spawn_until:
            platform = self._generator.next_platform(highest_y, height_climbed)
            self.platforms.append(platform)
            item = self._generator.maybe_item(platform)
            if item is not None:
                self.items.append(item)
            portal = self._generator.maybe_portal(platform.y)
            if portal is not None:
                self.portals.append(portal)
            enemy = self._generator.maybe_enemy(platform.y, height_climbed)
            if enemy is not None:
                self.enemies.append(enemy)
            self._maybe_spawn_weapon(platform)
            highest_y = platform.y

    def _maybe_spawn_weapon(self, platform: Platform) -> None:
        """Place the next pending weapon once the platform reaches its height."""
        platform_height = (self._start_y - platform.y) / SCORE_DIVISOR
        while self._weapons_pending and platform_height >= self._weapons_pending[0].spawn_height:
            kind = self._weapons_pending.pop(0)
            x = platform.center_x - WEAPON_SIZE / 2
            y = platform.top - WEAPON_SIZE - 4
            self.items.append(Weapon(x=x, y=y, kind=kind))

    def _check_portals(self) -> None:
        if any(self.player.overlaps(portal) for portal in self.portals):
            self.is_game_over = True

    def _check_game_over(self) -> None:
        if self.player.top > self.camera_y + SCREEN_HEIGHT:
            self.is_game_over = True
