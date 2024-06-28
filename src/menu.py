import pygame
from pygame import Vector2 as vector
from pygame.sprite import Sprite
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_pressed

from src.coordinates import isoToScreen, screenToIso
from src.buildings import Building
import src.settings as settings
from src.settings import *


class Menu:
    def __init__(self, tiles_map, buildings_sprites):
        self.display_surface = pygame.display.get_surface()
        self.rect_group = []
        self.tiles_map = tiles_map
        self.buildings_sprites = buildings_sprites

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
        self.leaves = 400

        # settings
        self.settings = Settings()
        

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
        i = 0
        for key in BUILDINGS:
            mid_left = self.buildings_bar_rect.midleft + vector(i * 130 + 10, 0)
            building_rect = self.building_image.get_rect(midleft=mid_left)
            button = Button(self.building_image, building_rect, key)
            self.buttons.append(button)
            i += 1
    
    def new_build(self):
        for tile in self.preview.cluster:
            self.tiles_map.append(tile)  
        Building(self.buildings_sprites, self.preview.cluster, self.preview.index)     

    def update_rects(self):
        self.buildings_bar_rect.midbottom = self.display_surface.get_rect().midbottom
        self.buttons = []
        self.create_menu()
        self.settings = Settings()

    # events
    def click_event(self):
        self.settings_click_event()

        if self.preview_active and mouse_pressed()[0]:
            return
        
        # drag
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos()) and mouse_pressed()[0]:
                self.active_index = button.index
                self.preview_active = True
                self.preview = Preview(button.index, self.tiles_map)
                break
        
        # drop
        if self.preview_active and not mouse_pressed()[0]:
            cost = self.preview.cost
            if self.leaves >= cost and self.preview.is_valid_position():
                self.leaves -= cost
                self.new_build()
            
            self.active_index = None
            self.preview_active = False
            self.preview = None

    def settings_click_event(self):
        if self.settings_button_rect.collidepoint(mouse_pos()) and mouse_pressed()[0]:
            self.settings.active = True

        self.settings.event_loop()

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
            button.draw(self.leaves)

    def draw_preview(self, origin):
        if self.preview:
            self.preview.update(origin)
            self.preview.draw()

    def draw(self, origin):
        self.draw_preview(origin)
        self.draw_leaf_counter()
        self.draw_settings_button()
        self.draw_buildings_bar()
        self.settings.draw()



class Button:
    def __init__(self, image, rect, index):
        self.display_surface = pygame.display.get_surface()
        self.index = index
        self.image = image
        self.rect = rect
        self.cost = BUILDINGS[self.index]['cost']
        
    def draw_cost(self):
        font_path = 'assets/fonts/more-sugar.regular.ttf'
        font = pygame.font.Font(font_path, 20)
        text = font.render(f"{self.cost}", True, 'white')
        offset = vector(33, 38)
        text_rect = text.get_rect(center=self.rect.center + offset)
        self.display_surface.blit(text, text_rect)

    def draw(self, leaves):
        self.display_surface.blit(self.image, self.rect)
        self.draw_cost()
        color = 'green' if leaves >= self.cost else 'red'
        pygame.draw.rect(self.display_surface, color, self.rect, 4)

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
    
    def import_building_info(self):
        self.size = BUILDINGS[self.index]['size']
        self.cost = BUILDINGS[self.index]['cost']

    def create_offset_cluster(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.offset_cluster.append((self.iso_pos[0] + i, self.iso_pos[1] + j))

    def update_cluster(self):
        self.cluster = []
        for tile in self.offset_cluster:
            pos = self.iso_pos + vector(tile)
            final_pos = (int(pos.x), int(pos.y))
            self.cluster.append(final_pos)

    def draw_isometric_diamond(self, iso_pos):
        center = self.origin + isoToScreen(iso_pos)

        x, y = center + vector(settings.TILE_SIZE , settings.TILE_SIZE//2 )
        points = [
            (x, y - settings.TILE_SIZE // 2),  # Point haut
            (x + settings.TILE_SIZE , y),   # Point droit
            (x, y + settings.TILE_SIZE // 2),  # Point bas
            (x - settings.TILE_SIZE, y)    # Point gauche
        ]

        color = 'green' if self.is_valid_position() else 'red'

        pygame.draw.polygon(self.display_surface, color, points)
      
    def get_tile_center(self, origin):
        self.iso_pos = screenToIso(mouse_pos() - origin)
        center_pos = origin + isoToScreen(self.iso_pos)
        return center_pos
            
    def is_valid_position(self):
        for tile in self.cluster:
            if tile in self.tiles_map:
                return False
        return True

    
    def update(self, origin):
        self.origin = origin
        self.iso_pos = screenToIso(mouse_pos() - self.origin)
        self.update_cluster()

    def draw(self):
        self.draw_cluster_test()
    
    def draw_cluster_test(self):
        for tile in self.cluster:
            self.draw_isometric_diamond(tile)

class Settings:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.import_assets()
        self.create_blur_surface()

        self.on_off_button_sprites = pygame.sprite.Group()
        self.create_params()
        
        self.active = False

    def create_params(self):
        self.params = {
            'music': True,
            'sound': True,
            'mouse': False,
            'keyboard': False,
        }

        i = 0
        for key, value in self.params.items():
            image = self.on_button if value else self.off_button
            rect = image.get_rect(center=(600, 210 + i * 83))
            SettingsButton(self.on_button, self.off_button, rect, self.on_off_button_sprites, value)
            i+=1
    
    def import_assets(self):
        self.surface = pygame.image.load('assets/settings/page.png')
        self.rect = self.surface.get_rect(center=self.display_surface.get_rect().center)

        self.on_button = pygame.image.load('assets/settings/on.png')
        self.off_button = pygame.image.load('assets/settings/off.png')

        self.close_button = pygame.image.load('assets/settings/close.png')
        self.close_button_rect = self.close_button.get_rect(center = self.rect.topright + vector(-50, 50))

    def event_loop(self):
        if self.active:
            self.close_button_event()
            self.on_off_button_event()

    def close_button_event(self):
        if self.close_button_rect.collidepoint(mouse_pos()) and mouse_pressed()[0]:
            self.active = False

    def on_off_button_event(self):
        offset = vector(self.rect.topleft)
        self.on_off_button_sprites.update(offset)

    
    
    def create_blur_surface(self):
        size = self.display_surface.get_size()
        self.blur_surface = pygame.Surface(size)
        self.blur_surface.fill('black')
        self.blur_surface.set_alpha(80)
    
    def draw_on_off(self):
        self.on_off_button_sprites.draw(self.surface)

    def draw(self):
        if self.active:
            self.display_surface.blit(self.blur_surface, (0, 0))
            self.draw_on_off()
            self.display_surface.blit(self.surface, self.rect)
            self.display_surface.blit(self.close_button, self.close_button_rect)


class SettingsButton(Sprite):
    def __init__(self, on_image, off_image, rect, group, active):
        super().__init__(group)
        self.on_image = on_image
        self.off_image = off_image
        self.image = on_image if active else off_image
        self.rect = rect
        self.active = active
    
    def event_loop(self, offset):
        if self.rect.collidepoint(mouse_pos() - offset) and mouse_pressed()[0]:
            self.toggle()

    def toggle(self):
        self.active = not self.active
        self.image = self.on_image if self.active else self.off_image

    def update(self, offset):
        self.event_loop(offset)

    # def draw(self, surface):
    #     surface.blit(self.image, self.rect)
