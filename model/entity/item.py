import pygame
from abc import ABC, abstractmethod
from configs.settings import HEAL_ITEM_IMG, LAYERS
from model.service.event_bus import GLOBAL_EVENTS


class ItemEffect(ABC):
    @abstractmethod
    def apply(self, target): ...


class HealEffect(ItemEffect):
    def __init__(self, amount: int, image_path: str | None = None):
        self.amount = amount
        self.image_path = image_path

    def apply(self, target):
        # special negative rule handled by caller previously; keep simple here
        old = getattr(target, 'health', 0)
        max_hp = getattr(target, 'max_health', old + self.amount)
        new_val = max(0, min(old + self.amount, max_hp))
        setattr(target, 'health', new_val)
        GLOBAL_EVENTS.emit('health_changed', current=new_val, max_hp=max_hp, entity_id=id(target))


class BaseItem(pygame.sprite.Sprite):
    def __init__(self, position, *groups, collision_sprites: pygame.sprite.Group | None = None):
        super().__init__(*groups)
        self._collision_sprites = collision_sprites
        self._vel_y = 0.0
        self._gravity = 1800
        self._max_fall = 1200
        self._landed = False
        self._pos_y = 0.0
        self.effect: ItemEffect | None = None

    def _physics_init(self):
        self._pos_y = float(self.rect.y)

    def _apply_gravity(self, dt: float):
        if self._landed:
            return
        self._vel_y = min(self._vel_y + self._gravity * dt, self._max_fall)
        self._pos_y += self._vel_y * dt
        self.rect.y = round(self._pos_y)
        if self._collision_sprites:
            for sprite in self._collision_sprites.sprites():
                if self.rect.colliderect(sprite.rect) and self._vel_y >= 0 and self.rect.bottom >= sprite.rect.top:
                    self.rect.bottom = sprite.rect.top
                    self._pos_y = self.rect.y
                    self._vel_y = 0
                    self._landed = True
                    break

    def pick(self, target):
        if self.effect:
            self.effect.apply(target)
        self.kill()

    def update(self, dt):
        self._apply_gravity(dt)


class HealItem(BaseItem):
    """Backward compatible heal item (positive or negative)."""
    def __init__(self, position, *groups, heal_amount: int = 1, collision_sprites: pygame.sprite.Group | None = None, image_path: str | None = None):
        super().__init__(position, *groups, collision_sprites=collision_sprites)
        path = image_path or HEAL_ITEM_IMG
        try:
            self.image = pygame.image.load(path).convert_alpha()
        except Exception:
            self.image = pygame.Surface((32, 48))
            self.image.fill((50, 200, 50))
        self.rect = self.image.get_rect(center=position)
        self.z = LAYERS['Level']
        self.heal_amount = heal_amount
        self.image_path = path
        self.effect = HealEffect(heal_amount, image_path=path)
        self._physics_init()

