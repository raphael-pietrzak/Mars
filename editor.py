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
        self.i =0
        # menu
        self.menu = Menu()
        self.resize_active = False
        self.resize_offset = vector()

		# navigation
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector()

        # support lines 
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(30)



    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.resize_screen_event(event)
            self.pan_input(event)
            # self.menu_resize(event)
            self.menu_click(event)
    
    def pan_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0] and not self.menu.rect.collidepoint(mouse_pos()) :
            self.pan_active = True
            self.pan_offset = vector(mouse_pos()) - self.origin
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)

        if event.type == pygame.MOUSEBUTTONUP:
            self.pan_active = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
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
            self.menu.click()



    def update(self):
        self.event_loop()

        self.display_surface.fill('orange')
        self.draw_grid()
        self.menu.display()



