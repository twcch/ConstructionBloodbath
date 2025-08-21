import pygame
from pygame.math import Vector2 as vector

from model.entity.combatant.base import Combatant


class Enemy(Combatant):
    def __init__(self, position, path, groups, shoot, player, collision_sprites):
        super().__init__(position, path, groups, shoot)
        self.player = player  # 玩家物件
        for sprite in collision_sprites.sprites():
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = self.rect.top + 80  # 確保敵人不會穿過地面
        self.cooldown = 1000

        self.health = 2

    def get_status(self):
        # 檢查玩家位置來決定敵人狀態
        if self.player.rect.centerx < self.rect.centerx:
            self.status = 'left'
        else:
            self.status = 'right'

    def check_fire(self):
        enemy_position = vector(self.rect.center)
        player_position = vector(self.player.rect.center)

        distance = (player_position - enemy_position).magnitude()
        same_y = True if self.rect.top - 20 < player_position.y < self.rect.bottom + 20 else False

        if distance < 600 and same_y and self.can_shoot:
            bullet_direction = vector(1, 0) if self.status == 'right' else vector(-1, 0)
            y_offset = vector(0, -16)
            position = self.rect.center + bullet_direction * 80
            self.shoot(position + y_offset, bullet_direction, self)

            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()  # 記錄射擊時間

    def update(self, dt):
        self.get_status()
        self.animate(dt)  # 更新動畫
        self.blink()
        self.invul_timer()
        self.shoot_timer()  # 檢查射擊冷卻時間
        self.check_fire()  # 檢查是否可以射擊

        self.check_death()
