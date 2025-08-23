import pygame
from configs.settings import WINDOW_WIDTH, WINDOW_HEIGHT

class CreditsScene:
    def __init__(self, app):
        self.app = app
        self.lines = [
            "THANK YOU FOR PLAYING",
            "感謝遊玩本遊戲！",
            "=========================",
            "【製作團隊】",
            "    國立成功大學 工程科學系 謝志謙",
            "    國立成功大學 工程科學系 黃紹恩",
            "=========================",
            "特別感謝!!",
            "Press ANY KEY to return to Menu"
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.app.change_scene('menu')

    def draw(self, surface):
        surface.fill((0, 0, 0))
        title_surf = self.app.fonts.credits_title.render(self.lines[0], True, (255,255,255))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT*0.25))
        surface.blit(title_surf, title_rect)
        start_y = title_rect.bottom + 40
        for i, line in enumerate(self.lines[1:]):
            surf = self.app.fonts.credits_line.render(line, True, (220,220,220))
            rect = surf.get_rect(center=(WINDOW_WIDTH/2, start_y + i * 50))
            surface.blit(surf, rect)

    def update(self, dt: float):
        pass
