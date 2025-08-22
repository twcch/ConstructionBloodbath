import pygame
from configs.settings import HEAL_ITEM_IMG, LAYERS


class HealItem(pygame.sprite.Sprite):
    """簡單的補血道具，玩家碰到即 +1 HP，下落至地面停止。"""

    def __init__(self, position, *groups, heal_amount: int = 1, collision_sprites: pygame.sprite.Group | None = None, image_path: str | None = None):
        super().__init__(*groups)
        path = image_path or HEAL_ITEM_IMG
        try:
            self.image = pygame.image.load(path).convert_alpha()
        except Exception:
            # 後備方塊
            self.image = pygame.Surface((32, 48))
            self.image.fill((50, 200, 50))
        self.rect = self.image.get_rect(center=position)
        self.z = LAYERS['Level']
        self.heal_amount = heal_amount
        self.image_path = path  # 用於辨識道具種類

        # 下落物理
        self._vel_y = 0.0
        self._gravity = 1800  # px/s^2
        self._max_fall = 1200
        self._landed = False
        self._pos_y = float(self.rect.y)
        self._collision_sprites = collision_sprites

    def _apply_gravity(self, dt: float):
        if self._landed:
            return
        self._vel_y = min(self._vel_y + self._gravity * dt, self._max_fall)
        self._pos_y += self._vel_y * dt
        self.rect.y = round(self._pos_y)

        # 簡單垂直碰撞: 找到腳下第一個碰撞磚
        if self._collision_sprites:
            for sprite in self._collision_sprites.sprites():
                if self.rect.colliderect(sprite.rect):
                    # 落地 (僅考慮從上往下)
                    if self._vel_y >= 0 and self.rect.bottom >= sprite.rect.top:
                        self.rect.bottom = sprite.rect.top
                        self._pos_y = self.rect.y
                        self._vel_y = 0
                        self._landed = True
                    break

    def update(self, dt):
        self._apply_gravity(dt)
        # 可再加入閃爍 / 呼吸動畫
