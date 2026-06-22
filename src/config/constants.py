"""Константы всего проекта (чтобы в коде не было «магических чисел»)."""

# --- Окно -----------------------------------------------------------------
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Jump or die"

# --- Физика (координаты экрана: y растёт вниз) ----------------------------
GRAVITY = 2000.0          # пикс/с^2
JUMP_VELOCITY = -900.0    # пикс/с (минус = вверх)
SPRING_JUMP_VELOCITY = -1500.0
MOVE_SPEED = 360.0        # пикс/с по горизонтали

# --- Игрок ----------------------------------------------------------------
PLAYER_WIDTH = 56
PLAYER_HEIGHT = 56
PLAYER_START_OFFSET_Y = 120  # расстояние от низа экрана в начале игры

# --- Платформы ------------------------------------------------------------
PLATFORM_WIDTH = 70
PLATFORM_HEIGHT = 20
PLATFORM_MIN_GAP_Y = 70           # минимальное расстояние между платформами по вертикали
PLATFORM_MAX_GAP_RATIO = 0.85     # максимальный зазор как доля от досягаемой высоты прыжка
MOVING_PLATFORM_SPEED = 90.0      # пикс/с

# --- Предметы и опасности -------------------------------------------------
COIN_SIZE = 28
COIN_SPAWN_CHANCE = 0.25          # шанс, что на новой платформе будет монета
ELYTRA_SIZE = 36
ELYTRA_SPAWN_CHANCE = 0.04        # редко
ELYTRA_FLIGHT_VELOCITY = -700.0   # скорость вверх во время полёта (пикс/с)
ELYTRA_BOOST_HEIGHT = 700.0       # на сколько пикселей элитры поднимают игрока

PORTAL_SIZE = 64
PORTAL_SPAWN_CHANCE = 0.06        # шанс поставить портал у края
PORTAL_EDGE_MARGIN = 4            # насколько близко к краю экрана стоит портал

# --- Оружие и стрельба ----------------------------------------------------
WEAPON_SIZE = 36

# Каждое оружие появляется один раз, когда набранная высота (= счёт) достигает значения.
WEAPON_HEIGHT_BOW = 1000
WEAPON_HEIGHT_PISTOL = 2000
WEAPON_HEIGHT_RIFLE = 5000

# Перезарядка для каждого оружия (секунд между выстрелами).
BOW_COOLDOWN = 3.0
PISTOL_COOLDOWN = 1.0
RIFLE_COOLDOWN = 0.5

# Снаряды игрока летят строго вверх.
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 24
PROJECTILE_SPEED = -900.0         # скорость вверх (пикс/с)

# --- Враги ----------------------------------------------------------------
ENEMY_SIZE = 64
ENEMY_MIN_HEIGHT = 1000           # в очках; враги появляются как и оружие

# Очки здоровья (сколько выстрелов нужно, чтобы убить), не зависит от типа оружия.
ZOMBIE_HP = 2
SPIDER_HP = 1
SKELETON_HP = 3

# Скорости движения (пикс/с).
SPIDER_SPEED = 90.0               # патруль по горизонтали, как у движущейся платформы
SKELETON_SPEED = 70.0             # патруль по вертикали

# Стрельба скелета.
SKELETON_SHOOT_COOLDOWN = 2.0     # секунд между стрелами
SKELETON_ARROW_SPEED = 320.0      # скорость стрелы по горизонтали (пикс/с)

# Шансы спавна на каждую сгенерированную платформу (зомби часто, паук реже, скелет редко).
# Суммарно ~17% на платформу, поэтому враги появляются регулярно, но не на каждом шаге.
ZOMBIE_SPAWN_CHANCE = 0.10
SPIDER_SPAWN_CHANCE = 0.05
SKELETON_SPAWN_CHANCE = 0.02

# --- Камера и счёт --------------------------------------------------------
CAMERA_FOLLOW_RATIO = 0.4         # держим игрока на 40% от верха экрана
SCORE_DIVISOR = 10.0              # сколько мировых пикселей на одно очко
SPAWN_AHEAD = 200                 # насколько выше камеры продолжать спавн
CULL_MARGIN = 80                  # на сколько пикселей ниже экрана удалять платформу

# --- Ресурсы --------------------------------------------------------------
ASSETS_DIR = "assets"
IMAGES_DIR = "images"
SOUNDS_DIR = "sounds"
FONTS_DIR = "fonts"
FONT_CANDIDATES = "arialunicodems,arial,dejavusans,freesans,liberationsans"
FONT_SIZE_TITLE = 64
FONT_SIZE_NORMAL = 32
FONT_SIZE_SMALL = 24

