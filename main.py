# gọi
import pygame, sys
from setting import *
from level import Level     

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map,screen) # level_map để tạo map, screen để vẽ lên (tham số trong init)

# vòng lặp
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('black')
    level.run()
    
    pygame.display.update()
