import pygame
from os.path import join

class Tile(pygame.sprite.Sprite):
    def __init__ (self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('green')
        self.rect = self.image.get_frect(topleft=pos)
        
    def update(self, x_shift):
        self.rect.x += x_shift   # type: ignore