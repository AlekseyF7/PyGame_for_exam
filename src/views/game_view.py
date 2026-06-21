"""Rendering of the gameplay scene (sky, ground, items, weapons, player, HUD)."""

import math

import pygame

from src.config.constants import (
    COIN_SIZE,
    COLOR_BACKGROUND,
    COLOR_TEXT,
    ELYTRA_SIZE,
    ENEMY_SIZE,
    FONT_SIZE_NORMAL,
    GROUND_TOP_Y,
    IMAGE_BACKGROUND,
    IMAGE_COIN,
    IMAGE_ELYTRA,
    IMAGE_ENEMY_SKELETON,
    IMAGE_ENEMY_SPIDER,
    IMAGE_ENEMY_ZOMBIE,
    IMAGE_GROUND,
    IMAGE_PLATFORM_BREAKABLE,
    IMAGE_PLATFORM_MOVING,
    IMAGE_PLATFORM_SPRING,
    IMAGE_PLATFORM_STATIC,
    IMAGE_PLAYER,
    IMAGE_PLAYER_BOW,
    IMAGE_PLAYER_BOW_JUMP,
    IMAGE_PLAYER_JUMP,
    IMAGE_PLAYER_PISTOL,
    IMAGE_PLAYER_PISTOL_JUMP,
    IMAGE_PLAYER_RIFLE,
    IMAGE_PLAYER_RIFLE_JUMP,
    IMAGE_PORTAL,
    IMAGE_PROJECTILE_BOW,
    IMAGE_PROJECTILE_PISTOL,
    IMAGE_PROJECTILE_RIFLE,
    IMAGE_WEAPON_BOW,
    IMAGE_WEAPON_PISTOL,
    IMAGE_WEAPON_RIFLE,
    PLATFORM_HEIGHT,
    PLATFORM_WIDTH,
    PLAYER_WIDTH,
    PORTAL_SIZE,
    PROJECTILE_HEIGHT,
    PROJECTILE_WIDTH,
    SKY_DRIFT,
    SKY_DRIFT_FREQ,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WEAPON_SIZE,
)
from src.models.entities import (
    Coin,
    Platform,
    PlatformKind,
    Skeleton,
    Spider,
    Weapon,
    WeaponKind,
    Zombie,
)
from src.models.game_model import GameModel
from src.views.assets import AssetManager

_PLATFORM_IMAGES = {
    PlatformKind.STATIC: IMAGE_PLATFORM_STATIC,
    PlatformKind.MOVING: IMAGE_PLATFORM_MOVING,
    PlatformKind.BREAKABLE: IMAGE_PLATFORM_BREAKABLE,
    PlatformKind.SPRING: IMAGE_PLATFORM_SPRING,
}

_WEAPON_PICKUP_IMAGES = {
    WeaponKind.BOW: IMAGE_WEAPON_BOW,
    WeaponKind.PISTOL: IMAGE_WEAPON_PISTOL,
    WeaponKind.RIFLE: IMAGE_WEAPON_RIFLE,
}

_PROJECTILE_IMAGES = {
    WeaponKind.BOW: IMAGE_PROJECTILE_BOW,
    WeaponKind.PISTOL: IMAGE_PROJECTILE_PISTOL,
    WeaponKind.RIFLE: IMAGE_PROJECTILE_RIFLE,
}

# Player poses per weapon (None = unarmed). Each entry: (idle_image, jump_image).
_PLAYER_POSE_IMAGES = {
    None: (IMAGE_PLAYER, IMAGE_PLAYER_JUMP),
    WeaponKind.BOW: (IMAGE_PLAYER_BOW, IMAGE_PLAYER_BOW_JUMP),
    WeaponKind.PISTOL: (IMAGE_PLAYER_PISTOL, IMAGE_PLAYER_PISTOL_JUMP),
    WeaponKind.RIFLE: (IMAGE_PLAYER_RIFLE, IMAGE_PLAYER_RIFLE_JUMP),
}

_WEAPON_NAMES = {
    WeaponKind.BOW: "Лук",
    WeaponKind.PISTOL: "Пистолет",
    WeaponKind.RIFLE: "Автомат",
}

_ENEMY_IMAGES = {
    Zombie: IMAGE_ENEMY_ZOMBIE,
    Spider: IMAGE_ENEMY_SPIDER,
    Skeleton: IMAGE_ENEMY_SKELETON,
}


