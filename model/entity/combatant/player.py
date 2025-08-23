import sys

import pygame
from pygame.math import Vector2 as vector

from model.entity.combatant.base import Combatant
from configs.settings import HEAL_ITEM_CLAM_SOUP_IMG


class Player(Combatant):
    def __init__(self, position, groups, path, collision_sprites, shoot):
        super().__init__(position, path, groups, shoot)  # Sprite 的建構子就會自動幫你把自己加入到這些 Group 裡

        # collision
        self.collision_sprites = collision_sprites  # 碰撞用的群組

        # vertical movement
        self.gravity = 15  # 重力加速度
        self.jump_speed = 600  # 跳躍速度
        self.on_floor = False  # 是否在地面上
        self.moving_floor = None  # 當前接觸的移動平台

        self.health = 10
        self.is_dead = False
        # 新增：擊殺計數
        self.kill_count = 0

    def get_status(self):
        # idle
        if self.direction.x == 0 and self.on_floor:
            self.status = self.status.split('_')[0] + '_idle'

        # jump
        if self.direction.y != 0 and not self.on_floor:
            self.status = self.status.split('_')[0] + '_jump'

        # duck
        if self.on_floor and self.duck:
            self.status = self.status.split('_')[0] + '_duck'

    def check_contact(self):
        bottom_rect = pygame.Rect(0, 0, self.rect.width, 5)
        bottom_rect.midtop = self.rect.midbottom

        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(bottom_rect):
                if self.direction.y > 0:
                    self.on_floor = True
                if hasattr(sprite, 'direction'):
                    self.moving_floor = sprite

    # get the player input (all arrow keys: left, right, up, down)
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_floor:
            self.direction.y = -self.jump_speed

        if keys[pygame.K_DOWN]:
            self.duck = True
        else:
            self.duck = False

        if keys[pygame.K_SPACE] and self.can_shoot:
            direction = vector(1, 0) if self.status.split('_')[0] == 'right' else vector(-1, 0)
            position = self.rect.center + direction * 80  # 射擊位置在玩家前方
            y_offset = vector(0, -16) if not self.duck else vector(0, 10)
            self.shoot(position + y_offset, direction, self)

            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()  # 記錄射擊時間
            self.shoot_sound.play()  # 播放射擊音效

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    # left collision
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.rect.right:
                        self.rect.left = sprite.rect.right
                    # right collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.rect.left:
                        self.rect.right = sprite.rect.left

                    self.position.x = self.rect.x
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.on_floor = True
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    self.position.y = self.rect.y
                    self.direction.y = 0

        if self.on_floor and self.direction.y != 0:
            self.on_floor = False

    # use the input to move the player
    def move(self, dt):
        # 修正蹲下移動
        if self.duck and self.on_floor:
            self.direction.x = 0

        # 浮點座標 vs 畫面座標分離
        # self.position: float (高精度、可累積細小位移，不受取整誤差影響)
        # self.rect: int (pygame blit 需要整數像素)
        # 每幀: 更新 position (float) → 再同步到 rect (int)

        # horizontal movement
        self.position.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.position.x)
        self.collision('horizontal')

        # vertical movement
        # gravity
        self.direction.y += self.gravity  # 重力影響
        self.position.y += self.direction.y * dt

        # glue the player to the platform
        if self.moving_floor and self.moving_floor.direction.y > 0 and self.direction.y > 0:
            self.position.y = 0
            self.rect.bottom = self.moving_floor.rect.top
            self.position.y = self.rect.y
            self.on_floor = True

        self.rect.y = round(self.position.y)
        self.collision('vertical')
        self.moving_floor = None  # 重置移動平台接觸狀態

    def add_kill(self):
        self.kill_count += 1

    def check_death(self):
        if self.health <= 0 and not self.is_dead:
            self.is_dead = True
            self.kill()  # 只移除自己，不結束遊戲

    def update(self, dt):
        self.old_rect = self.rect.copy()

        self.input()
        self.get_status()
        self.move(dt)
        self.check_contact()
        self.animate(dt)
        self.blink()  # 閃爍效果

        self.shoot_timer()
        self.invul_timer()

        # 撿取補血道具
        if hasattr(self, 'item_sprites'):
            hits = pygame.sprite.spritecollide(self, self.item_sprites, dokill=True)
            for item in hits:
                heal = getattr(item, 'heal_amount', 1)
                # 若為蛤蜊湯且當前 hp <5 則直接死亡
                if getattr(item, 'image_path', None) == HEAL_ITEM_CLAM_SOUP_IMG and self.health < 5:
                    self.health = 0
                else:
                    self.health = max(0, min(self.health + heal, 10))

        # github copilot ------
        # 保存上一幀的平台引用
        self.previous_moving_floor = self.moving_floor
        self.moving_floor = None

        # 其他更新邏輯...
        self.check_contact()  # 這裡會檢測移動平台並更新 self.moving_floor

        # 如果站在移動平台上
        if self.moving_floor:
            # 跟隨平台移動
            self.position.y += self.moving_floor.direction.y * self.moving_floor.speed * dt
            self.rect.y = round(self.position.y)
            self.on_floor = True
        # github copilot ------

        self.check_death()
