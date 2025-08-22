from pathlib import Path

"""全域設定與資源路徑集中管理

將專案中散落的 'assets/...'
 路徑集中到此，方便後續重構 / 搬移 / 打包。
使用 Path 物件組合，最終仍以 str() 提供給 pygame 載入。
"""

# ---- 基本視窗設定 ----
FPS = 60
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TITLE = '工地血戰'

# ---- 專案根目錄與資源資料夾 ----
BASE_DIR = Path(__file__).resolve().parent.parent  # 專案根 (configs/ 的上層)
ASSETS_DIR = BASE_DIR / 'assets'
GFX_DIR = ASSETS_DIR / 'graphics'
AUDIO_DIR = ASSETS_DIR / 'audio'
DATA_DIR = ASSETS_DIR / 'data'
FONT_DIR = ASSETS_DIR / 'font'

# ---- 子資源資料夾 ----
PLAYER_DIR = GFX_DIR / 'player'
ENEMY_DIR = GFX_DIR / 'enemy'
FIRE_DIR = GFX_DIR / 'fire'
SKY_DIR = GFX_DIR / 'sky'

# ---- 單一檔案路徑常數 (str) ----
SKY_FG = str(SKY_DIR / 'fg_sky.png')
SKY_BG = str(SKY_DIR / 'bg_sky.png')
BULLET_IMG = str(GFX_DIR / 'bullet.png')
HEALTH_IMG = str(GFX_DIR / 'health.png')
MUSIC_FILE = str(AUDIO_DIR / 'music.wav')
MAIN_MAP = str(DATA_DIR / 'map.tmx')
HEAL_ITEM_IMG = str(GFX_DIR / 'objects' / '台灣啤酒.png')  # 補血道具圖片
HEAL_ITEM_BIG_IMG = str(GFX_DIR / 'objects' / '台灣啤酒大.png')  # 大補血道具圖片
HEAL_ITEM_SOUP_IMG = str(GFX_DIR / 'objects' / '阿堂鹹粥.png')  # 特大補血 (+5)
HEAL_ITEM_CLAM_SOUP_IMG = str(GFX_DIR / 'objects' / '蛤蜊湯.png')  # 負面道具 (-5 HP)

# ---- 關卡地圖 (如後續擴充直接修改此 dict) ----
LEVEL_MAPS = {
    1: MAIN_MAP,
    2: MAIN_MAP,  # TODO: 更換為第二關實際地圖檔
    3: MAIN_MAP,  # TODO: 更換為第三關實際地圖檔
}

# ---- 字型 ----
FONT_CUBIC = str(FONT_DIR / 'Cubic-11-main' / 'Cubic-11.ttf')
FONT_BOUTIQUE = str(FONT_DIR / '微軟正黑體-1.ttf')
"""字型統一設定: 所有遊戲 UI / 文字統一指向這個路徑。
若要更換只需修改 FONT_DEFAULT = 某字型常數。
可用的候選: FONT_CUBIC, FONT_BOUTIQUE 或自行新增放入 assets/font/ 下。
"""
FONT_DEFAULT = FONT_BOUTIQUE  # ← 修改這裡即可全域換字型

# ---- 其他可擴充的載入輔助 (保留給未來需要) ----
def asset_path(*parts: str) -> str:
    """動態組合 assets 內路徑: asset_path('graphics','player','0.png')"""
    return str(ASSETS_DIR.joinpath(*parts))

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
MENU_BG_IMAGE = SKY_FG  # 主選單背景可直接重用前景天空