import pygame
from pygame.math import Vector2 as vector
from configs.settings import WINDOW_WIDTH, WINDOW_HEIGHT, SKY_FG, SKY_BG

class AllSprites(pygame.sprite.Group):
    """Camera group: handles world offset & parallax sky rendering."""
    def __init__(self, assets, tmx_map):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.half_w = WINDOW_WIDTH / 2
        self.half_h = WINDOW_HEIGHT / 2

        # Sky layers
        self.fg_sky = assets.image(SKY_FG)
        self.bg_sky = assets.image(SKY_BG)

        # Compute repeat count based on map width
        self.padding = self.half_w
        self.sky_width = self.bg_sky.get_width()
        map_width = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
        self.sky_num = int(map_width // self.sky_width)

    def _render_background(self):
        for x in range(self.sky_num):
            x_pos = -self.padding + (x * self.sky_width)
            self.display_surface.blit(self.bg_sky, (x_pos - self.offset.x / 2.5, 850 - self.offset.y / 2.5))
            self.display_surface.blit(self.fg_sky, (x_pos - self.offset.x / 2, 850 - self.offset.y / 2))

    def _render_sprites(self):
        for sprite in sorted(self.sprites(), key=lambda spr: getattr(spr, 'z', 0)):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

    def render(self, player):
        if not player:
            return
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h
        self._render_background()
        self._render_sprites()
