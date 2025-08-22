import pygame
from configs.settings import WINDOW_WIDTH, WINDOW_HEIGHT

class HUD:
    def __init__(self, fonts):
        self.fonts = fonts
        self.level_announce_duration = 2.0
        self.level_announce_timer = 0.0

    def start_level_announce(self):
        self.level_announce_timer = self.level_announce_duration

    def draw_kill_count(self, surface, level: int, player):
        if not player:
            return
        text_surf = self.fonts.text.render(f'Level: {level}  Kills: {player.kill_count}', True, (255, 255, 255))
        bg = pygame.Surface((text_surf.get_width() + 12, text_surf.get_height() + 8), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 120))
        surface.blit(bg, (8, 8))
        surface.blit(text_surf, (14, 12))

    def draw_level_announce(self, surface, level: int, dt: float):
        if self.level_announce_timer <= 0:
            return
        self.level_announce_timer -= dt
        ratio = max(0, self.level_announce_timer / self.level_announce_duration)
        alpha = int(255 * ratio)
        text_surf = self.fonts.level.render(f'Level {level}', True, (255, 255, 255))
        padding = 40
        box = pygame.Surface((text_surf.get_width() + padding, text_surf.get_height() + padding), pygame.SRCALPHA)
        box.fill((0, 0, 0, int(160 * ratio)))
        box_rect = box.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        text_rect = text_surf.get_rect(center=box_rect.center)
        tmp = text_surf.copy()
        tmp.set_alpha(alpha)
        surface.blit(box, box_rect)
        surface.blit(tmp, text_rect)
