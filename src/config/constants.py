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
