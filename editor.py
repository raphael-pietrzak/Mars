from collections.abc import Iterable
import sys
import pygame
from settings import *
from pygame import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from menu import Menu



class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # import
        self.import_menu()

        # menu
        self.menu = Menu()
        self.resize_active = False
        self.resize_offset = vector()
        self.selection_index = None

        # preview
        self.preview_active = False
        self.preview_cluster = None    

		# navigation
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector()

        # support lines 
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(30)

        # canvas
        self.canvas = {}


    def import_menu(self):
        self.buildings = MENU_BUILDINGS
        # for key, value in MENU_BUILDINGS.items():
            # self.menu.add_button(key, value)
            

    def event_loop(self):
        self.border_pan()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.resize_screen_event(event)
            self.pan_input(event)
            self.zoom(event)
            
            self.menu_click(event)
            self.menu.event_loop(event)


    def border_pan(self):
        speed = 5
        delta = 20
        if (mouse_pos()[0] < delta):
            self.origin.x += speed
        if (mouse_pos()[0] > WINDOW_WIDTH - delta):
            self.origin.x -= speed
        if (mouse_pos()[1] < 20):
            self.origin.y += speed
        if (mouse_pos()[1] > WINDOW_HEIGHT - delta):
            self.origin.y -= speed

    
    def pan_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0] and not self.menu.rect.collidepoint(mouse_pos())  and not self.preview_active:
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
            
    def menu_resize(self, event):
        deltaX = abs(mouse_pos()[0] - self.menu.rect.right)
        deltaY = abs(mouse_pos()[1] - self.menu.rect.top)
        gap =  5
        if deltaX < gap and deltaY < gap:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
                self.resize_active = True
                self.resize_offset = vector(mouse_pos()) - self.menu.rect.bottomleft


        
        if event.type == pygame.MOUSEBUTTONUP:
            self.resize_active = False


        if self.resize_active:
            self.pan_active = False
            size = vector(
                x = mouse_pos()[0] - self.resize_offset.x,
                y = -mouse_pos()[1] - self.resize_offset.y
            )
            print(size)
            size = (min(max(30, size.x), 300), min(max(30, size.y), 800))
            self.menu.surface2 = pygame.Surface(size)
            self.menu.surface = self.menu.surface2


    def zoom(self, event):
        pass
    
    def resize_screen_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            global WINDOW_WIDTH, WINDOW_HEIGHT
            WINDOW_WIDTH, WINDOW_HEIGHT = self.display_surface.get_size()
            self.support_line_surf = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.support_line_surf.set_colorkey('green')
            self.support_line_surf.set_alpha(60)

    def draw_grid(self):
        self.support_line_surf.fill('green')

        rows = WINDOW_HEIGHT // TILE_SIZE
        cols = WINDOW_WIDTH // TILE_SIZE

        offset = vector(
            x = self.origin.x % TILE_SIZE,
            y = self.origin.y % TILE_SIZE
        )

        for col in range(cols+1):
            x = col * TILE_SIZE  + offset.x
            pygame.draw.line(self.support_line_surf, 'black', (x, 0), (x, WINDOW_HEIGHT))

        for row in range(rows+1):
            y = row * TILE_SIZE  + offset.y
            pygame.draw.line(self.support_line_surf, 'black', (0, y), (WINDOW_WIDTH, y))


        self.display_surface.blit(self.support_line_surf, (0,0))
        


    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu.rect.collidepoint(mouse_pos()):
            self.preview_active = False
            self.selection_index = self.menu.click() 
            if self.selection_index is not None:
                self.preview_active = True
                self.preview_cluster = TileCluster(
                    name = self.buildings[self.selection_index]['name'],
                    cost = self.buildings[self.selection_index]['cost'],
                    income = self.buildings[self.selection_index]['income'],
                    size = self.buildings[self.selection_index]['size'],
                    pos = (0, 0)
                )
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.preview_active and not self.menu.rect.collidepoint(mouse_pos()):

            if self.is_cluster_valid(self.preview_cluster):
                for tile in self.preview_cluster.tiles:
                    canvas_pos = (tile.x + self.preview_cluster.tiles_origin.x, tile.y + self.preview_cluster.tiles_origin.y)
                    self.canvas[canvas_pos] = CanvasTile(tile + self.preview_cluster.tiles_origin)


            self.preview_active = False
            self.preview_cluster = None

        


    def is_cluster_valid(self, cluster):
        for tile in cluster.tiles:
            canvas_pos = (tile.x + cluster.tiles_origin.x, tile.y + cluster.tiles_origin.y)
            if canvas_pos in self.canvas:
                return False
        return True

    def get_tile_pos(self, pos=vector()):
        x = (pos.x - self.origin.x) // TILE_SIZE
        y = (pos.y - self.origin.y) // TILE_SIZE
        return vector(x, y)
    
    def draw_tiles(self):
        for tile in self.canvas.values():
            tile.draw(self.origin)
    
    def draw_menu_preview(self):
        if self.preview_active:
            pos = self.get_tile_pos(mouse_pos() - (self.preview_cluster.size - vector(1, 1))  // 2 * TILE_SIZE)
            self.preview_cluster.tiles_origin = pos
            self.preview_cluster.pos = vector(mouse_pos())
            color = 'green' if self.is_cluster_valid(self.preview_cluster) else 'red'
            self.preview_cluster.draw_preview(self.origin, color)
        
            
    
    def draw_origin(self):
        pygame.draw.circle(self.display_surface, 'red', (int(self.origin.x), int(self.origin.y)), 10)


    def update(self, dt):
        # update
        self.event_loop()

        # drawing
        self.display_surface.fill('orange')
        self.draw_grid()
        self.draw_origin()
        self.draw_tiles()
        self.draw_menu_preview()
        self.menu.update(dt)


class TileCluster:
    def __init__(self, name, cost, income, size, pos):
        self.name = name
        self.cost = cost
        self.income = income
        self.size = vector(size)
        self.tiles_origin = pos
        self.pos = pos
        self.tiles = self.create_tiles()
        self.display_surface = pygame.display.get_surface()
    
    def create_tiles(self):
        tiles = []
        for x in range(int(self.size.x)):
            for y in range(int(self.size.y)):
                tiles.append(vector(x, y))
        return tiles
    
    def draw_preview_warnings(self, origin, color):
        surface = pygame.Surface((self.size.x * TILE_SIZE, self.size.y * TILE_SIZE))
        surface.fill(color)
        surface.set_alpha(150)
        warnings_origin = self.tiles_origin * TILE_SIZE + origin
        rect = surface.get_rect(topleft=warnings_origin)
        self.display_surface.blit(surface, rect)

    
    def draw_preview(self, origin, color):
        self.draw_preview_warnings(origin, color)

        surface = pygame.Surface((self.size.x * TILE_SIZE, self.size.y * TILE_SIZE))
        surface.fill('red')
        rect = surface.get_rect(center = mouse_pos())
        self.display_surface.blit(surface, rect)




        


class CanvasTile:
    def __init__(self, pos, color='blue'):
        self.pos = pos
        self.color = color
        self.surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.surface.fill(self.color)
        self.display_surface = pygame.display.get_surface()

    def draw(self, origin=vector()):
        self.rect = self.surface.get_rect(topleft = self.pos * TILE_SIZE + origin)
        self.display_surface.blit(self.surface, self.rect)                


