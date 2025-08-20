import pygame
from configs.settings import *
from pygame.math import Vector2 as vector

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

class MovingPlatform(CollisionTile):
    def __init__(self, position, surface, groups):
        super().__init__(position, surface, groups)
        
        # float based movement
        self.direction = vector(0, -1)  # 移動方向
        self.speed = 200  # 移動速度 (像素/秒)
        self.position = vector(self.rect.topleft)  # 位置 (浮點數)
        
        # github copilot ------
        # 添加移動邊界
        self.start_pos = vector(self.rect.topleft)
        self.max_distance = 800  # 平台上下移動的最大距離
        # github copilot ------
    
    def update(self, dt):
        self.old_rect = self.rect.copy()  # 儲存上幀的 rect
        self.position.y += self.direction.y * self.speed * dt  # 更新位置
        
        # github copilot ------
        # 檢查是否達到移動邊界，如果是則反向
        if abs(self.position.y - self.start_pos.y) > self.max_distance:
            self.direction.y *= -1  # 反向移動
        # github copilot ------
        
        
        self.rect.topleft = (round(self.position.x), round(self.position.y))  # 同步到 rect
