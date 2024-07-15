import pygame, sys
from pygame import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from pygame.key import get_pressed as keys

import src.settings as settings
from .settings import TILE_SIZE
from .overlay.buildings_bar import BuildingsBar
from .overlay.settings import Settings
from .overlay.stock import Stock

from .settings import *
from .utils import rotate_90_clockwise, isoToScreen, screenToIso
from .camera import Camera
from .gui.button import Component

class Level:
    def __init__(self):
        # display
        self.display_surface = pygame.display.get_surface()

        # screen test
        self.screen_test_rect = pygame.Rect(0, 0, 20*TILE_SIZE, 10*TILE_SIZE)
        self.test_active = False

        # map
        self.tiles_map = []
        self.buildings_sprites = Camera()

        # menu
        self.buildings_bar_menu = BuildingsBar(self.tiles_map, self.buildings_sprites)
        self.settings_menu = Settings()
        self.stock_menu = Stock()

		# navigation
        self.origin = vector(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        self.pan_active = False
        self.pan_offset = vector()
        self.level_active = True

        # grid
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(30)

        # test
        self.settings_button_image = pygame.image.load(ASSETS[1]['path'])
        self.button_test = Component(self.settings_button_image, (300, 300))


    # events
    def event_loop(self):
        self.border_pan()
        self.infinite_map()

        for event in pygame.event.get():

            self.button_test.event_handler(event)
            
            if self.level_active:
                self.menus_events(event)
                self.zoom(event)
                self.pan_input(event)
                self.activate_test(event)
                self.key_input(event)
                
            self.resize_window(event)
            self.close(event)
    
    def menus_events(self, event):
        if not self.pan_active:
            self.buildings_bar_menu.click_event()

    def border_pan(self):
        if self.buildings_bar_menu.preview_active:
            speed = 5
            delta = 10
            if (mouse_pos()[0] < delta):
                self.origin.x += speed
            if (mouse_pos()[0] > WINDOW_WIDTH - delta):
                self.origin.x -= speed
            if (mouse_pos()[1] < 20):
                self.origin.y += speed
            if (mouse_pos()[1] > WINDOW_HEIGHT - delta):
                self.origin.y -= speed
    
    def pan_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0] and not self.is_menu_collided(event):
            self.pan_active = True
            self.pan_offset = vector(mouse_pos()) - self.origin
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        if event.type == pygame.MOUSEBUTTONUP:
            self.pan_active = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        if event.type == pygame.MOUSEWHEEL and not self.zoom_active:
            self.origin += vector(- event.x * 10, event.y * 10)

        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset
    
    def is_menu_collided(self, event):
        return self.buildings_bar_menu.buildings_bar_rect.collidepoint(mouse_pos())
 
    def update_stock(self):
        for building in self.buildings_sprites:
            self.buildings_bar_menu.leaves += building.get_leaves()

    def key_input(self, event):
        if event.type == pygame.KEYDOWN:
            if keys()[pygame.K_RIGHT]:
                self.rotate()
            if keys()[pygame.K_t]:
                self.test_active = not self.test_active 

    def rotate(self):
        for building in self.buildings_sprites:
            cluster = []
            for pos in building.cluster:
                new_axis_pos = vector(pos) -  vector(MAP_SIZE//2, MAP_SIZE//2)
                rotated_pos = rotate_90_clockwise(new_axis_pos)
                origin_pos = rotated_pos + vector(MAP_SIZE//2, MAP_SIZE//2)
                cluster.append(origin_pos)

            building.cluster = cluster
            building.barycenter = building.get_barycenter()
        
        self.tiles_map = [rotate_90_clockwise(pos) for pos in self.tiles_map]
        self.buildings_bar_menu.tiles_map = self.tiles_map

    def infinite_map(self):
        screen_center = vector(WINDOW_WIDTH//2, WINDOW_HEIGHT//2) 
        offset = isoToScreen((MAP_SIZE//2, MAP_SIZE//2))
        x, y = screenToIso(screen_center - self.origin - offset) 
        if x < 0:
            self.origin -= isoToScreen((MAP_SIZE, 0))
        if x >= MAP_SIZE:
            self.origin += isoToScreen((MAP_SIZE, 0))
        if y < 0:
            self.origin -= isoToScreen((0, MAP_SIZE))
        if y >= MAP_SIZE:
            self.origin += isoToScreen((0, MAP_SIZE))

    def activate_test(self, event):
        if event.type == pygame.KEYDOWN:
            if keys()[pygame.K_t]:
                self.test_active = not self.test_active
            

    # resize
    def resize_window(self, event):
        if event.type == pygame.VIDEORESIZE:
            global WINDOW_WIDTH, WINDOW_HEIGHT
            WINDOW_WIDTH = event.w
            WINDOW_HEIGHT = event.h
            self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.support_line_surf.set_colorkey('green')
            self.support_line_surf.set_alpha(30)

            self.buildings_bar_menu.update_rects()

    def zoom(self, event):
        self.zoom_active = False
        self.zoom_speed = 5
        if event.type == pygame.MOUSEWHEEL and keys()[pygame.K_LMETA]:
            self.zoom_active = True

            self.distance_to_origin = vector(WINDOW_WIDTH//2, WINDOW_HEIGHT//2) - self.origin

            tile_size_before = settings.TILE_SIZE

            if event.y > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            
            tile_size_after = settings.TILE_SIZE
            factor = tile_size_after / tile_size_before

            offset = (1 - factor) * self.distance_to_origin
            self.origin += offset

    def zoom_in(self):
        settings.TILE_SIZE += self.zoom_speed
        settings.TILE_SIZE = min(settings.ZOOM_MAX, settings.TILE_SIZE)

    def zoom_out(self):
        settings.TILE_SIZE -= self.zoom_speed
        settings.TILE_SIZE = max(settings.ZOOM_MIN, settings.TILE_SIZE)

    def close(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # draw
    def draw_grid(self):
        self.display_surface.fill('orange')
        self.draw_origin()
        self.support_line_surf.fill('green')  # Clear the support line surface with transparency

        tile_width = settings.TILE_SIZE * 2
        tile_height = settings.TILE_SIZE   # Height of an isometric tile is half its width

        rows = WINDOW_HEIGHT // tile_height
        cols = WINDOW_WIDTH // tile_width


        offset_x = self.origin.x % tile_width
        offset_y = self.origin.y % tile_height

        for col in range(-2, cols + 2):
            for row in range(-2, rows + 2):
                x = col * tile_width + offset_x + settings.TILE_SIZE
                y = row * tile_height + offset_y

                # Draw lines for isometric grid
                pygame.draw.line(self.support_line_surf, 'black', (x, y), (x - tile_width , y + tile_height))
                pygame.draw.line(self.support_line_surf, 'black', (x, y), (x + tile_width, y + tile_height))

                # Draw vertical lines
                # for i in range(1, 5):
                #     pygame.draw.line(self.support_line_surf, 'white', (x - settings.TILE_SIZE * i, y), (x - settings.TILE_SIZE * i, WINDOW_HEIGHT))

        self.display_surface.blit(self.support_line_surf, (0, 0))
        # pygame.draw.circle(self.display_surface, 'red', self.target_1, 10)
 
    def draw_origin(self):
        pygame.draw.circle(self.display_surface, 'red', self.origin, 10)

    def draw_buildings(self):
        self.buildings_sprites.draw_4_times()

    def draw_menu(self):
        self.buildings_bar_menu.draw(self.origin)
        self.settings_menu.draw()
        self.stock_menu.draw()

    def draw_screen_test(self):
        self.screen_test_rect = pygame.Rect(0, 0, 20*settings.TILE_SIZE, 10*settings.TILE_SIZE)
        self.screen_test_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        pygame.draw.rect(self.display_surface, 'red', self.screen_test_rect, 2)

    def draw_diamond_test(self, iso_left, color):
        left = self.origin - vector(settings.TILE_SIZE, 0) + isoToScreen(iso_left)
        points = [
            left + isoToScreen((0, MAP_SIZE)),          # Point haut
            left,                                       # Point droit
            left + isoToScreen((MAP_SIZE, 0)),          # Point bas
            left + isoToScreen((MAP_SIZE, MAP_SIZE))    # Point gauche
        ]

        pygame.draw.polygon(self.display_surface, color, points, 2)
            
    def draw_screen_center(self):
        pygame.draw.circle(self.display_surface, 'blue', (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), 10)

    def draw_tests(self):
        if self.test_active:
            self.draw_diamond_test((0, 0), 'red')
            self.draw_diamond_test((MAP_SIZE//2, MAP_SIZE//2), 'blue')
            self.draw_screen_center()
            self.draw_screen_test()


    # update
    def update_sprites(self, dt):
        self.buildings_sprites.update(self.origin, dt)

    def update(self, dt):
        # update
        self.event_loop()
        self.update_stock()
        self.update_sprites(dt)
        self.button_test.update(dt)

        # drawing
        self.draw_grid()
        self.draw_buildings()
        self.draw_tests()
        self.draw_menu()
        self.button_test.draw(self.display_surface)





