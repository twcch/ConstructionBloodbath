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

        self.setup()

        # overlay
        self.overlay = Overlay(self.player)

        # bullet images
        self.bullet_surf = self.assets.image('assets/graphics/bullet.png')
        self.fire_surfs = [self.assets.image(f'assets/graphics/fire/{i}.png') for i in range(1, 2)]

        # music
        self.music = self.assets.sound('assets/audio/music.wav')
        self.music.play(loops=-1)
        self.music.set_volume(MUSIC_VOLUME)  # 使用設定常數

    def setup(self):
        factory = TMXEntityFactory(
            assets=self.assets,
            all_sprites=self.all_sprites,
            collision_sprites=self.collision_sprites,
            platform_sprites=self.platform_sprites,
            vulnerable_sprites=self.vulnerable_sprites,
            shoot_cb=self.shoot
        )
        self.player, self.platform_border_rects = factory.build_world('assets/data/map.tmx')

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

    def shoot(self, position: vector, direction: vector, entity: pygame.sprite.Sprite) -> None:
        Bullet(position=position, surface=self.bullet_surf, direction=direction,
               groups=[self.all_sprites, self.bullet_sprites])
        FireAnimation(entity=entity, surface_list=self.fire_surfs, direction=direction, groups=self.all_sprites)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self, dt: float) -> None:
        self.platform_collisions()
        self.all_sprites.update(dt)
        self.bullet_collisions()

    def draw(self) -> None:
        self.display_surface.fill(BG_COLOR)
        self.all_sprites.render(self.player)  # 原 customer_draw 改為 render
        self.overlay.display()
        pygame.display.update()

    def run(self) -> None:
        while True:
            if not self.handle_events():
                pygame.quit()
                sys.exit()
            dt = self.clock.tick(FPS) / 1000
            self.update(dt)
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
