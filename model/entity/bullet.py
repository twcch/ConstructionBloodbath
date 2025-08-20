import pygame
from configs.settings import *
from pygame.math import Vector2 as vector

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, surface, direction, groups):
        super().__init__(groups)
        self.image = surface
        
        # 修正子彈方向
        if direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect = self.image.get_rect(center=position)
        self.z = LAYERS['Level']
        
        self.direction = direction
        self.speed = 600  # 像素/秒
        self.position = vector(self.rect.center)
        
        self.start_time = pygame.time.get_ticks()
        
    def update(self, dt):
        self.position += self.direction * self.speed * dt
        self.rect.center = (round(self.position.x), round(self.position.y))
        
        # 子彈射程
        if pygame.time.get_ticks() - self.start_time > 1000:  # 子彈存在時間限制
            self.kill()  # 超過時間後自動銷毀子彈