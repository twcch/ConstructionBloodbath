import pygame
from pytmx.util_pygame import load_pygame

class AssetManager:
    def __init__(self):
        self._images: dict[str, pygame.Surface] = {}
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._tmx: dict[str, object] = {}
    
    def image(self, path: str) -> pygame.Surface:
        if path not in self._images:
            self._images[path] = pygame.image.load(path).convert_alpha()
        return self._images[path]

    def sound(self, path: str) -> pygame.mixer.Sound:
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)
        return self._sounds[path]

    def tmx(self, path: str):
        if path not in self._tmx:
            self._tmx[path] = load_pygame(path)
        return self._tmx[path]