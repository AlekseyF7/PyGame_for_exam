"""Project-wide constants (no magic numbers in the code)."""

# --- Window ---------------------------------------------------------------
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Jump or die"

# --- Physics (screen coordinates: y grows downward) -----------------------
GRAVITY = 2000.0          # px/s^2
JUMP_VELOCITY = -900.0    # px/s (negative = upward)
SPRING_JUMP_VELOCITY = -1500.0
MOVE_SPEED = 360.0        # px/s horizontal

# --- Player ---------------------------------------------------------------
PLAYER_WIDTH = 46
PLAYER_HEIGHT = 46
PLAYER_START_OFFSET_Y = 120  # distance from bottom at game start

# --- Platforms ------------------------------------------------------------
PLATFORM_WIDTH = 70
PLATFORM_HEIGHT = 20
PLATFORM_MIN_GAP_Y = 70           # min vertical distance between platforms
PLATFORM_MAX_GAP_RATIO = 0.85     # max gap as a fraction of reachable jump height
MOVING_PLATFORM_SPEED = 90.0      # px/s

# --- Collectibles & hazards ----------------------------------------------
COIN_SIZE = 28
COIN_SPAWN_CHANCE = 0.25          # chance a new platform carries a coin
ELYTRA_SIZE = 36
ELYTRA_SPAWN_CHANCE = 0.04        # rare
ELYTRA_FLIGHT_VELOCITY = -700.0   # upward velocity while flying (px/s)
ELYTRA_BOOST_HEIGHT = 700.0       # how far up the elytra carries the player (px)

PORTAL_SIZE = 64
PORTAL_SPAWN_CHANCE = 0.06        # chance to place a portal near an edge
PORTAL_EDGE_MARGIN = 4            # how far from the screen edge a portal sits

# --- Weapons & shooting ---------------------------------------------------
WEAPON_SIZE = 36

# Each weapon spawns once when the climbed height (= score) reaches its value.
WEAPON_HEIGHT_BOW = 1000
WEAPON_HEIGHT_PISTOL = 2000
WEAPON_HEIGHT_RIFLE = 5000

# Fire cooldown per weapon (seconds between shots).
BOW_COOLDOWN = 3.0
PISTOL_COOLDOWN = 1.0
RIFLE_COOLDOWN = 0.5

# Projectiles fly straight up.
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 24
PROJECTILE_SPEED = -900.0         # upward velocity (px/s)

# --- Enemies --------------------------------------------------------------
ENEMY_SIZE = 48
ENEMY_MIN_HEIGHT = 1000           # enemies start at the same height as weapons

# Hit points (number of player shots to kill), independent of weapon type.
ZOMBIE_HP = 2
SPIDER_HP = 1
SKELETON_HP = 3

# Movement speeds (px/s).
SPIDER_SPEED = 90.0               # horizontal patrol, like a moving platform
SKELETON_SPEED = 70.0            # vertical patrol

# Skeleton shooting.
SKELETON_SHOOT_COOLDOWN = 1.0     # seconds between arrows
SKELETON_ARROW_SPEED = 320.0      # horizontal arrow speed (px/s)

# Spawn chances per generated platform (zombie common, spider rarer, skeleton rare).
# Combined ~17% per platform, so enemies appear regularly but not on every step.
ZOMBIE_SPAWN_CHANCE = 0.10
SPIDER_SPAWN_CHANCE = 0.05
SKELETON_SPAWN_CHANCE = 0.02

# --- Camera / scoring -----------------------------------------------------
CAMERA_FOLLOW_RATIO = 0.4         # keep player at 40% from the top
SCORE_DIVISOR = 10.0              # world pixels per score point
SPAWN_AHEAD = 200                 # how far above the camera to keep spawning
CULL_MARGIN = 80                  # px below screen before a platform is removed

