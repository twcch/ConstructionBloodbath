FPS = 60
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TITLE = 'Iron Vortex'
LAYERS = {
	'BG': 0,
	'BG Detail': 1,
	'Level': 2,
	'FG Detail Bottom': 3,
	'FG Detail Top': 4,
}

# Visual / audio constants
BG_COLOR = (249, 131, 103)
MUSIC_VOLUME = 0.5

# Optional: sprite layer mapping (若你用 sprite.z，可用這個統一)
Z_LAYERS = {
    'bg': 0,
    'terrain': 1,
    'entities': 2,
    'fx': 3,
    'ui': 4,
}