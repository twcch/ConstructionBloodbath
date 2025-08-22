import os
import pygame
from configs.settings import FONT_DEFAULT

class FontManager:
    def __init__(self, base_path: str | None = FONT_DEFAULT):
        self.base_path = base_path

    def load(self, size: int) -> pygame.font.Font:
        path = self.base_path
        if not path or not os.path.exists(path):
            return pygame.font.Font(None, size)
        try:
            return pygame.font.Font(path, size)
        except Exception:
            return pygame.font.Font(None, size)

class GameFonts:
    def __init__(self, fm: FontManager):
        self.title = fm.load(72)
        self.text = fm.load(32)
        self.level = fm.load(96)
        self.credits_title = fm.load(72)
        self.credits_line = fm.load(32)
