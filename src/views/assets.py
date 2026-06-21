"""Asset loading for the View layer (images, sounds, fonts).

Only the View layer touches pygame and the filesystem for resources.
Missing files are tolerated: images become labelled placeholders and sounds
simply do not play, so the game runs even without final art.
"""

from pathlib import Path

import pygame

from src.config.constants import (
    ASSETS_DIR,
    COLOR_TEXT_DIM,
    FONT_CANDIDATES,
    FONTS_DIR,
    IMAGES_DIR,
    SOUNDS_DIR,
)


class AssetManager:
    def __init__(self, base_dir: str = ASSETS_DIR) -> None:
        self._base = Path(base_dir)
        self._images: dict[tuple[str, tuple[int, int] | None, bool], pygame.Surface] = {}
        self._sounds: dict[str, "pygame.mixer.Sound | None"] = {}
        self._fonts: dict[int, pygame.font.Font] = {}
        self._volume = 1.0

    def image(
        self,
        name: str,
        size: tuple[int, int] | None = None,
        smooth: bool = True,
    ) -> pygame.Surface:
        """Load (and cache) an image. Use smooth=False for crisp pixel-art."""
        key = (name, size, smooth)
        if key not in self._images:
            self._images[key] = self._load_image_or_placeholder(name, size, smooth)
        return self._images[key]

    def sound(self, name: str) -> "pygame.mixer.Sound | None":
        if name not in self._sounds:
            sound = self._load_sound_or_none(name)
            if sound is not None:
                sound.set_volume(self._volume)
            self._sounds[name] = sound
        return self._sounds[name]

    def font(self, size: int) -> pygame.font.Font:
        if size not in self._fonts:
            self._fonts[size] = pygame.font.SysFont(FONT_CANDIDATES, size)
        return self._fonts[size]

    def set_volume(self, volume: float) -> None:
        self._volume = max(0.0, min(1.0, volume))
        for sound in self._sounds.values():
            if sound is not None:
                sound.set_volume(self._volume)

    # Accept a file under any of these extensions, regardless of the name given.
    _IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".bmp")

    def _resolve_image_path(self, name: str) -> Path | None:
        exact = self._base / IMAGES_DIR / name
        if exact.exists():
            return exact
        stem = exact.with_suffix("")
        for ext in self._IMAGE_EXTENSIONS:
            candidate = stem.with_suffix(ext)
            if candidate.exists():
                return candidate
        return None

    def _load_image_or_placeholder(
        self, name: str, size: tuple[int, int] | None, smooth: bool
    ) -> pygame.Surface:
        path = self._resolve_image_path(name)
        if path is not None:
            surface = pygame.image.load(str(path)).convert_alpha()
            if size is not None:
                if smooth:
                    surface = pygame.transform.smoothscale(surface, size)
                else:
                    # Nearest-neighbour keeps pixels crisp (Minecraft style).
                    surface = pygame.transform.scale(surface, size)
            return surface
        return self._make_placeholder(name, size or (64, 64))

    def _load_sound_or_none(self, name: str) -> "pygame.mixer.Sound | None":
        path = self._base / SOUNDS_DIR / name
        if not path.exists() or not pygame.mixer.get_init():
            return None
        try:
            return pygame.mixer.Sound(str(path))
        except pygame.error:
            return None

    @staticmethod
    def _make_placeholder(label: str, size: tuple[int, int]) -> pygame.Surface:
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((200, 200, 210))
        pygame.draw.rect(surface, COLOR_TEXT_DIM, surface.get_rect(), width=2)
        return surface

    def fonts_dir_exists(self) -> bool:
        return (self._base / FONTS_DIR).exists()
