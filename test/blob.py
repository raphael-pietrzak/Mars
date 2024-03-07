from sets import *
import sys
import pygame


class Editor:
    def __init__(self):
        self.display_surface =  pygame.display.get_surface()

        # blob
        self.blob_surface = pygame.Surface((200, 200))
        self.blob_rect = self.blob_surface.get_rect()
        self.blob_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        # animation
        self.time = 0
        self.duration = 30000


    def event_loop(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            # if event.type == pygame.MOUSEBUTTONDOWN:
            self.animate(dt)


    def animate(self, dt):
        self.time +=  dt * ANIMATION_SPEED
        if self.time > self.duration:
            self.time %= self.duration
        self.blob_rect.centerx = WINDOW_WIDTH//2 + self.time



    def update(self, dt):
        self.event_loop(dt)
        self.display_surface.fill('aquamarine')
        self.display_surface.blit(self.blob_surface, self.blob_rect)

class Blob:
    def __init__(self, parent, width=10, height=10, locked=False):
        self.width = width
        self.height = height
        self.locked = locked
        self.parent = parent



