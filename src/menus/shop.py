import pygame
from pygame import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_pressed

from src.utils import isoToScreen, screenToIso, infiniteToAbs
from src.sprites.buildings import Building
from src.settings import BUILDINGS, ASSETS
import src.settings as settings

class BuildingsBar:
    def __init__(self, tiles_map, buildings_sprites, stock):
        self.display_surface = pygame.display.get_surface()
        self.buildings_sprites = buildings_sprites
        self.tiles_map = tiles_map

        # import 
        self.import_assets()

        # menu
        self.buttons = []
        self.create_menu()

        # preview
        self.preview = None
        self.preview_active = False
        self.active_index = None

        # rect
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect.topleft = (0, 0)

        # stock
        self.stock = stock

    def import_assets(self):
        # Buildings bar
        self.buildings_bar_image = pygame.image.load(ASSETS[4]['path'])
        self.building_image = pygame.image.load(ASSETS[3]['path'])
        mid_bottom = self.display_surface.get_rect().midbottom
        self.buildings_bar_rect = self.buildings_bar_image.get_rect(midbottom=mid_bottom)

    def create_menu(self):
        i = 0
        for key in BUILDINGS:
            mid_left = self.buildings_bar_rect.midleft + vector(i * 130 + 10, 0)
            building_rect = self.building_image.get_rect(midleft=mid_left)
            button = Button(self.building_image, building_rect, key)
            self.buttons.append(button)
            i += 1
    
    def new_build(self):
        cluster = []
        for tile in self.preview.cluster:
            tile = infiniteToAbs(tile)
            self.tiles_map.append(tile)  
            cluster.append(tile)

        Building(self.buildings_sprites, cluster, self.preview.index)     

    # events
    def click_event(self):
        if self.preview_active and mouse_pressed()[0]:
            return
        
        # drag
        for button in self.buttons:
            if button.clickable and button.rect.collidepoint(mouse_pos()) and mouse_pressed()[0]:
                self.active_index = button.index
                self.preview_active = True
                self.preview = Preview(button.index, self.tiles_map)
                break
        
        # drop
        if self.preview_active and not mouse_pressed()[0]:
            cost = self.preview.cost
            self.leaves = self.stock.leaves
            if self.leaves >= cost and self.preview.is_valid_position():
                self.stock.get_leaves(cost)
                self.new_build()
            
            self.active_index = None
            self.preview_active = False
            self.preview = None

    # draw
    def draw_buildings_bar(self):
        self.display_surface.blit(self.buildings_bar_image, self.buildings_bar_rect)
        leaves = self.stock.leaves
        for button in self.buttons:
            button.draw(leaves)

    def draw_preview(self, origin):
        if self.preview:
            self.preview.update(origin)
            self.preview.draw()

    def draw(self, origin):
        self.draw_preview(origin)
        self.draw_buildings_bar()


class Button:
    def __init__(self, image, rect, index):
        self.display_surface = pygame.display.get_surface()
        self.index = index
        self.image = image
        self.rect = rect
        self.cost = BUILDINGS[self.index]['cost']
        self.clickable = False
        
    def draw_cost(self):
        font_path = 'assets/fonts/more-sugar.regular.ttf'
        font = pygame.font.Font(font_path, 20)
        text = font.render(f"{self.cost}", True, 'white')
        offset = vector(33, 38)
        text_rect = text.get_rect(center=self.rect.center + offset)
        self.display_surface.blit(text, text_rect)
    
    def draw_border(self):
        color = 'green' if self.clickable else 'red'
        pygame.draw.rect(self.display_surface, color, self.rect, 4, 5)

    def draw(self, leaves):
        self.display_surface.blit(self.image, self.rect)
        self.draw_cost()
        self.clickable = leaves >= self.cost
        self.draw_border()


class Preview:
    def __init__(self, index, tiles_map):
        self.tiles_map = tiles_map
        self.display_surface = pygame.display.get_surface()
        self.index = index
        self.import_building_info()

        colors = ['red', 'blue', 'green', 'yellow']
        self.preview_surface = pygame.Surface((settings.TILE_SIZE*2, settings.TILE_SIZE))
        self.preview_surface.fill(colors[index])
        self.preview_rect = self.preview_surface.get_rect(center=mouse_pos())
        
        self.iso_pos = (0, 0)

        self.offset_cluster = []
        self.cluster = []
        self.create_offset_cluster()
    
    # setup
    def import_building_info(self):
        self.size = BUILDINGS[self.index]['size']
        self.cost = BUILDINGS[self.index]['cost']

    def create_offset_cluster(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.offset_cluster.append((self.iso_pos[0] + i, self.iso_pos[1] + j))

    def get_tile_center(self, origin):
        self.iso_pos = screenToIso(mouse_pos() - origin)
        center_pos = origin + isoToScreen(self.iso_pos)
        return center_pos
            
    def is_valid_position(self):
        for tile in self.cluster:
            origin_tile = infiniteToAbs(tile)
            if origin_tile in self.tiles_map:
                return False
        return True

    # draw
    def draw_isometric_diamond(self, iso_pos):
        center = self.origin + isoToScreen(iso_pos)

        x, y = center 
        points = [
            (x, y - settings.TILE_SIZE // 2),  # Point haut
            (x + settings.TILE_SIZE , y),   # Point droit
            (x, y + settings.TILE_SIZE // 2),  # Point bas
            (x - settings.TILE_SIZE, y)    # Point gauche
        ]

        color = 'green' if self.is_valid_position() else 'red'

        pygame.draw.polygon(self.display_surface, color, points)
   
    def draw_cluster_test(self):
        for tile in self.cluster:
            self.draw_isometric_diamond(tile)

    def draw(self):
        self.draw_cluster_test()
    
    # update
    def update_cluster(self):
        self.cluster = []
        for tile in self.offset_cluster:
            pos = self.iso_pos + vector(tile)
            final_pos = (int(pos.x), int(pos.y))
            self.cluster.append(final_pos)

    def update(self, origin):
        self.origin = origin
        self.iso_pos = screenToIso(mouse_pos() - self.origin)
        self.update_cluster()