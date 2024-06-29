import pygame, sys
from pygame import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from pygame.key import get_pressed as keys

import src.settings as settings
from src.menu import Menu
from src.settings import *
from src.coordinates import rotate_90_clockwise, isoToScreen, screenToIso
from src.camera import Camera


class Level:
    def __init__(self):
        # display
        self.display_surface = pygame.display.get_surface()

        # screen test
        self.screen_test_rect = pygame.Rect(0, 0, 20*settings.TILE_SIZE, 10*settings.TILE_SIZE)

        # map
        self.tiles_map = []
        self.buildings_sprites = Camera()

        # menu
        self.menu = Menu(self.tiles_map, self.buildings_sprites)

		# navigation
        self.origin = vector(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        self.pan_active = False
        self.pan_offset = vector()

        # grid
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(30)


    # events
    def event_loop(self):
        self.border_pan()
        self.infinite_map()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)
            self.resize_window(event)
            self.menu.click_event()
            self.zoom(event)
            self.key_input(event)

    def border_pan(self):
        if self.menu.preview_active:
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
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0] and not self.menu.collidepoint(mouse_pos()):
            self.pan_active = True
            self.pan_offset = vector(mouse_pos()) - self.origin
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)

        if event.type == pygame.MOUSEBUTTONUP:
            self.pan_active = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        if event.type == pygame.MOUSEWHEEL:
            self.origin += vector(- event.x * 10, event.y * 10)

        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset
 
    def update_stock(self):
        for building in self.buildings_sprites:
            self.menu.leaves += building.get_leaves()

    def key_input(self, event):
        if event.type == pygame.KEYDOWN:
            if keys()[pygame.K_RIGHT]:
                self.rotate()

    def rotate(self):
        for building in self.buildings_sprites:
            building.cluster = [rotate_90_clockwise(pos) for pos in building.cluster]
            building.barycenter = building.get_barycenter()
        
        self.tiles_map = [rotate_90_clockwise(pos) for pos in self.tiles_map]
        self.menu.tiles_map = self.tiles_map

    def infinite_map(self):
        x, y = MAP_SIZE, MAP_SIZE
        if self.origin.x < self.screen_test_rect.left:
            self.origin += isoToScreen((x, y))
        if self.origin.x > self.screen_test_rect.right:
            self.origin -= isoToScreen((x, y))
        if self.origin.y < self.screen_test_rect.top:
            self.origin += isoToScreen((x, -y))
        if self.origin.y > self.screen_test_rect.bottom:
            self.origin -= isoToScreen((x, -y))

    # resize
    def resize_window(self, event):
        if event.type == pygame.VIDEORESIZE:
            global WINDOW_WIDTH, WINDOW_HEIGHT
            WINDOW_WIDTH = event.w
            WINDOW_HEIGHT = event.h
            self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.support_line_surf.set_colorkey('green')
            self.support_line_surf.set_alpha(30)

            self.menu.update_rects()

    def zoom(self, event):
        
        if event.type == pygame.MOUSEWHEEL and keys()[pygame.K_LMETA]:
            if event.y > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        
    def zoom_in(self):
        settings.TILE_SIZE += 10
        settings.TILE_SIZE = min(settings.ZOOM_MAX, settings.TILE_SIZE)
    
    def zoom_out(self):
        settings.TILE_SIZE -= 10
        settings.TILE_SIZE = max(settings.ZOOM_MIN, settings.TILE_SIZE)


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

                # # Draw vertical lines
                # for i in range(1, 5):
                #     pygame.draw.line(self.support_line_surf, 'white', (x - settings.TILE_SIZE * i, y), (x - settings.TILE_SIZE * i, WINDOW_HEIGHT))

        self.display_surface.blit(self.support_line_surf, (0, 0))
 
    def draw_origin(self):
        pygame.draw.circle(self.display_surface, 'red', self.origin, 10)

    def draw_buildings(self):
        self.buildings_sprites.draw_4_times()

    def draw_menu(self):
        self.menu.draw(self.origin)

    def draw_screen_test(self):
        self.screen_test_rect = pygame.Rect(0, 0, 20*settings.TILE_SIZE, 10*settings.TILE_SIZE)
        self.screen_test_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        pygame.draw.rect(self.display_surface, 'red', self.screen_test_rect, 2)

    def draw_diamond_test(self):
        left = self.origin - vector(settings.TILE_SIZE, 0)
        points = [
            left + isoToScreen((0, MAP_SIZE)),    # Point haut
            left,                    # Point droit
            left + isoToScreen((MAP_SIZE, 0)),    # Point bas
            left + isoToScreen((MAP_SIZE, MAP_SIZE))    # Point gauche
        ]
        pygame.draw.polygon(self.display_surface, 'red', points, 2)
            
    # update
    def update_sprites(self, dt):
        self.buildings_sprites.update(self.origin, dt)

    def update(self, dt):
        # update
        self.event_loop()
        self.update_stock()
        self.update_sprites(dt)

        # drawing
        self.draw_grid()
        self.draw_buildings()
        self.draw_diamond_test()
        self.draw_screen_test()
        self.draw_menu()





