
import pygame
from pygame import Vector2 as vector

from src.settings import ASSETS

class StockMenu:
    def __init__(self, stock):
        self.display_surface = pygame.display.get_surface()
        self.import_assets()
        self.stock = stock

    # import
    def import_assets(self):
        self.leaf_counter_image = pygame.image.load(ASSETS[0]['path'])
        self.leaf_counter_rect = self.leaf_counter_image.get_rect(topleft=(0, 0))

    # draw
    def draw_count(self):
        mid_right = self.leaf_counter_rect.midright
        mid_right_offset = vector(-10, -25)
        font_path = 'assets/fonts/more-sugar.regular.ttf'
        font = pygame.font.Font(font_path, 50)
        leaves = self.stock.leaves
        text = font.render(str(leaves), True, (255, 255, 255))
        text_rect = text.get_rect(midright=mid_right + mid_right_offset)
        self.display_surface.blit(text, text_rect)

    def draw_background(self):
        self.display_surface.blit(self.leaf_counter_image, (0, 0))

    def draw(self):
        self.draw_background()
        self.draw_count()