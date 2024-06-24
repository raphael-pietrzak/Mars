import pygame
from pygame import sprite
from pygame import Vector2 as vector
from src.coordinates import isoToScreen, screenToIso
from src.settings import *

class Building(sprite.Sprite):
    def __init__(self, group, screen_pos, iso_pos):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()
        self.pos = iso_pos
        self.screen_pos = screen_pos



    def draw_isometric_diamond(self, center):
        x, y = (TILE_SIZE, TILE_SIZE//2)
        points = [
            (x, y - TILE_SIZE // 2),    # Point haut
            (x + TILE_SIZE , y),        # Point droit
            (x, y + TILE_SIZE // 2),    # Point bas
            (x - TILE_SIZE, y)          # Point gauche
        ]
        points = [(x + center[0], y + center[1]) for x, y in points]
        color = 'white'

        pygame.draw.polygon(self.display_surface, color, points, 4)

    def draw(self, origin):
        pos = origin + self.screen_pos
        self.draw_isometric_diamond(pos)
    
    def update(self, origin):
        self.draw(origin)
        
        

