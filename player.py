import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.character_assets()
        self.frame_index = 0
        self.animation_speed = 0.05
        self.image = self.animations['idle'][self.frame_index]   
        #self.image = pygame.Surface((80,60)) 
        self.rect = self.image.get_frect(topleft = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 3
        self.gravity = 0.06
        self.jump_speed = -6
        
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False 
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
    
    def character_assets(self):
        character_path = 'graphics/character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation 
            self.animations[animation] = import_folder(full_path)
  
    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            
        if self.on_ground and self.on_right:
            self.rect = self.image.get_frect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_frect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_frect(midbottom = self.rect.midbottom)
        
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_frect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_frect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_frect(midtop = self.rect.midtop)
            
    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        
        if self.direction.x > 0:
            self.facing_right = True
        elif self.direction.x < 0:
            self.facing_right = False
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
    
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 0.05:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y      # type: ignore
    
    def jump(self):
        self.direction.y = self.jump_speed
        
    def update(self):
        self.input()
        self.get_status()
        self.animate()
        
        
