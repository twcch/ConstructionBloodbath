FPS = 60
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TITLE = 'Construction Bloodbath'

LAYERS = {
    'BG': 0,
    'BG Detail': 1,
    'Level': 2,
    'FG Detail Bottom': 3,
    'FG Detail Top': 4,
}

# Optional: sprite layer mapping (若你用 sprite.z，可用這個統一)
Z_LAYERS = {
    'bg': 0,
    'terrain': 1,
    'entities': 2,
    'fx': 3,
    'ui': 4,
}

# Visual / audio constants
#BG_COLOR = (35, 20, 50)
BG_COLOR = (0, 0, 0)  # Black background
MUSIC_VOLUME = 0.5

# --- Menu colors ---
MENU_BG_COLOR = (10, 10, 10)
MENU_TITLE_COLOR = (255, 255, 255)
MENU_TEXT_COLOR = (200, 200, 200)
MENU_BG_IMAGE = 'assets/graphics/sky/fg_sky.png'