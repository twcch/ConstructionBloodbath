import pygame
from configs.settings import WINDOW_WIDTH, WINDOW_HEIGHT, MENU_BG_IMAGE, MENU_BG_COLOR, MENU_TITLE_COLOR, MENU_TEXT_COLOR, TITLE

class MenuScene:
    def __init__(self, app):
        self.app = app
        self.bg = None
        try:
            raw = self.app.assets.image(MENU_BG_IMAGE)
            self.bg = pygame.transform.scale(raw, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception:
            pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.app.change_scene('level')
            if event.key == pygame.K_ESCAPE:
                self.app.running = False

    def draw(self, surface):
        if self.bg:
            surface.blit(self.bg, (0, 0))
        else:
            surface.fill(MENU_BG_COLOR)
        title_surf = self.app.fonts.title.render(TITLE, True, MENU_TITLE_COLOR)
        title_surf_2 = self.app.fonts.text.render('- 台南洛聖都 -', True, MENU_TEXT_COLOR)
        tip_surf = self.app.fonts.text.render('Press ENTER / SPACE to Start  |  ESC to Quit', True, MENU_TEXT_COLOR)
        surface.blit(title_surf, title_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 60)))
        surface.blit(title_surf_2, title_surf_2.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 20)))
        surface.blit(tip_surf, tip_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 40)))

    def update(self, dt: float):
        pass