class GameView:
    def __init__(self, screen: pygame.Surface, assets: AssetManager) -> None:
        self._screen = screen
        self._assets = assets
        self._font = assets.font(FONT_SIZE_NORMAL)
        self._facing_left = False
        self._load_sprites(assets)

    def _load_sprites(self, assets: AssetManager) -> None:
        self._sky = assets.image(
            IMAGE_BACKGROUND, size=(SCREEN_WIDTH, SCREEN_HEIGHT + 2 * SKY_DRIFT), smooth=True
        )
        self._ground = self._scale_to_width(IMAGE_GROUND, SCREEN_WIDTH, smooth=True)
        self._ground_h = self._ground.get_height()

        # Player poses: build idle/jump (+ flipped) for each weapon state.
        self._player_poses = {
            weapon: self._build_pose_set(idle_name, jump_name)
            for weapon, (idle_name, jump_name) in _PLAYER_POSE_IMAGES.items()
        }

        platform_size = (PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self._platform_sprites = {
            kind: assets.image(name, size=platform_size, smooth=False)
            for kind, name in _PLATFORM_IMAGES.items()
        }

        self._coin_sprite = assets.image(IMAGE_COIN, size=(COIN_SIZE, COIN_SIZE), smooth=False)
        self._elytra_sprite = assets.image(IMAGE_ELYTRA, size=(ELYTRA_SIZE, ELYTRA_SIZE), smooth=False)
        self._portal_sprite = assets.image(IMAGE_PORTAL, size=(PORTAL_SIZE, PORTAL_SIZE), smooth=False)

        weapon_size = (WEAPON_SIZE, WEAPON_SIZE)
        self._weapon_pickup_sprites = {
            kind: assets.image(name, size=weapon_size, smooth=False)
            for kind, name in _WEAPON_PICKUP_IMAGES.items()
        }
        projectile_size = (PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
        self._projectile_sprites = {
            kind: assets.image(name, size=projectile_size, smooth=False)
            for kind, name in _PROJECTILE_IMAGES.items()
        }

        enemy_size = (ENEMY_SIZE, ENEMY_SIZE)
        self._enemy_sprites = {
            cls: assets.image(name, size=enemy_size, smooth=False)
            for cls, name in _ENEMY_IMAGES.items()
        }

    def _build_pose_set(self, idle_name: str, jump_name: str) -> dict[str, pygame.Surface]:
        idle = self._scale_to_width(idle_name, PLAYER_WIDTH, smooth=False)
        jump = self._scale_to_width(jump_name, PLAYER_WIDTH, smooth=False)
        return {
            "idle": idle,
            "jump": jump,
            "idle_left": pygame.transform.flip(idle, True, False),
            "jump_left": pygame.transform.flip(jump, True, False),
        }

    def _scale_to_width(self, name: str, target_width: int, smooth: bool) -> pygame.Surface:
        natural = self._assets.image(name)
        ratio = natural.get_height() / natural.get_width()
        target_height = max(1, int(target_width * ratio))
        return self._assets.image(name, size=(target_width, target_height), smooth=smooth)

    def render(self, model: GameModel) -> None:
        self._draw_sky(model.camera_y)
        self._draw_ground(model.camera_y)
        self._draw_portals(model)
        for platform in model.platforms:
            self._draw_platform(platform, model.camera_y)
        self._draw_items(model)
        self._draw_enemies(model)
        self._draw_projectiles(model)
        self._draw_player(model)
        self._draw_hud(model)

    def _draw_sky(self, camera_y: float) -> None:
        self._screen.fill(COLOR_BACKGROUND)
        drift = SKY_DRIFT * math.sin(camera_y * SKY_DRIFT_FREQ)
        self._screen.blit(self._sky, (0, int(-SKY_DRIFT + drift)))

    def _draw_ground(self, camera_y: float) -> None:
        screen_top = int(GROUND_TOP_Y - camera_y)
        if screen_top >= SCREEN_HEIGHT:
            return
        y = screen_top
        while y < SCREEN_HEIGHT:
            self._screen.blit(self._ground, (0, y))
            y += self._ground_h

    def _draw_portals(self, model: GameModel) -> None:
        for portal in model.portals:
            self._screen.blit(self._portal_sprite, (int(portal.x), int(portal.y - model.camera_y)))

    def _draw_platform(self, platform: Platform, camera_y: float) -> None:
        sprite = self._platform_sprites[platform.kind]
        self._screen.blit(sprite, (int(platform.x), int(platform.y - camera_y)))

    def _draw_items(self, model: GameModel) -> None:
        for item in model.items:
            sprite = self._item_sprite(item)
            self._screen.blit(sprite, (int(item.x), int(item.y - model.camera_y)))

    def _item_sprite(self, item: object) -> pygame.Surface:
        if isinstance(item, Weapon):
            return self._weapon_pickup_sprites[item.kind]
        if isinstance(item, Coin):
            return self._coin_sprite
        return self._elytra_sprite

    def _draw_enemies(self, model: GameModel) -> None:
        for enemy in model.enemies:
            sprite = self._enemy_sprites[type(enemy)]
            self._screen.blit(sprite, (int(enemy.x), int(enemy.y - model.camera_y)))

    def _draw_projectiles(self, model: GameModel) -> None:
        for projectile in (*model.projectiles, *model.enemy_projectiles):
            sprite = self._projectile_sprites[projectile.weapon]
            self._screen.blit(sprite, (int(projectile.x), int(projectile.y - model.camera_y)))

    def _draw_player(self, model: GameModel) -> None:
        player = model.player
        if player.vx < 0:
            self._facing_left = True
        elif player.vx > 0:
            self._facing_left = False
        pose = self._player_poses[model.current_weapon]
        rising = player.vy < 0  # negative vy means moving upward
        key = "jump" if rising else "idle"
        if self._facing_left:
            key += "_left"
        sprite = pose[key]
        x = int(player.x + (player.width - sprite.get_width()) / 2)
        y = int(player.bottom - sprite.get_height() - model.camera_y)
        self._screen.blit(sprite, (x, y))

    def _draw_hud(self, model: GameModel) -> None:
        score_text = self._font.render(f"Счёт: {model.score}", True, COLOR_TEXT)
        self._screen.blit(score_text, (16, 12))
        coin_text = self._font.render(f"Монеты: {model.coins}", True, COLOR_TEXT)
        self._screen.blit(coin_text, (16, 48))
        weapon_name = _WEAPON_NAMES.get(model.current_weapon, "нет")
        weapon_text = self._font.render(f"Оружие: {weapon_name}", True, COLOR_TEXT)
        self._screen.blit(weapon_text, (16, 84))