import pygame
from pygame.math import Vector2 as vector
import random

from model.entity.combatant.base import Combatant
from model.entity.item import HealItem
from configs.settings import HEAL_ITEM_IMG, HEAL_ITEM_BIG_IMG, HEAL_ITEM_SOUP_IMG, HEAL_ITEM_CLAM_SOUP_IMG
from model.service.event_bus import GLOBAL_EVENTS


class Enemy(Combatant):
    def __init__(self, position, path, groups, shoot, player, collision_sprites):
        super().__init__(position, path, groups, shoot)
        self.player = player  # 玩家物件
        self.collision_sprites = collision_sprites
        for sprite in collision_sprites.sprites():
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = self.rect.top + 80  # 確保敵人不會穿過地面
        self.cooldown = 1000

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

    def check_death(self):
        if self.health <= 0:
            # 記錄玩家擊殺
            if hasattr(self, 'player') and hasattr(self.player, 'kill_count'):
                self.player.kill_count += 1
                GLOBAL_EVENTS.emit('enemy_killed', player_id=id(self.player))
            # 50% 掉落 (四擇一: 小/大/特大/蛤蜊湯)
            if hasattr(self.player, 'item_sprites') and hasattr(self.player, 'all_sprites'):
                if random.random() < 0.5:  # 總掉落率 50%
                    roll = random.random()  # 內部分配: 小50% 大30% 特大10% 負面10%
                    if roll < 0.5:
                        heal_amount, path = 1, HEAL_ITEM_IMG
                    elif roll < 0.8:
                        heal_amount, path = 2, HEAL_ITEM_BIG_IMG
                    elif roll < 0.9:
                        heal_amount, path = 5, HEAL_ITEM_SOUP_IMG
                    else:
                        heal_amount, path = -5, HEAL_ITEM_CLAM_SOUP_IMG
                    HealItem(
                        self.rect.center,
                        self.player.all_sprites,
                        self.player.item_sprites,
                        collision_sprites=self.collision_sprites,
                        heal_amount=heal_amount,
                        image_path=path
                    )
            self.kill()

    def update(self, dt):
        self.get_status()
        self.animate(dt)  # 更新動畫
        self.blink()
        self.invul_timer()
        self.shoot_timer()  # 檢查射擊冷卻時間
        self.check_fire()  # 檢查是否可以射擊
        self.check_death()
