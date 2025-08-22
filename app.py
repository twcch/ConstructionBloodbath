import os
import sys

import pygame
from pygame.math import Vector2 as vector

from configs.settings import *
from model.entity.bullet import Bullet, FireAnimation
from model.entity.overlay import Overlay
from model.factory.tmx_entities import TMXEntityFactory
from model.service.assets import AssetManager


# Camera, 控制玩家視角
class AllSprites(pygame.sprite.Group):
    def __init__(self, assets, tmx_map):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.half_w = WINDOW_WIDTH / 2
        self.half_h = WINDOW_HEIGHT / 2

        # sky via AssetManager
        self.fg_sky = assets.image('assets/graphics/sky/fg_sky.png')
        self.bg_sky = assets.image('assets/graphics/sky/bg_sky.png')

        # dimensions
        self.padding = self.half_w
        self.sky_width = self.bg_sky.get_width()
        map_width = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
        self.sky_num = int(map_width // self.sky_width)

    def _render_background(self):
        for x in range(self.sky_num):
            x_position = -self.padding + (x * self.sky_width)
            # 可將 2.5 與 850 移到 settings 做成常數
            self.display_surface.blit(self.bg_sky, (x_position - self.offset.x / 2.5, 850 - self.offset.y / 2.5))
            self.display_surface.blit(self.fg_sky, (x_position - self.offset.x / 2, 850 - self.offset.y / 2))

    def _render_sprites(self):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

    def render(self, player) -> None:
        # 計算相機偏移量
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h
        self._render_background()
        self._render_sprites()


class Game:  # game
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        # 狀態（新增）
        self.state = 'menu'
        self.player = None
        self.platform_border_rects = []
        self.overlay = None
        
        # 關卡與門檻設定
        self.level = 1
        self.level_maps = {
            1: 'assets/data/map.tmx',
            2: 'assets/data/map.tmx',   # 請自行新增對應 TMX 檔
            3: 'assets/data/map.tmx'
        }
        # 從該關欲前進到下一關所需的總累積殺敵數
        self.level_thresholds = {
            1: 17,   # 累積 16 殺 → 進入第 2 關
            2: 34,    # 累積 32 殺 → 進入第 3 關
            3: 51   # 第 3 關達到門檻後進入致謝畫面（數值可調整）
        }
        
        # managers
        self.assets = AssetManager()
        # 先載入 TMX 供 AllSprites 計算 sky_num
        self._map_path = 'assets/data/map.tmx'
        tmx_map = self.assets.tmx(self._map_path)
        # Groups
        self.all_sprites = AllSprites(self.assets, tmx_map)
        self.collision_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.vulnerable_sprites = pygame.sprite.Group()

        # overlay
        self.overlay = Overlay(self.player)

        # bullet images
        self.bullet_surf = self.assets.image('assets/graphics/bullet.png')
        self.fire_surfs = [self.assets.image(f'assets/graphics/fire/{i}.png') for i in range(1, 2)]

        # music
        self.music = self.assets.sound('assets/audio/music.wav')
        self.music.play(loops=-1)
        self.music.set_volume(MUSIC_VOLUME)  # 使用設定常數

        # --- 字型設定（改用 Font 而非 SysFont）---
        base_dir = os.path.dirname(os.path.abspath(__file__))
        fonts_dir = os.path.join(base_dir, 'assets', 'fonts')
        cubic_font_path = os.path.join(base_dir, 'assets', 'font', 'Cubic-11-main', 'Cubic-11.ttf')

        def load_font(path, size):
            if not os.path.exists(path):
                print(f'[Font] Not found: {path} -> fallback default')
                return pygame.font.Font(None, size)
            try:
                return pygame.font.Font(path, size)
            except Exception as e:
                print(f'[Font] Fail load {path}: {e}')
                return pygame.font.Font(None, size)

        self.title_font = load_font(cubic_font_path, 72)
        self.text_font = load_font(cubic_font_path, 32)
        self.level_font = load_font(cubic_font_path, 96)
        self.credits_font_title = load_font(cubic_font_path, 72)
        self.credits_font_line = load_font(cubic_font_path, 32)

        try:
            _test = self.title_font.render('測試中文 Test', True, (255,255,255))
            print(f'[Font] Chinese render size: {_test.get_size()}')
        except Exception as e:
            print(f'[Font] Render fail: {e}')

        # Menu 背景
        self._menu_ready = False
        try:
            raw = self.assets.image(MENU_BG_IMAGE)
            self.menu_bg = pygame.transform.scale(raw, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception:
            self.menu_bg = None

        # UI 用（可直接用同一中文字型，避免 None）
        self.ui_font = self.text_font

        # --- 新增：關卡提示文字相關 (若想保留像素英文字型可另外命名，否則省略) ---
        # 原本 BoutiqueBitmap 不含中文，若仍要它，確保只用於英數。
        # self.pixel_font = load_font(os.path.join(fonts_dir,'BoutiqueBitmap9x9_Bold_1.9.ttf'), 32)

        self.level_announce_duration = 2.0
        self.level_announce_timer = 0.0
        # self.level_font = self.pixel_font  # 若需像素英字才打開

        # --- Credits （致謝畫面）---
        FONT_PATH = cubic_font_path  # 可改成其他字型路徑

        # self.credits_font_title = pygame.font.SysFont(FONT_PATH, 72, bold=True)
        # self.credits_font_line = pygame.font.SysFont(FONT_PATH, 32)
        self.credits_lines = [
            "THANK YOU FOR PLAYING",
            "感謝遊玩本遊戲！",
            "程式 / 美術 / 音效: 你自己",
            "特別感謝: 家人朋友支持",
            "Press ANY KEY to return to Menu"
        ]

    def draw_kill_count(self, surface):
        if not self.player:
            return
        text_surf = self.ui_font.render(f'Level: {self.level}  Kills: {self.player.kill_count}', True, (255, 255, 255))
        bg = pygame.Surface((text_surf.get_width() + 12, text_surf.get_height() + 8), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 120))
        surface.blit(bg, (8, 8))
        surface.blit(text_surf, (14, 12))

    def setup(self):
        # 只建立當前關卡（第 1 關 start_game 時呼叫）
        factory = TMXEntityFactory(
            assets=self.assets,
            all_sprites=self.all_sprites,
            collision_sprites=self.collision_sprites,
            platform_sprites=self.platform_sprites,
            vulnerable_sprites=self.vulnerable_sprites,
            shoot_cb=self.shoot
        )
        self.player, self.platform_border_rects = factory.build_world(self._map_path)
        self.overlay = Overlay(self.player)

    def start_game(self):
        if self.state != 'game':
            self.level = 1
            self._map_path = self.level_maps[self.level]

            # 重新建立群組與攝影機（確保乾淨重開）
            tmx_map = self.assets.tmx(self._map_path)
            self.all_sprites = AllSprites(self.assets, tmx_map)
            self.collision_sprites = pygame.sprite.Group()
            self.platform_sprites = pygame.sprite.Group()
            self.bullet_sprites = pygame.sprite.Group()
            self.vulnerable_sprites = pygame.sprite.Group()
            
        if self.state != 'game':
            self.level = 1
            self._map_path = self.level_maps[self.level]
            self.setup()
            self.state = 'game'
            # 新增：啟動關卡顯示
            self.level_announce_timer = self.level_announce_duration

    def platform_collisions(self):
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rects:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0:  # up
                        platform.rect.top = border.bottom
                        platform.position.y = platform.rect.y
                        platform.direction.y = 1
                    else:  # down
                        platform.rect.bottom = border.top
                        platform.position.y = platform.rect.y
                        platform.direction.y = -1
            if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.player.rect.top
                platform.position.y = platform.rect.y
                platform.direction.y = -1

    def bullet_collisions(self) -> None:
        # 子彈 vs 靜態障礙（矩形碰撞即可）
        pygame.sprite.groupcollide(self.bullet_sprites, self.collision_sprites, True, False)

        # 子彈 vs 可受傷實體（使用遮罩）
        hits = pygame.sprite.groupcollide(
            self.bullet_sprites, self.vulnerable_sprites, True, False, collided=pygame.sprite.collide_mask
        )
        for _, targets in hits.items():
            for target in targets:
                target.damage()

    def check_level_progression(self):
        """檢查是否達成進入下一關的條件"""
        if not self.player:
            return
        if self.level in self.level_thresholds:
            need = self.level_thresholds[self.level]
            if self.player.kill_count >= need:
                next_level = self.level + 1
                if next_level in self.level_maps:
                    self.advance_level(next_level)
                else:
                    self.enter_credits()
    
    def advance_level(self, next_level: int):
        """進入下一關並重置場景 (保留累積殺敵數)"""
        preserved_kills = self.player.kill_count if self.player else 0

        # 讀取對應地圖，若不存在則 fallback 到第一關
        map_path = self.level_maps.get(next_level, self.level_maps[1])
        try:
            tmx_map = self.assets.tmx(map_path)
        except Exception:
            tmx_map = self.assets.tmx(self.level_maps[1])
            next_level = 1

        # 重新建立主要群組（AllSprites 需依新地圖計算 sky_num）
        self.all_sprites = AllSprites(self.assets, tmx_map)
        self.collision_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.vulnerable_sprites = pygame.sprite.Group()

        # 建立世界
        factory = TMXEntityFactory(
            assets=self.assets,
            all_sprites=self.all_sprites,
            collision_sprites=self.collision_sprites,
            platform_sprites=self.platform_sprites,
            vulnerable_sprites=self.vulnerable_sprites,
            shoot_cb=self.shoot
        )
        self.player, self.platform_border_rects = factory.build_world(map_path)
        self.player.kill_count = preserved_kills  # 保留累積擊殺
        self.overlay = Overlay(self.player)
        self.level = next_level
        
        # 新增：切關時啟動顯示
        self.level_announce_timer = self.level_announce_duration
    
    def shoot(self, position: vector, direction: vector, entity: pygame.sprite.Sprite) -> None:
        Bullet(position=position, surface=self.bullet_surf, direction=direction,
               groups=[self.all_sprites, self.bullet_sprites])
        FireAnimation(entity=entity, surface_list=self.fire_surfs, direction=direction, groups=self.all_sprites)

    def enter_credits(self):
        self.state = 'credits'

    def return_to_menu(self):
        self.state = 'menu'
        # 如需重新開始時歸零擊殺可在 start_game 時重設
    
    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.state == 'menu':
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.start_game()
                    if event.key == pygame.K_ESCAPE:
                        return False
            elif self.state == 'credits':
                if event.type == pygame.KEYDOWN:
                    self.return_to_menu()
            else:
                # 遊戲內事件
                pass
        return True

    def update(self, dt: float) -> None:
        if self.state == 'menu':
            return
        if self.state == 'credits':
            return  # 致謝畫面不更新遊戲世界
        # ...existing code...
        if self.level_announce_timer > 0:
            self.level_announce_timer -= dt
            
        self.platform_collisions()
        self.all_sprites.update(dt)
        self.bullet_collisions()
        self.check_level_progression()
        
        # 玩家死亡 → 回主選單
        if self.player and (self.player.health <= 0 or not self.player.alive()):
            self.return_to_menu()
            self.player = None  # 清除引用，避免舊物件殘留
        
        # 新增：遞減關卡顯示計時
        if self.level_announce_timer > 0:
            self.level_announce_timer -= dt

    def draw_menu(self):
        if self.menu_bg:
            self.display_surface.blit(self.menu_bg, (0, 0))
        else:
            self.display_surface.fill(MENU_BG_COLOR)
        title_surf = self.title_font.render(TITLE, True, MENU_TITLE_COLOR)
        tip_surf = self.text_font.render('Press ENTER / SPACE to Start  |  ESC to Quit', True, MENU_TEXT_COLOR)
        rect_title = title_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 60))
        rect_tip = tip_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 40))
        self.display_surface.blit(title_surf, rect_title)
        self.display_surface.blit(tip_surf, rect_tip)

    def draw(self) -> None:
        if self.state == 'menu':
            self.draw_menu()
            pygame.display.update()
            return

        if self.state == 'credits':
            self.display_surface.fill((0, 0, 0))
            # 標題
            title_surf = self.credits_font_title.render(self.credits_lines[0], True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT*0.25))
            self.display_surface.blit(title_surf, title_rect)
            # 其餘行
            start_y = title_rect.bottom + 40
            for i, line in enumerate(self.credits_lines[1:]):
                surf = self.credits_font_line.render(line, True, (220, 220, 220))
                rect = surf.get_rect(center=(WINDOW_WIDTH/2, start_y + i * 50))
                self.display_surface.blit(surf, rect)
            pygame.display.update()
            return

        # 遊戲畫面
        self.display_surface.fill(BG_COLOR)
        self.all_sprites.render(self.player)
        self.overlay.display()
        if self.level_announce_timer > 0:
            ratio = max(0, self.level_announce_timer / self.level_announce_duration)
            alpha = int(255 * ratio)
            text_surf = self.level_font.render(f'Level {self.level}', True, (255, 255, 255))
            padding = 40
            box = pygame.Surface((text_surf.get_width() + padding, text_surf.get_height() + padding), pygame.SRCALPHA)
            box.fill((0, 0, 0, int(160 * ratio)))
            box_rect = box.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            text_rect = text_surf.get_rect(center=box_rect.center)
            temp_text = text_surf.copy()
            temp_text.set_alpha(alpha)
            self.display_surface.blit(box, box_rect)
            self.display_surface.blit(temp_text, text_rect)
        self.draw_kill_count(self.display_surface)
        pygame.display.update()
        
        pygame.display.update()

    def run(self) -> None:
        while True:
            if not self.handle_events():
                pygame.quit()
                sys.exit()
            dt = self.clock.tick(FPS) / 1000
            self.update(dt)
            self.draw()
            
            self.draw_kill_count(self.display_surface)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
