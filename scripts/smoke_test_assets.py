import sys
from pathlib import Path
import pygame
from pygame.math import Vector2 as vector

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.entity.player import Player
from configs.settings import *


def dummy_shoot(position, direction, entity):
    pass


def main():
    pygame.init()
    # Create a small window to allow convert_alpha to work
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    all_sprites = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()

    try:
        player = Player(position=(100, 100), groups=[all_sprites], path='assets/graphics/player', collision_sprites=collision_sprites, shoot=dummy_shoot)
        print("SMOKE_OK: Player assets loaded. Animations keys:", sorted(player.animations.keys()))
    except Exception as e:
        print("SMOKE_FAIL:", repr(e))
        raise
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
