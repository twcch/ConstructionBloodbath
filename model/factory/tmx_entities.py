import pygame

from configs.settings import LAYERS, PLAYER_DIR, ENEMY_DIR
from model.entity.combatant.enemy import Enemy
from model.entity.combatant.player import Player
from model.entity.tile import Tile, CollisionTile, MovingPlatform
from model.service.assets import AssetManager


class TMXEntityFactory:
    """
    Factory for instantiating game world entities and tiles from a Tiled TMX map.

    This class orchestrates the creation of:
    - Collision tiles from the 'Level' tile layer.
    - Decorative tiles from 'BG', 'BG Detail', 'FG Detail Bottom', and 'FG Detail Top' tile layers,
        using a LAYERS mapping for draw-order (z-index).
    - Player and enemy entities from the 'Entities' object layer (spawning enemies after the player
        to ensure they can reference the player).
    - Moving platforms and platform border rects from the 'Platforms' object layer.

    Side effects:
    - Populates the provided sprite groups with created sprites.
    - Returns a reference to the spawned player (or None) and a list of platform border rectangles.

    Assumptions:
    - Tile coordinates are in grid units and converted to pixels using a 64px tile size.
    - The TMX map contains the expected layers by name: 'Level', 'BG', 'BG Detail',
        'FG Detail Bottom', 'FG Detail Top', 'Entities', and 'Platforms'.
    - Object names in the 'Entities' layer are 'Player' or 'Enemy'.
    - Object names in the 'Platforms' layer named 'Platform' are moving platforms; all others are
        treated as platform border regions.

    Raises:
    - KeyError if any required TMX layers are missing.
    - AttributeError or TypeError if TMX objects/layers do not provide expected attributes.
    """
    """
    Initialize the TMXEntityFactory.

    Args:
            assets (AssetManager): Asset manager capable of loading TMX maps via assets.tmx(path).
            all_sprites (pygame.sprite.Group): Group containing every drawable/updatable sprite.
            collision_sprites (pygame.sprite.Group): Group used for collision detection/response.
            platform_sprites (pygame.sprite.Group): Group containing moving platforms.
            vulnerable_sprites (pygame.sprite.Group): Group of entities that can take damage.
            shoot_cb (Callable): Callback passed to entities to handle shooting logic.

    Notes:
    - The provided groups are mutated: created sprites are added to one or more of them.
    - The shoot callback is forwarded to Player and Enemy instances.
    """
    """
    Build the world from a TMX file and return key references.

    Loads the TMX map, instantiates tiles and entities into the provided sprite groups,
    and collects platform border rectangles.

    Processing details:
    - Collision tiles:
        - From the 'Level' tile layer; each tile is placed at (x * 64, y * 64).
    - Decorative tiles:
        - From 'BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top'; each tile is placed at
            (x * 64, y * 64) with z-order determined by LAYERS[layer].
    - Entities:
        - From the 'Entities' object layer.
        - Spawns the Player first (obj.name == 'Player').
        - Buffers enemies (obj.name == 'Enemy') and spawns them after the player is created so enemies
            can reference the player instance.
    - Platforms:
        - From the 'Platforms' object layer.
        - Objects named 'Platform' become MovingPlatform sprites (added to all_sprites, collision_sprites,
            and platform_sprites).
        - Other objects are converted into pygame.Rect instances and returned as platform borders.

    Args:
            tmx_path (str): Filesystem path to the TMX file to load.

    Returns:
            tuple[Player | None, list[pygame.Rect]]:
                    - The Player instance if one was defined in the TMX map; otherwise None.
                    - A list of rectangles representing platform border regions.

    Raises:
            KeyError: If any required TMX layers are missing.
            AttributeError: If TMX objects/layers do not provide expected attributes (e.g., obj.x, obj.y).
            Exception: Propagates exceptions from the asset loader (assets.tmx).

    Side effects:
            - Mutates sprite groups by adding created sprites.
    """
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
                    path=str(PLAYER_DIR),
                    collision_sprites=self.collision_sprites,
                    shoot=self.shoot_cb
                )
            elif obj.name == 'Enemy':
                enemies_buffer.append(obj)

        # spawn enemies after player exists (避免層順序造成 player=None)
        for obj in enemies_buffer:
            Enemy(
                position=(obj.x, obj.y),
                path=str(ENEMY_DIR),
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
