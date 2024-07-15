
import pygame
from pygame import Vector2 as vector

from src.settings import ASSETS

class Stock:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.leaves = 0
        self.import_assets()

    def import_assets(self):
        self.leaf_counter_image = pygame.image.load(ASSETS[0]['path'])
        self.leaf_counter_rect = self.leaf_counter_image.get_rect(topleft=(0, 0))

        # Settings button
        self.objectives_button_image = pygame.image.load(ASSETS[2]['path'])
        self.objectives_button_rect = self.objectives_button_image.get_rect(topleft=(500, 0))

    def add(self, amount):
        self.leaves += amount

    def print_leaf_counter(self, rect):
        mid_right = rect.midright
        mid_right_offset = vector(-10, -25)
        font_path = 'assets/fonts/more-sugar.regular.ttf'
        font = pygame.font.Font(font_path, 50)
        text = font.render(str(self.leaves), True, (255, 255, 255))
        text_rect = text.get_rect(midright=mid_right + mid_right_offset)
        self.display_surface.blit(text, text_rect)

    def draw_leaf_counter(self):
        self.display_surface.blit(self.leaf_counter_image, (0, 0))
        self.print_leaf_counter(self.leaf_counter_rect)

    def draw_settings_button(self):
        self.display_surface.blit(self.objectives_button_image, (500, 0))

    def draw(self):
        self.draw_leaf_counter()
        self.draw_settings_button()
