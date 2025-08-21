import sys

import pygame
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame

from model.entity.player import Player
from configs.settings import *
from model.entity.tile import Tile, CollisionTile, MovingPlatform
from model.entity.bullet import Bullet, FireAnimation
from model.entity.enemy import Enemy
from model.entity.overlay import Overlay

# Camera, 控制玩家視角
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        # 抓取目前遊戲主畫布 (pygame.display.set_mode() 建立的 surface)
        self.display_surface = pygame.display.get_surface()
        # 偏移量，用來決定地圖相對於玩家的捲動位置
        self.offset = vector()
        
        # sky
        self.fg_sky = pygame.image.load('assets/graphics/sky/fg_sky.png').convert_alpha()
        self.bg_sky = pygame.image.load('assets/graphics/sky/bg_sky.png').convert_alpha()
        tmx_map = load_pygame('assets/data/map.tmx')
        
        ## dimensions
        self.padding = WINDOW_WIDTH / 2
        self.sky_width = self.bg_sky.get_width()
        map_width = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
        self.sky_num = int(map_width // self.sky_width)  # 計算需要多少張天空圖片來覆蓋整個地圖

    def customer_draw(self, player):
        # 計算相機偏移量
        # 玩家座標 (player.rect.centerx, player.rect.centery) 減掉螢幕中心點 → 得到「相機需要偏移多少」才能讓玩家保持在螢幕中心
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2
        
        for x in range(self.sky_num):
            x_position = -self.padding + (x * self.sky_width)
            self.display_surface.blit(self.bg_sky, (x_position - self.offset.x / 2.5, 850 - self.offset.y / 2.5))  # 背景天空
            self.display_surface.blit(self.fg_sky, (x_position - self.offset.x / 2, 850 - self.offset.y / 2))

        # 繪製所有 sprites
        # 遍歷群組裡的所有物件
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)  # 先用 sprite 的座標取得原始位置
            offset_rect.center -= self.offset  # 再扣掉相機偏移量，得到「在螢幕上的最終位置」
            self.display_surface.blit(sprite.image, offset_rect)  # 把 sprite 畫到畫布上


class Game:  # game
    def __init__(self):
        pygame.init()  # 遊戲初始化

        self.display_surface = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()

        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()  # 碰撞用的群組
        self.platform_sprites = pygame.sprite.Group()  # 用來儲存移動平台的群組
        self.bullet_sprites = pygame.sprite.Group()  # 用來儲存子彈的群組
        self.vulnerable_sprites = pygame.sprite.Group()  # 用來儲存無敵狀態的敵人

        self.setup()

        # overlay
        self.overlay = Overlay(self.player)

        # bullet images
        self.bullet_surf = pygame.image.load('assets/graphics/bullet.png').convert_alpha()
        self.fire_surfs = [pygame.image.load(f'assets/graphics/fire/{i}.png').convert_alpha() for i in range(1, 2)]

    def setup(self):
        tmx_map = load_pygame('assets/data/map.tmx')
        
        # collision tiles
        for x, y, surface in tmx_map.get_layer_by_name('Level').tiles():
            # 我們要顯示地圖的其中一個區塊，不能夠直接傳 (x, y)，必須要放大顯示局部
            # 有別於一般的寫法透過 all_sprites.add(object) 把物件加入群組，這是直接把群組傳入這個物件，由 Sprites() 將這個物件加入群組
            CollisionTile(position=(x * 64, y * 64), surface=surface, groups=[self.all_sprites, self.collision_sprites])

        # tiles
        # 4 mores layers we need to import: BG, BG Detail, FG Detail Bottom, FG Detail Top
        for layer in ['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']:
            # 這些層的 tiles() 方法會返回每個 tile 的位置和表面
            # 這裡假設每個 tile 的大小是 64x64 像素
            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():
                # 背景層
                Tile(position=(x * 64, y * 64), surface=surface, groups=self.all_sprites, z=LAYERS[layer])
        
        # objects
        # 從地圖檔 (TMX) 動態生成遊戲物件 (Entities)
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                # Player 初始位置是 TMX 中的 obj.x, obj.y (裡的 object layer 裡每個物件會有座標)
                # 生成 Player 物件，並加入到 all_sprites 群組，obj.x, obj.y 是 tile 的左上角座標
                self.player = Player(
                    position=(obj.x, obj.y), 
                    groups=[self.all_sprites, self.vulnerable_sprites], 
                    path='assets/graphics/player', 
                    collision_sprites=self.collision_sprites, 
                    shoot=self.shoot
                    )
            elif obj.name == 'Enemy':
                Enemy(
                    position=(obj.x, obj.y), 
                    path='assets/graphics/enemy', 
                    groups=[self.all_sprites, self.vulnerable_sprites], 
                    shoot=self.shoot, 
                    player=self.player, 
                    collision_sprites=self.collision_sprites
                    )

        self.platform_border_rects = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == 'Platform':
                MovingPlatform(position=(obj.x, obj.y), surface=obj.image, groups=[self.all_sprites, self.collision_sprites, self.platform_sprites])
            else:
                border_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.platform_border_rects.append(border_rect)

    def platform_collisions(self):
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rects:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0: # up
                        platform.rect.top = border.bottom
                        platform.position.y = platform.rect.y
                        platform.direction.y = 1
                    else: # down
                        platform.rect.bottom = border.top
                        platform.position.y = platform.rect.y
                        platform.direction.y = -1
            if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.player.rect.top
                platform.position.y = platform.rect.y
                platform.direction.y = -1

    def bullet_collisions(self):
        for obstacle in self.collision_sprites.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullet_sprites, True)  # 刪除與障礙物碰撞的子彈
        
        # entities
        for sprite in self.vulnerable_sprites.sprites():
            if pygame.sprite.spritecollide(sprite, self.bullet_sprites, True, pygame.sprite.collide_mask):  # 刪除與敵人碰撞的子彈
                sprite.damage()
                
    def shoot(self, position, direction, entity):
        Bullet(position=position, surface=self.bullet_surf, direction=direction, groups=[self.all_sprites, self.bullet_sprites])
        
        FireAnimation(entity=entity, surface_list=self.fire_surfs, direction=direction, groups=self.all_sprites)
        
    def run(self):
        while True:
            # 關閉遊戲
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # 取得單位 (s): 以「時間」而非「幀」來移動 (delta time)
            # 位移用：位移量 = 速度(像素/秒) × dt(秒)
            # --- 說明:
            # --- 設計理念就是把「移動邏輯」與「幀率 (FPS)」脫鉤，讓角色速度以「真實時間」為準，而不是以「每幀」為準
            # --- 例如 speed=400、dt=0.016 (約 60 FPS)，單幀位移 ≈ 6.4 px。
            # --- 即使 FPS 波動，1 秒跑的距離保持不變。
            dt = self.clock.tick(FPS) / 1000

            # 視窗背景
            self.display_surface.fill((249, 131, 103))

            # 畫面更新
            self.platform_collisions()
            self.all_sprites.update(dt)
            # self.all_sprites.draw(self.display_surface) # 把 all_sprites 群組裡的每一個 Sprite 的 image 畫到 self.display_surface 上，位置依照 Sprite 的 rect
            self.all_sprites.customer_draw(self.player)
            self.bullet_collisions()
            self.overlay.display()
            
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
