from model.entity.bullet import Bullet, FireAnimation
from pygame.math import Vector2 as vector
import pygame

class ShootingSystem:
    def __init__(self, level_manager, bullet_surf, fire_surfs):
        self.lm = level_manager
        self.bullet_surf = bullet_surf
        self.fire_surfs = fire_surfs

    def shoot(self, position: vector, direction: vector, entity: pygame.sprite.Sprite):
        Bullet(position=position, surface=self.bullet_surf, direction=direction,
               groups=[self.lm.all_sprites, self.lm.bullet_sprites])
        FireAnimation(entity=entity, surface_list=self.fire_surfs, direction=direction,
                      groups=self.lm.all_sprites)
