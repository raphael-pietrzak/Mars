import sys
import pygame


class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.event_loop()
        
        self.display_surface.fill('green')



