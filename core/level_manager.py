import os
import pygame
from configs.settings import LEVEL_MAPS, MAIN_MAP
from model.service.camera import AllSprites
from model.entity.overlay import Overlay
from model.factory.tmx_entities import TMXEntityFactory

class LevelManager:
    def __init__(self, assets, level_thresholds: dict[int, int]):
        self.assets = assets
        self.level_maps = LEVEL_MAPS
        self.level_thresholds = level_thresholds
        self.current_level = 1
        self.player = None
        self.platform_border_rects = []
        self.overlay = None

        self.all_sprites: AllSprites | None = None
        self.collision_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.vulnerable_sprites = pygame.sprite.Group()
        self.factory: TMXEntityFactory | None = None
        self._shoot_cb = None  # persist shooting callback across rebuilds

    def build_level(self, level: int, shoot_cb=None):
        """(Re)build level; optionally inject shoot callback."""
        self.current_level = level
        if shoot_cb:
            self._shoot_cb = shoot_cb
        map_path = self.level_maps.get(level, MAIN_MAP)
        if not os.path.exists(map_path):
            map_path = MAIN_MAP
        tmx_map = self.assets.tmx(map_path)
        self.all_sprites = AllSprites(self.assets, tmx_map)
        self.collision_sprites.empty()
        self.platform_sprites.empty()
        self.bullet_sprites.empty()
        self.vulnerable_sprites.empty()

        self.factory = TMXEntityFactory(
            assets=self.assets,
            all_sprites=self.all_sprites,
            collision_sprites=self.collision_sprites,
            platform_sprites=self.platform_sprites,
            vulnerable_sprites=self.vulnerable_sprites,
            shoot_cb=self._shoot_cb
        )
        self.player, self.platform_border_rects = self.factory.build_world(map_path)
        self.overlay = Overlay(self.player)

    def inject_shoot(self, shoot_cb):
        if self.factory:
            self.factory.shoot_cb = shoot_cb
        self._shoot_cb = shoot_cb

    def needs_advance(self) -> bool:
        if not self.player:
            return False
        need = self.level_thresholds.get(self.current_level)
        return need is not None and self.player.kill_count >= need

    def next_level_exists(self) -> bool:
        return (self.current_level + 1) in self.level_maps