# --- Assets ---------------------------------------------------------------
ASSETS_DIR = "assets"
IMAGES_DIR = "images"
SOUNDS_DIR = "sounds"
FONTS_DIR = "fonts"
FONT_CANDIDATES = "arialunicodems,arial,dejavusans,freesans,liberationsans"
FONT_SIZE_TITLE = 64
FONT_SIZE_NORMAL = 32
FONT_SIZE_SMALL = 24

# Image file names (placed in assets/images/). Missing files fall back to
# simple placeholders, so art can be added gradually.
IMAGE_PLAYER = "player.png"            # standing / falling pose
IMAGE_PLAYER_JUMP = "player_jump.png"  # rising / jumping pose
IMAGE_BACKGROUND = "background.png"     # sky image (stretched full-screen)
IMAGE_GROUND = "ground.png"            # ground strip shown at the start
IMAGE_MENU_BACKGROUND = "menu_bg.png"  # main menu background

# Per-platform sprites (keyed by PlatformKind in the view).
IMAGE_PLATFORM_STATIC = "platform_static.png"
IMAGE_PLATFORM_MOVING = "platform_moving.png"
IMAGE_PLATFORM_BREAKABLE = "platform_breakable.png"
IMAGE_PLATFORM_SPRING = "platform_spring.png"

# Collectibles and hazards.
IMAGE_COIN = "coin.png"
IMAGE_ELYTRA = "elytra.png"
IMAGE_PORTAL = "portal.png"

# Weapon pickups (lying on platforms).
IMAGE_WEAPON_BOW = "weapon_bow.png"
IMAGE_WEAPON_PISTOL = "weapon_pistol.png"
IMAGE_WEAPON_RIFLE = "weapon_rifle.png"

# Projectiles / ammo.
IMAGE_PROJECTILE_BOW = "arrow.png"
IMAGE_PROJECTILE_PISTOL = "bullet.png"
IMAGE_PROJECTILE_RIFLE = "bullet.png"

# Player holding a weapon (idle + jump poses). Falls back to the base player
# sprite if a file is missing.
IMAGE_PLAYER_BOW = "player_bow.png"
IMAGE_PLAYER_BOW_JUMP = "player_bow_jump.png"
IMAGE_PLAYER_PISTOL = "player_pistol.png"
IMAGE_PLAYER_PISTOL_JUMP = "player_pistol_jump.png"
IMAGE_PLAYER_RIFLE = "player_rifle.png"
IMAGE_PLAYER_RIFLE_JUMP = "player_rifle_jump.png"

# Enemies (one sprite each; they do not change appearance).
IMAGE_ENEMY_ZOMBIE = "zombie.png"
IMAGE_ENEMY_SPIDER = "spider.png"
IMAGE_ENEMY_SKELETON = "skeleton.png"

# Ground: a world-fixed strip at the bottom that scrolls away as you climb.
GROUND_TOP_Y = SCREEN_HEIGHT - 80   # world Y of the ground top at game start

# Gentle seamless sky drift (no tiling => no seams).
SKY_DRIFT = 24          # max vertical drift in px
SKY_DRIFT_FREQ = 0.002  # how fast the sky bobs as the camera climbs

# --- Persistence ----------------------------------------------------------
SAVE_FILE_PATH = "savegame.json"

# --- Colors (RGB) ---------------------------------------------------------
COLOR_BACKGROUND = (235, 240, 250)
COLOR_TEXT = (40, 44, 52)
COLOR_TEXT_DIM = (120, 124, 132)
COLOR_PLAYER = (90, 160, 90)
COLOR_PLATFORM_STATIC = (110, 200, 110)
COLOR_PLATFORM_MOVING = (90, 150, 220)
COLOR_PLATFORM_BREAKABLE = (200, 150, 90)
COLOR_PLATFORM_SPRING = (220, 110, 160)
COLOR_OVERLAY = (0, 0, 0, 140)

# Menu text: shades of white with a dark shadow so it never blends with the art.
COLOR_MENU_TITLE = (255, 255, 255)
COLOR_MENU_TEXT = (236, 240, 248)
COLOR_MENU_DIM = (205, 211, 223)
COLOR_MENU_SHADOW = (12, 16, 24)
