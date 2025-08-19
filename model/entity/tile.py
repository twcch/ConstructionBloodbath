import pygame
from configs.settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups, z):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.z = z  # 設定 z 層級，確保 Tile 在正確的層次上繪製


class CollisionTile(Tile):
    def __init__(self, position, surface, groups):
        super().__init__(position, surface, groups, LAYERS['Level'])
        self.old_rect = self.rect.copy() # 用來儲存上幀的 rect，避免碰撞檢測時