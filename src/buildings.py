import pygame
from pygame.sprite import Sprite
from pygame import Vector2 as vector

from src.coordinates import isoToScreen
import src.settings as settings
from src.settings import *

class Building(Sprite):
    def __init__(self, group, cluster, index):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()
        self.origin = vector()
        self.index = index

        self.import_data()
        self.cluster = cluster
        self.barycenter = self.get_barycenter()
        self.leaves = 0
    
    def import_data(self):
        self.income = BUILDINGS[self.index]['income']

    def update_leaves(self, dt):
        self.leaves += dt * self.income / 10

    def get_leaves(self):
        production = int(self.leaves)
        self.leaves -= production
        return production

    def draw_isometric_diamond(self, iso_pos):
        center = self.origin + isoToScreen(iso_pos)
        x, y = (settings.TILE_SIZE, settings.TILE_SIZE//2)
        points = [
            (x, y - settings.TILE_SIZE // 2),    # Point haut
            (x + settings.TILE_SIZE , y),        # Point droit
            (x, y + settings.TILE_SIZE // 2),    # Point bas
            (x - settings.TILE_SIZE, y)          # Point gauche
        ]
        points = [(x + center[0], y + center[1]) for x, y in points]
        color = 'white'

        pygame.draw.polygon(self.display_surface, color, points, 4)
    
    def get_barycenter(self):
        x = sum([pos[0] for pos in self.cluster]) / len(self.cluster)
        y = sum([pos[1] for pos in self.cluster]) / len(self.cluster)
        return (x, y)

    def draw_leaves_production(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"{int(self.leaves)}", True, 'green')
        pos = self.origin + isoToScreen(self.barycenter)
        self.display_surface.blit(text, pos)

    def draw(self):
        for pos in self.cluster:
            self.draw_isometric_diamond(pos)
        # self.draw_leaves_production()
    
    
    def update(self, origin, dt):
        self.origin = origin
        self.update_leaves(dt)
        self.draw()

        
        

