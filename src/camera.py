import pygame
from pygame.sprite import Group
from pygame import Vector2 as vector

import src.settings as settings
from src.coordinates import isoToScreen

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offsets = [(0, 0), (-1, 0), (0, -1), (-1, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
        self.origin = vector(0, 0)
        
    def draw_4_times(self):
        for offset in self.offsets:
            tiles_offset = vector(offset) * settings.MAP_SIZE
            screen_offset = isoToScreen(tiles_offset)
            self.draw(screen_offset)
    
    def draw(self, offset):
        for sprite in self.sprites():
            sprite.draw(self.origin + offset)

    def update(self, origin, dt):
        self.origin = origin
        for sprite in self.sprites():
            sprite.update(dt, self.origin)