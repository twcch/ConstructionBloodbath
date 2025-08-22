import pygame
from configs.settings import *


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

    def display(self):
        if not self.player:
            return
        for h in range(self.player.health):
            x = h * (self.health_surface.get_width() + 5)
            y = WINDOW_HEIGHT - 50
            self.display_surface.blit(self.health_surface, (x + 20, y))
