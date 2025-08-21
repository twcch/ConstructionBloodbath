import pygame
from pygame.math import Vector2 as vector

from configs.settings import *


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
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.position += self.direction * self.speed * dt
        self.rect.center = (round(self.position.x), round(self.position.y))

        # 子彈射程
        if pygame.time.get_ticks() - self.start_time > 1000:  # 子彈存在時間限制
            self.kill()  # 超過時間後自動銷毀子彈


class FireAnimation(pygame.sprite.Sprite):
    def __init__(self, entity, surface_list, direction, groups):
        super().__init__(groups)

        # setup
        self.entity = entity
        self.frames = surface_list
        if direction.x < 0:
            self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]

        # image
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # offset
        x_offset = 60 if direction.x > 0 else -60
        y_offset = 10 if entity.duck else -16
        self.offset = vector(x_offset, y_offset)

        # position
        self.rect = self.image.get_rect(center=self.entity.rect.center + self.offset)
        self.z = LAYERS['Level']  # 火焰動畫在子彈上方

    def animate(self, dt):
        self.frame_index += 15 * dt  # 調整動畫速度

        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def move(self):
        self.rect.center = self.entity.rect.center + self.offset

    def update(self, dt):
        self.animate(dt)
        self.move()
