import pygame
from configs.settings import *
from model.service.event_bus import GLOBAL_EVENTS


class Overlay:
    def __init__(self, player):
        self.player = player
    # 統一字型: 使用 settings.FONT_DEFAULT (若載入失敗 fallback None)
        try:
            self.font = pygame.font.Font(FONT_DEFAULT, 32)
        except Exception:
            self.font = pygame.font.Font(None, 32)
        self.display_surface = pygame.display.get_surface()
        # 延後載入 health_surface：若 display 尚未初始化，使用暫時 surface
        try:
            self.health_surface = pygame.image.load(HEALTH_IMG).convert_alpha()
        except pygame.error:
            self.health_surface = pygame.Surface((32, 32))
            self.health_surface.fill((255, 0, 0))
        self._cached_health = getattr(player, 'health', 0) if player else 0
        self._cached_max = getattr(player, 'max_health', self._cached_health)
        if player:
            GLOBAL_EVENTS.subscribe('health_changed', self._on_health)

    def _on_health(self, current, max_hp, entity_id):
        if self.player and entity_id == id(self.player):
            self._cached_health = current
            self._cached_max = max_hp

    def display(self):
        if not self.player:
            return
        health_value = self._cached_health if self.player else 0
        for h in range(health_value):
            x = h * (self.health_surface.get_width() + 5)
            y = WINDOW_HEIGHT - 50
            self.display_surface.blit(self.health_surface, (x + 20, y))
