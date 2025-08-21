import pygame
from pygame.math import Vector2 as vector
from configs.settings import *
from os import walk
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, position, path, groups, shoot):
        super().__init__(groups)
        
        # graphics setup
        self.import_assets(path)  # 載入玩家資源
        self.frame_index = 0  # 當前動畫幀索引
        self.status = 'right'  # 當前動畫狀態 (方向)
        
        # image setup
        self.image = self.animations[self.status][self.frame_index]  # 初始圖片
        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()  # 用來儲存上幀的 rect，避免碰撞檢測時使用當前 rect 導致錯誤
        self.z = LAYERS['Level']
        self.mask = pygame.mask.from_surface(self.image)  # 用於碰撞檢測的遮罩
        
        # float variables for movement
        # 速度 (像素/秒)。搭配 dt (秒) 讓移動與幀率無關
        self.direction = vector()
        self.position = vector(self.rect.topleft)
        self.speed = 400
        
        # shooting setup
        self.shoot = shoot  # 射擊方法
        self.can_shoot = True  # 是否可以射擊
        self.shoot_time = None
        self.cooldown = 200
        self.duck = False  # 是否蹲下
        
        # health
        self.health = 1  # 初始生命值
        self.is_vulnerable = True
        self.hit_time = None  # 用來記錄被擊中的時間
        self.invul_duration = 500
    
    def blink(self):
        if not self.is_vulnerable:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surface = mask.to_surface()
                white_surface.set_colorkey((0, 0, 0))  # 設置透明色
                self.image = white_surface
                
                    
    def wave_value(self):
        value = sin(pygame.time.get_ticks() / 200) * 10
        if value >= 0:
            return True
        
        return False

    def damage(self):
        if self.is_vulnerable:
            self.health -= 1
            self.is_vulnerable = False
            self.hit_time = pygame.time.get_ticks()
        
    def check_death(self):
        if self.health <= 0:
            self.kill()
    
    def animate(self, dt):
        # 更新動畫幀索引
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        
        self.image = self.animations[self.status][int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)  # 用於碰撞檢測的遮罩

    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown:
                self.can_shoot = True

    def invul_timer(self):
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > self.invul_duration:
                self.is_vulnerable = True
    
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