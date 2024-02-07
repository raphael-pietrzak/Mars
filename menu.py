from settings import *
from pygame import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos
import pygame
from random import choice


class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.is_active = False
        self.create_buttons()

    def create_buttons(self):
        # menu_area
        size1 = vector(50, 50)
        size2 = vector(200, 600)
        margin = vector(6, 6)
        topleft1 = (0 + margin.x, WINDOW_HEIGHT - margin.y - size1.y)
        topleft2 = (0 + margin.x, WINDOW_HEIGHT - margin.y - size2.y)
        self.rect1 = pygame.Rect(topleft1, size1)
        self.rect2 = pygame.Rect(topleft2, size2)

        self.surface1 = pygame.Surface(size1)
        self.surface2 = pygame.Surface(size2)
        self.surface1.fill('grey')
        self.surface2.fill('beige')

        self.surface = self.surface2 if self.is_active else self.surface1
        self.rect = pygame.Rect((6,0), (300, WINDOW_HEIGHT-6))

        self.close_box =  pygame.Surface((30, 30))
        self.close_box.fill('red')
        close_box_topleft = (self.rect2.width - self.close_box.get_width(), 0)
        self.surface2.blit(self.close_box, close_box_topleft )
    


    
    def click(self):
        if not self.is_active :
            self.toggle()   


    def toggle(self):
        self.is_active = not self.is_active
        self.surface = self.surface2 if self.is_active else self.surface1
        self.rect = self.rect2 if self.is_active else self.rect1

    def display(self):
        rect =  self.surface.get_rect()
        rect.bottomleft = self.rect.bottomleft
        self.display_surface.blit(self.surface, rect)

        
class SubMenu:
    def __init__(self, surface):
        self.items = ['A', 'B', 'C']


    def update(self):
        pass
