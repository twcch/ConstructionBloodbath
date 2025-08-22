import pygame

class CollisionSystem:
    def __init__(self, level_manager):
        self.lm = level_manager

    def platform_collisions(self):
        player = self.lm.player
        if not player:
            return
        for platform in self.lm.platform_sprites.sprites():
            for border in self.lm.platform_border_rects:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0:
                        platform.rect.top = border.bottom
                        platform.position.y = platform.rect.y
                        platform.direction.y = 1
                    else:
                        platform.rect.bottom = border.top
                        platform.position.y = platform.rect.y
                        platform.direction.y = -1
            if platform.rect.colliderect(player.rect) and player.rect.centery > platform.rect.centery:
                platform.rect.bottom = player.rect.top
                platform.position.y = platform.rect.y
                platform.direction.y = -1

    def bullet_collisions(self):
        pygame.sprite.groupcollide(self.lm.bullet_sprites, self.lm.collision_sprites, True, False)
        hits = pygame.sprite.groupcollide(
            self.lm.bullet_sprites, self.lm.vulnerable_sprites, True, False, collided=pygame.sprite.collide_mask
        )
        for _, targets in hits.items():
            for target in targets:
                target.damage()
