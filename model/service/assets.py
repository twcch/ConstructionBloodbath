import pygame
from pytmx.util_pygame import load_pygame
from pathlib import Path
from xml.etree import ElementTree
import json


class AssetManager:
    def __init__(self):
        # caches
        self._images = {}
        self._sounds = {}
        self._tmx = {}
        self._json = {}

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
            # Pre-validate TMX and external TSX to surface clearer errors
            try:
                root = ElementTree.parse(path).getroot()
                tmx_dir = Path(path).parent
                for ts in root.findall('tileset'):
                    src = ts.get('source')
                    if src:
                        tsx_path = (tmx_dir / src).resolve()
                        if not tsx_path.exists():
                            raise FileNotFoundError(f"Tileset not found: {tsx_path}")
                        try:
                            ElementTree.parse(tsx_path)
                        except ElementTree.ParseError as e:
                            raise ElementTree.ParseError(f"Failed to parse TSX: {tsx_path}: {e}") from e
            except Exception:
                # Re-raise to keep original traceback visible in console
                raise

            self._tmx[path] = load_pygame(path)
        return self._tmx[path]

    def json(self, path: str):
        """Load and cache a JSON configuration file.

        Returns parsed python object (dict/list)."""
        if path not in self._json:
            with open(path, 'r', encoding='utf-8') as f:
                self._json[path] = json.load(f)
        return self._json[path]