# Имена файлов картинок (лежат в assets/images/). Если файла нет — рисуется
# простая заглушка, поэтому графику можно добавлять постепенно.
IMAGE_PLAYER = "player.png"            # поза стоя / падение
IMAGE_PLAYER_JUMP = "player_jump.png"  # поза подъёма / прыжка
IMAGE_BACKGROUND = "background.png"     # небо (растягивается на весь экран)
IMAGE_GROUND = "ground.png"            # полоса земли в начале игры
IMAGE_MENU_BACKGROUND = "menu_bg.png"  # фон главного меню

# Спрайты платформ по типам (выбираются по PlatformKind во view).
IMAGE_PLATFORM_STATIC = "platform_static.png"
IMAGE_PLATFORM_MOVING = "platform_moving.png"
IMAGE_PLATFORM_BREAKABLE = "platform_breakable.png"
IMAGE_PLATFORM_SPRING = "platform_spring.png"

# Предметы и опасности.
IMAGE_COIN = "coin.png"
IMAGE_ELYTRA = "elytra.png"
IMAGE_PORTAL = "portal.png"

# Оружие-пикапы (лежат на платформах).
IMAGE_WEAPON_BOW = "weapon_bow.png"
IMAGE_WEAPON_PISTOL = "weapon_pistol.png"
IMAGE_WEAPON_RIFLE = "weapon_rifle.png"

# Снаряды / патроны.
IMAGE_PROJECTILE_BOW = "arrow.png"
IMAGE_PROJECTILE_PISTOL = "bullet.png"
IMAGE_PROJECTILE_RIFLE = "bullet.png"

# Игрок с оружием в руках (позы стоя + прыжок). Если файла нет — берётся
# обычный спрайт игрока.
IMAGE_PLAYER_BOW = "player_bow.png"
IMAGE_PLAYER_BOW_JUMP = "player_bow_jump.png"
IMAGE_PLAYER_PISTOL = "player_pistol.png"
IMAGE_PLAYER_PISTOL_JUMP = "player_pistol_jump.png"
IMAGE_PLAYER_RIFLE = "player_rifle.png"
IMAGE_PLAYER_RIFLE_JUMP = "player_rifle_jump.png"

# Враги (по одному спрайту на каждого; внешне не меняются).
IMAGE_ENEMY_ZOMBIE = "zombie.png"
IMAGE_ENEMY_SPIDER = "spider.png"
IMAGE_ENEMY_SKELETON = "skeleton.png"

# Земля: закреплённая в мире полоса внизу, которая уезжает вниз при подъёме.
GROUND_TOP_Y = SCREEN_HEIGHT - 80   # мировая координата Y верха земли в начале игры

# Лёгкий бесшовный дрейф неба (без тайлинга => без швов).
SKY_DRIFT = 24          # максимальный сдвиг по вертикали в пикселях
SKY_DRIFT_FREQ = 0.002  # как быстро небо «покачивается» при подъёме камеры

# --- Звук -----------------------------------------------------------------
MUSIC_BACKGROUND = "music.ogg"   # фоновая музыка, играет по кругу всё время
MUSIC_VOLUME = 0.4               # громкость фоновой музыки (0..1)

# --- Сохранение -----------------------------------------------------------
SAVE_FILE_PATH = "savegame.json"

# --- Цвета (RGB) ----------------------------------------------------------
COLOR_BACKGROUND = (235, 240, 250)
COLOR_TEXT = (40, 44, 52)
COLOR_TEXT_DIM = (120, 124, 132)
COLOR_PLAYER = (90, 160, 90)
COLOR_PLATFORM_STATIC = (110, 200, 110)
COLOR_PLATFORM_MOVING = (90, 150, 220)
COLOR_PLATFORM_BREAKABLE = (200, 150, 90)
COLOR_PLATFORM_SPRING = (220, 110, 160)
COLOR_OVERLAY = (0, 0, 0, 140)

# Текст меню: оттенки белого с тёмной тенью, чтобы не сливался с картинкой.
COLOR_MENU_TITLE = (255, 255, 255)
COLOR_MENU_TEXT = (236, 240, 248)
COLOR_MENU_DIM = (205, 211, 223)
COLOR_MENU_SHADOW = (12, 16, 24)
