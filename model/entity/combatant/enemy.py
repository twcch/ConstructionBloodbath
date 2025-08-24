import pygame
from pygame.math import Vector2 as vector
import random
from pathlib import Path

from model.entity.combatant.base import Combatant
from model.entity.item import HealItem
from configs.settings import HEAL_ITEM_IMG, HEAL_ITEM_BIG_IMG, HEAL_ITEM_SOUP_IMG, HEAL_ITEM_CLAM_SOUP_IMG, BASE_DIR
from model.service.event_bus import GLOBAL_EVENTS
from typing import Any


class Enemy(Combatant):
    def __init__(self, position, path, groups, shoot, player, collision_sprites, assets=None, kind: str = 'default'):
        super().__init__(position, path, groups, shoot)
        self.player = player  # 玩家物件
        self.collision_sprites = collision_sprites
        for sprite in collision_sprites.sprites():
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = self.rect.top + 80  # 確保敵人不會穿過地面
        # data-driven stats
        self.cooldown = 1000
        if assets:
            enemies_cfg_path = str(Path(BASE_DIR) / 'configs' / 'enemies.json')
            try:
                enemies_cfg: dict[str, Any] = assets.json(enemies_cfg_path)
                data = enemies_cfg.get(kind, enemies_cfg.get('default', {}))
                self.health = data.get('health', self.health)
                self.cooldown = data.get('cooldown_ms', self.cooldown)
                self._drop_table_name = data.get('drop_table', 'standard_items')
            except Exception:
                self._drop_table_name = 'standard_items'
        else:
            self._drop_table_name = 'standard_items'

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
            # Data-driven drop logic
            if hasattr(self.player, 'item_sprites') and hasattr(self.player, 'all_sprites'):
                try:
                    items_cfg_path = str(Path(BASE_DIR) / 'configs' / 'items.json')
                    drop_cfg = None
                    if hasattr(self.player, 'assets'):
                        assets = getattr(self.player, 'assets')
                        items_cfg = assets.json(items_cfg_path)
                        tables = items_cfg.get('tables', {})
                        global_cfg = items_cfg.get('global', {})
                        drop_chance = float(global_cfg.get('drop_chance', 0.5))
                        if random.random() < drop_chance:
                            table = tables.get(getattr(self, '_drop_table_name', 'standard_items'), [])
                            total = sum(entry.get('weight', 1) for entry in table) or 1
                            r = random.uniform(0, total)
                            upto = 0
                            selected = table[0] if table else None
                            for entry in table:
                                upto += entry.get('weight', 1)
                                if r <= upto:
                                    selected = entry
                                    break
                            if selected:
                                img_rel = selected.get('image')
                                heal_amount = int(selected.get('heal', 1))
                                # resolve path relative to graphics dir
                                if img_rel and not img_rel.startswith('assets/'):
                                    path = str(Path(BASE_DIR) / 'assets' / 'graphics' / img_rel)
                                else:
                                    path = img_rel
                                HealItem(
                                    self.rect.center,
                                    self.player.all_sprites,
                                    self.player.item_sprites,
                                    collision_sprites=self.collision_sprites,
                                    heal_amount=heal_amount,
                                    image_path=path
                                )
                except Exception:
                    # fallback silence
                    pass
            self.kill()

    def update(self, dt):
        self.get_status()
        self.animate(dt)  # 更新動畫
        self.blink()
        self.invul_timer()
        self.shoot_timer()  # 檢查射擊冷卻時間
        self.check_fire()  # 檢查是否可以射擊
        self.check_death()
