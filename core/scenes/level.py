import pygame
from configs.settings import BG_COLOR, BULLET_IMG, asset_path
from core.systems.collisions import CollisionSystem
from core.systems.shooting import ShootingSystem

class LevelScene:
    def __init__(self, app):
        self.app = app
        self.lm = app.level_manager
        # Systems filled in on enter when assets ready
        self.collision_system: CollisionSystem | None = None
        self.shooting: ShootingSystem | None = None

    def enter(self):
        # setup shooting system first so callback exists
        self.shooting = ShootingSystem(self.lm, self.app.bullet_surf, self.app.fire_surfs)
        self.lm.build_level(1, self.shooting.shoot)
        if self.lm.player:
            self.lm.player.kill_count = 0
        self.collision_system = CollisionSystem(self.lm)
        self.app.hud.start_level_announce()

    def update(self, dt: float):
        player = self.lm.player
        if not player:
            return
        if self.collision_system:
            self.collision_system.platform_collisions()
        if self.lm.all_sprites:
            self.lm.all_sprites.update(dt)
        if self.collision_system:
            self.collision_system.bullet_collisions()

        # level progression
        if self.lm.needs_advance():
            if self.lm.next_level_exists():
                preserved = player.kill_count
                next_level = self.lm.current_level + 1
                self.lm.build_level(next_level, self.shooting.shoot if self.shooting else None)
                if self.lm.player:
                    self.lm.player.kill_count = preserved
                self.app.hud.start_level_announce()
            else:
                self.app.change_scene('credits')

        # death returns to menu
        if player.health <= 0 or not player.alive():
            self.app.change_scene('menu')

    def draw(self, surface):
        surface.fill(BG_COLOR)
        if self.lm.all_sprites:
            self.lm.all_sprites.render(self.lm.player)
        if self.lm.overlay:
            self.lm.overlay.display()
        self.app.hud.draw_kill_count(surface, self.lm.current_level, self.lm.player)
        # level announce uses last dt stored in app
        self.app.hud.draw_level_announce(surface, self.lm.current_level, self.app.dt_last)
