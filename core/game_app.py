import pygame, sys
from configs.settings import WINDOW_WIDTH, WINDOW_HEIGHT, TITLE, MUSIC_FILE, MUSIC_VOLUME, BULLET_IMG, asset_path
from model.service.assets import AssetManager
from core.scene_manager import SceneManager
from core.level_manager import LevelManager
from core.fonts import FontManager, GameFonts
from core.audio import AudioManager
from ui.hud import HUD
from core.scenes.menu import MenuScene
from core.scenes.level import LevelScene
from core.scenes.credits import CreditsScene


class GameApp:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt_last = 0.0

        # assets
        self.assets = AssetManager()
        self.audio = AudioManager(self.assets, MUSIC_FILE, MUSIC_VOLUME)
        self.audio.play_music_loop()

        # fonts
        self.fonts = GameFonts(FontManager())

        # surfaces
        self.bullet_surf = self.assets.image(BULLET_IMG)
        self.fire_surfs = [self.assets.image(asset_path('graphics', 'fire', f'{i}.png')) for i in range(0, 2)]

        # level + HUD
        level_thresholds = {1: 2, 2: 34, 3: 51}
        self.level_manager = LevelManager(self.assets, level_thresholds)
        self.hud = HUD(self.fonts)

        # scenes
        self.scene_manager = SceneManager()
        self.scene_manager.register('menu', MenuScene(self))
        self.scene_manager.register('level', LevelScene(self))
        self.scene_manager.register('credits', CreditsScene(self))
        self.scene_manager.change('menu')

    def change_scene(self, name: str):
        self.scene_manager.change(name)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if self.scene_manager.current and hasattr(self.scene_manager.current, 'handle_event'):
                self.scene_manager.current.handle_event(event)

    def update(self, dt: float):
        if self.scene_manager.current:
            self.scene_manager.current.update(dt)

    def draw(self):
        if self.scene_manager.current:
            self.scene_manager.current.draw(self.display)
        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.dt_last = self.clock.tick(60) / 1000
            self.update(self.dt_last)
            self.draw()
        pygame.quit()
        sys.exit()
