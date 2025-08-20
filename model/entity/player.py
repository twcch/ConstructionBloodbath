import pygame
from pygame.math import Vector2 as vector
from configs.settings import *
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, path, collision_sprites):
        super().__init__(groups)  # Sprite 的建構子就會自動幫你把自己加入到這些 Group 裡
        self.import_assets(path)  # 載入玩家資源
        self.frame_index = 0  # 當前動畫幀索引
        self.status = 'right'  # 當前動畫狀態 (方向)
        
        self.image = self.animations[self.status][self.frame_index]  # 初始圖片
        self.rect = self.image.get_rect(topleft=position)
        self.z = LAYERS['Level']

        # float variables for movement
        # 速度 (像素/秒)。搭配 dt (秒) 讓移動與幀率無關
        self.direction = vector()
        self.position = vector(self.rect.topleft)
        self.speed = 400
        
        # collision
        self.old_rect = self.rect.copy()  # 用來儲存上幀的 rect，避免碰撞檢測時使用當前 rect 導致錯誤
        self.collision_sprites = collision_sprites  # 碰撞用的群組
        
        # vertical movement
        self.gravity = 15  # 重力加速度
        self.jump_speed = 600  # 跳躍速度
        self.on_floor = False  # 是否在地面上
        self.duck = False  # 是否蹲下

    def get_stauts(self):
        # idle
        if self.direction.x == 0 and self.on_floor:
            self.status = self.status.split('_')[0] + '_idle'
        
        # jump
        if self.direction.y != 0 and not self.on_floor:
            self.status = self.status.split('_')[0] + '_jump'

        # duck
        if self.duck and self.on_floor:
            self.status = self.status.split('_')[0] + '_duck'

    def check_contact(self):
        bottom_rect = pygame.Rect(0, 0, self.rect.width, 5)
        bottom_rect.midtop = self.rect.midbottom
        
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(bottom_rect):
                if self.direction.y > 0:
                    self.on_floor = True
    
    def import_assets(self, path):
        # 這裡可以載入玩家的圖片、音效等資源
        self.animations = {}
        
        # Walk through the directory structure
        for index, (root, dirs, files) in enumerate(walk(path)):
            if index == 0:
                # First iteration - initialize animation lists for each direction
                for name in dirs:
                    self.animations[name] = []
            else:
                # Get the animation direction from the folder name
                direction = root.split('/')[-1]  # Use / for Unix-style paths
                
                # Sort files numerically and load each frame
                for filename in sorted(files, key=lambda string: int(string.split('.')[0])):
                    file_path = f"{root}/{filename}"  # Use / for Unix-style paths
                    surface = pygame.image.load(file_path).convert_alpha()
                    self.animations[direction].append(surface)

    def animate(self, dt):
        # 更新動畫幀索引
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        
        self.image = self.animations[self.status][int(self.frame_index)]
            
    # get the player input (all arrow keys: left, right, up, down)
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_floor:
            self.direction.y = -self.jump_speed
            
        if keys[pygame.K_DOWN]:
            self.duck = True
        else:
            self.duck = False

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    # left collision
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.rect.right:
                        self.rect.left = sprite.rect.right
                    # right collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.rect.left:
                        self.rect.right = sprite.rect.left
                    
                    self.position.x = self.rect.x
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.on_floor = True
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    self.position.y = self.rect.y
                    self.direction.y = 0
                    
        if self.on_floor and self.direction.y != 0:
            self.on_floor = False
        
    
    # use the input to move the player
    def move(self, dt):
        # 修正蹲下移動
        if self.duck and self.on_floor:
            self.direction.x = 0
        
        # 浮點座標 vs 畫面座標分離
        # self.position: float (高精度、可累積細小位移，不受取整誤差影響)
        # self.rect: int (pygame blit 需要整數像素)
        # 每幀: 更新 position (float) → 再同步到 rect (int)
        
        # horizontal movement
        self.position.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.position.x)
        self.collision('horizontal')

        # vertical movement
        # gravity
        self.direction.y += self.gravity  # 重力影響
        self.position.y += self.direction.y * dt
        self.rect.y = round(self.position.y)
        self.collision('vertical')

    def update(self, dt):
        self.old_rect = self.rect.copy()
        
        self.input()
        self.get_stauts()
        self.move(dt)
        self.check_contact()
        self.animate(dt)