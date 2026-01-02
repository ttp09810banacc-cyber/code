# gọi
import pygame
from tiles import Tile
from setting import *
from player import *

class Level():
    def __init__(self,level_data,surf):
        # vẽ thế giới
        self.display_surf = surf
        self.setup_level(level_data)

        # độ dịch chuyển của thế giới
        self.world_shift =  0
        self.current_x = 0
        
    def setup_level(self, layout):
        # tạo group
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        
        # tạo ô và add vào group
        for row_index ,row in enumerate(layout): 
            #print(row)
            #print(row_index)
            for col_index ,cell in enumerate(row): 
                #print(f"{row_index},{col_index}:{cell}")
                x = tile_size * col_index
                y = tile_size * row_index
                
                if cell == 'X':
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
      
    def scroll_x(self):
        # gọi
        player = self.player.sprite
        player_x = player.rect.centerx  
        direction_x = player.direction.x    
        
        # đặt giới hạn screen
        if player_x < screen_width // 4 and direction_x < 0:
            self.world_shift = 1
            player.speed = 0    
            
        elif player_x > screen_width - (screen_width // 4) and direction_x > 0:
            self.world_shift = -1
            player.speed = 0   
            
        else:
            self.world_shift = 0
            player.speed = 1    
    
    def horizontal_movement(self):
        # va chạm ngang
        player = self.player.sprite
        # uppdate rect
        player.rect.x += player.direction.x * player.speed    
        
        # kiểm tra va chạm
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        
        if player.on_left and player.rect.left < self.current_x or player.direction.x >= 0:
            player.on_left = False
        elif player.on_right and player.rect.right > self.current_x or player.direction.x <= 0:
            player.on_right = True
                    
    def vertical_movement(self):
        # va chạm dọc
        player = self.player.sprite
        player.apply_gravity()   
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    
        if player.on_ground and (player.direction.y < 0 or player.direction.y > 0.05):
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
        
    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surf)

        self.scroll_x()

        self.player.update()
        self.horizontal_movement()
        self.vertical_movement()

        self.player.draw(self.display_surf)
