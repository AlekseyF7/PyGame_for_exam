"""Загрузка ресурсов для слоя View (картинки, звуки, шрифты).

Только слой View работает с pygame и файлами ресурсов.
Отсутствующие файлы не ломают игру: вместо картинки рисуется заглушка,
а звук просто не проигрывается — игра запускается даже без финальной графики.
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
        self._fonts: dict[tuple[int, bool], pygame.font.Font] = {}
        self._volume = 1.0

    def image(
        self,
        name: str,
        size: tuple[int, int] | None = None,
        smooth: bool = True,
    ) -> pygame.Surface:
        """Загрузить (и закэшировать) картинку. smooth=False — для чёткого пиксель-арта."""
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

    def font(self, size: int, bold: bool = False) -> pygame.font.Font:
        key = (size, bold)
        if key not in self._fonts:
            self._fonts[key] = pygame.font.SysFont(FONT_CANDIDATES, size, bold=bold)
        return self._fonts[key]

    def play_music(self, name: str, volume: float = 1.0, loop: bool = True) -> None:
        """Зациклить фоновую музыку. Если файла/звука нет — тихо ничего не делаем."""
        if not pygame.mixer.get_init():
            return
        path = self._resolve_sound_path(name)
        if path is None:
            return
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1 if loop else 0)
        except pygame.error:
            return

    def set_volume(self, volume: float) -> None:
        self._volume = max(0.0, min(1.0, volume))
        for sound in self._sounds.values():
            if sound is not None:
                sound.set_volume(self._volume)

    # Принимаем файл с любым из этих расширений, независимо от заданного имени.
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
                    # Ближайший сосед сохраняет чёткие пиксели (стиль Minecraft).
                    surface = pygame.transform.scale(surface, size)
            return surface
        return self._make_placeholder(name, size or (64, 64))

    # Принимаем звук с любым из этих расширений, независимо от заданного имени.
    _SOUND_EXTENSIONS = (".ogg", ".mp3", ".wav")

    def _resolve_sound_path(self, name: str) -> Path | None:
        exact = self._base / SOUNDS_DIR / name
        if exact.exists():
            return exact
        stem = exact.with_suffix("")
        for ext in self._SOUND_EXTENSIONS:
            candidate = stem.with_suffix(ext)
            if candidate.exists():
                return candidate
        return None

    def _load_sound_or_none(self, name: str) -> "pygame.mixer.Sound | None":
        path = self._resolve_sound_path(name)
        if path is None or not pygame.mixer.get_init():
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
