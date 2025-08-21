import pygame
from pytmx.util_pygame import load_pygame
from pathlib import Path
from xml.etree import ElementTree

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
