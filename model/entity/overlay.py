import pygame
from configs.settings import *

class Overlay:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 32)
        self.display_surface = pygame.display.get_surface()
        self.health_surface = pygame.image.load('assets/graphics/health.png').convert_alpha()

    def display(self):
        for h in range(self.player.health):
            x = h * (self.health_surface.get_width() + 5)
            y = WINDOW_HEIGHT - 50
            self.display_surface.blit(self.health_surface, (x + 20, y))
