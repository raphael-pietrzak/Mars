
import pygame
from pygame.sprite import Sprite
from pygame import Vector2 as vector

from ..settings import MAP_SIZE, BUILDINGS, TILE_SIZE_DEFAULT
from ..utils import isoToScreen, load_image, rotate_90_clockwise
import src.settings as settings

class Building(Sprite):
    def __init__(self, group, cluster, index):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()
        self.origin = vector()
        self.index = index
        self.paths = ['0.png', '1.png', '2.png', '3.png']
        self.image_index = 0

        self.import_images()
        self.cluster = cluster
        self.barycenter = self.get_barycenter()
        self.leaves = 0

        self.test_active = False
        self.income = BUILDINGS[self.index]['income']
    
    def import_images(self):
        self.images = []
        for path in self.paths:
            self.images.append(load_image(path))

        self.scale_image()
    
    def scale_image(self):
        self.factor = (settings.TILE_SIZE / TILE_SIZE_DEFAULT) 
        image_factor = 1/3 * self.factor
        self.image = self.images[self.image_index]
        self.image = pygame.transform.scale_by(self.image, image_factor)
        self.rect = self.image.get_rect()

    
    def zoom(self):
        self.scale_image()
        

    def rotate(self):
        self.cluster = [rotate_90_clockwise(pos) for pos in self.cluster]
        self.cluster = [(x%MAP_SIZE, y%MAP_SIZE) for x, y in self.cluster]
        self.barycenter = self.get_barycenter()
        self.image_index = (self.image_index + 1) % 4
        self.scale_image()

    def update_leaves(self, dt):
        self.leaves += dt * self.income / 10

    def get_leaves(self):
        production = int(self.leaves)
        self.leaves -= production
        return production

    def draw_isometric_diamond(self, iso_pos):
        center = self.origin + isoToScreen(iso_pos)

        x, y = center 
        points = [
            (x, y - settings.TILE_SIZE // 2),    # Point haut
            (x + settings.TILE_SIZE , y),        # Point droit
            (x, y + settings.TILE_SIZE // 2),    # Point bas
            (x - settings.TILE_SIZE, y)          # Point gauche
        ]
        
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

    def draw(self, origin):
        self.rect.center = origin + isoToScreen(self.cluster[0])
        self.display_surface.blit(self.image, self.rect)
        self.origin = origin

        if self.test_active:
            for pos in self.cluster:
                self.draw_isometric_diamond(pos)
            
            pygame.draw.rect(self.display_surface, 'red', self.rect, 2)
            pygame.draw.circle(self.display_surface, 'red', self.rect.center, 10)


    
    def update_rect(self):
        pass
    
    def update(self, dt, origin):
        self.origin = origin
        self.update_leaves(dt)

        
        

