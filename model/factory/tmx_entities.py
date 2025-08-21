import pygame

from configs.settings import LAYERS
from model.entity.combatant.enemy import Enemy
from model.entity.combatant.player import Player
from model.entity.tile import Tile, CollisionTile, MovingPlatform
from model.service.assets import AssetManager


class TMXEntityFactory:
    def __init__(
            self,
            assets: AssetManager,
            all_sprites: pygame.sprite.Group,
            collision_sprites: pygame.sprite.Group,
            platform_sprites: pygame.sprite.Group,
            vulnerable_sprites: pygame.sprite.Group,
            shoot_cb
    ):
        self.assets = assets
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.platform_sprites = platform_sprites
        self.vulnerable_sprites = vulnerable_sprites
        self.shoot_cb = shoot_cb

    def build_world(self, tmx_path: str):
        tmx_map = self.assets.tmx(tmx_path)

        # collision tiles
        for x, y, surf in tmx_map.get_layer_by_name('Level').tiles():
            CollisionTile(
                position=(x * 64, y * 64),
                surface=surf,
                groups=[self.all_sprites, self.collision_sprites]
            )

        # decorative tiles
        for layer in ['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile(
                    position=(x * 64, y * 64),
                    surface=surf,
                    groups=self.all_sprites,
                    z=LAYERS[layer]
                )

        # entities
        player = None
        enemies_buffer = []

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                player = Player(
                    position=(obj.x, obj.y),
                    groups=[self.all_sprites, self.vulnerable_sprites],
                    path='assets/graphics/player',
                    collision_sprites=self.collision_sprites,
                    shoot=self.shoot_cb
                )
            elif obj.name == 'Enemy':
                enemies_buffer.append(obj)

        # spawn enemies after player exists (避免層順序造成 player=None)
        for obj in enemies_buffer:
            Enemy(
                position=(obj.x, obj.y),
                path='assets/graphics/enemy',
                groups=[self.all_sprites, self.vulnerable_sprites],
                shoot=self.shoot_cb,
                player=player,
                collision_sprites=self.collision_sprites
            )

        # moving platforms + borders
        platform_border_rects: list[pygame.Rect] = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == 'Platform':
                MovingPlatform(
                    position=(obj.x, obj.y),
                    surface=obj.image,
                    groups=[self.all_sprites, self.collision_sprites, self.platform_sprites]
                )
            else:
                platform_border_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        return player, platform_border_rects
