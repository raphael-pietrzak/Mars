import sys
from src.coordinates import isoToScreen
import pygame
from pygame import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos

from src.menu import Menu
from src.buildings import Building
from src.settings import *
from src.stock import Stock


class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.tiles_map = []
        self.buildings_sprites = pygame.sprite.Group()

        # menu
        self.menu = Menu(self.tiles_map, self.buildings_sprites)
        self.selection_index = None

		# navigation
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector()

        # support lines 
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(30)



    # events
    def event_loop(self):
        self.border_pan()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)
            self.menu.click_event()

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

    # draw
    def draw_isometric_diamond(self, center):
        x, y = (TILE_SIZE, TILE_SIZE//2)
        points = [
            (x, y - TILE_SIZE // 2),  # Point haut
            (x + TILE_SIZE , y),   # Point droit
            (x, y + TILE_SIZE // 2),  # Point bas
            (x - TILE_SIZE, y)    # Point gauche
        ]
        points = [(x + center[0], y + center[1]) for x, y in points]
        color = 'white'
        pygame.draw.polygon(self.display_surface, color, points, 4)

    def draw_grid(self):
        self.display_surface.fill('orange')
        self.draw_origin()
        self.support_line_surf.fill('green')  # Clear the support line surface with transparency

        tile_width = TILE_SIZE * 4
        tile_height = TILE_SIZE   # Height of an isometric tile is half its width

        rows = WINDOW_HEIGHT // tile_height
        cols = WINDOW_WIDTH // tile_width

        offset_x = self.origin.x % tile_width
        offset_y = self.origin.y % tile_height

        for col in range(-2, cols + 2):
            for row in range(-2, rows + 2):
                x = col * tile_width + offset_x
                y = row * tile_height + offset_y

                # Draw lines for isometric grid
                pygame.draw.line(self.support_line_surf, 'black', (x, y), (x - tile_width // 2, y + tile_height))
                pygame.draw.line(self.support_line_surf, 'black', (x, y), (x + tile_width // 2, y + tile_height))
                pygame.draw.line(self.support_line_surf, 'black', (x - tile_width // 2, y + tile_height), (x, y + 2 * tile_height))
                pygame.draw.line(self.support_line_surf, 'black', (x + tile_width // 2, y + tile_height), (x, y + 2 * tile_height))

                # Draw vertical lines
                for i in range(1, 5):
                    pygame.draw.line(self.support_line_surf, 'red', (x - TILE_SIZE * i, y), (x - TILE_SIZE * i, WINDOW_HEIGHT))

        self.display_surface.blit(self.support_line_surf, (0, 0))
 
    def draw_tiles(self):
        for tile in self.tiles_map:
            pos = self.origin + vector(self.isoToScreen(tile[0], tile[1])) - vector(0, TILE_SIZE//2)
            self.draw_isometric_diamond(pos)

    def draw_origin(self):
        pygame.draw.circle(self.display_surface, 'red', (int(self.origin.x), int(self.origin.y)), 10)

    def update(self, dt):
        # update
        self.event_loop()
        self.update_stock()


        # drawing
        self.draw_grid()
        # self.draw_tiles()
        self.buildings_sprites.update(self.origin, dt)
        self.menu.draw(self.origin)





