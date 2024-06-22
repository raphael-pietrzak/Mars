import pygame
from settings import *
from pygame import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_pressed
from math import floor
from coordinates import isoToScreen, screenToIso

class Menu:
    def __init__(self, add_tile, tiles_map):
        self.display_surface = pygame.display.get_surface()
        self.rect_group = []
        self.add_tile = add_tile
        self.tiles_map = tiles_map

        # import 
        self.import_assets()

        # menu
        self.buttons = []
        self.create_menu()

        # preview
        self.preview = None
        self.preview_active = False

        # rect
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect.topleft = (0, 0)

        self.leaves = 3000

    
    def import_assets(self):
        self.leaf_counter_image = pygame.image.load(ASSETS[0]['path'])
        self.leaf_counter_rect = self.leaf_counter_image.get_rect(topleft=(0, 0))


        # Settings button
        self.settings_button_image = pygame.image.load(ASSETS[1]['path'])
        self.objectives_button_image = pygame.image.load(ASSETS[2]['path'])
        self.settings_button_rect = self.settings_button_image.get_rect(topleft=(400, 0))
        self.objectives_button_rect = self.objectives_button_image.get_rect(topleft=(500, 0))

        # Buildings bar
        self.buildings_bar_image = pygame.image.load(ASSETS[4]['path'])
        self.building_image = pygame.image.load(ASSETS[3]['path'])
        mid_bottom = self.display_surface.get_rect().midbottom
        self.buildings_bar_rect = self.buildings_bar_image.get_rect(midbottom=mid_bottom)


        self.rect_group.append(self.leaf_counter_rect)
        self.rect_group.append(self.buildings_bar_rect)
        self.rect_group.append(self.settings_button_rect)
        self.rect_group.append(self.objectives_button_rect)

    def create_menu(self):
        for i in range(4):
            mid_left = self.buildings_bar_rect.midleft + vector(i * 150, 0)
            building_rect = self.building_image.get_rect(midleft=mid_left)
            button = Button(self.building_image, building_rect, i)
            self.buttons.append(button)


    # events
    def click_event(self):
        # drag
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos()) and mouse_pressed()[0]:
                self.preview = Preview(button.index, self.tiles_map)
                self.preview_active = True
                break
        
        # drop
        if self.preview_active and not mouse_pressed()[0]:
            if self.leaves >= 100 and self.preview.is_valid_position():
                self.leaves -= 100
                self.add_tile(self.preview.iso_pos)
            self.preview_active = False
            self.preview = None

    def collidepoint(self, pos):
        for rect in self.rect_group:
            if rect.collidepoint(pos):
                return True
        return False

    # draw
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
        self.display_surface.blit(self.settings_button_image, (400, 0))
        self.display_surface.blit(self.objectives_button_image, (500, 0))

    def draw_buildings_bar(self):
        self.display_surface.blit(self.buildings_bar_image, self.buildings_bar_rect)
        for button in self.buttons:
            button.draw()

    def draw_preview(self, origin):
        if self.preview:
            self.preview.draw(origin)

    def draw_tile_test(self):
        tile_test_image = pygame.image.load(ASSETS[5]['path'])
        # self.display_surface.blit(tile_test_image, (0, 0))

    def draw(self, origin):
        self.draw_preview(origin)
        self.draw_leaf_counter()
        self.draw_settings_button()
        self.draw_buildings_bar()
        self.draw_tile_test()



class Button:
    def __init__(self, image, rect, index):
        self.display_surface = pygame.display.get_surface()
        self.index = index
        self.image = image
        self.rect = rect
        

    def draw(self):
        self.display_surface.blit(self.image, self.rect)
        pygame.draw.rect(self.display_surface, 'red', self.rect, 4)


class Preview():
    def __init__(self, index, tiles_map):
        self.tiles_map = tiles_map
        self.display_surface = pygame.display.get_surface()

        colors = ['red', 'blue', 'green', 'yellow']
        self.preview_surface = pygame.Surface((TILE_SIZE*2, TILE_SIZE))
        self.preview_surface.fill(colors[index])
        self.preview_rect = self.preview_surface.get_rect(center=mouse_pos())
        
        self.iso_pos = (0, 0)
        self.size = (2, 1)
        self.pattern = 'ABC'


    def draw_isometric_diamond(self, center):
        x, y = (TILE_SIZE, TILE_SIZE//2)
        points = [
            (x, y - TILE_SIZE // 2),  # Point haut
            (x + TILE_SIZE , y),   # Point droit
            (x, y + TILE_SIZE // 2),  # Point bas
            (x - TILE_SIZE, y)    # Point gauche
        ]
        points = [(x + center[0], y + center[1]) for x, y in points]
        color = 'green' if self.is_valid_position() else 'red'

        pygame.draw.polygon(self.display_surface, color, points)
      
    def get_tile_center(self, origin):
        self.iso_pos = screenToIso(mouse_pos() - origin)
        center_pos = origin + isoToScreen(self.iso_pos)
        return center_pos
            
    def is_valid_position(self):
        return self.iso_pos not in self.tiles_map

    def draw(self, origin):
        # pos = self.get_tile_center(origin)
        # self.draw_isometric_diamond(pos)
        self.draw_cluster(origin)
    
    def draw_cluster(self, origin):
        self.iso_pos = screenToIso(mouse_pos() - origin)
        for i in range(2):
            for j in range(4):
                iso_tile = self.iso_pos[0] + i, self.iso_pos[1] + j 
                pos = origin + isoToScreen(iso_tile)
                self.draw_isometric_diamond(pos)