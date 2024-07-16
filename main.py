import pygame
from src.level import Level
from src.settings import *

class Main:
    def __init__(self):
        pygame.init()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("MARS ISOMETRIC GAME")
        self.clock = pygame.time.Clock()

        # screens
        self.level = Level()
        self.main_menu = None

        self.screens = {
            "main_menu": self.main_menu,
            "game": self.level
        }
        self.current_screen = "game"

    def change_screen(self, screen):
        self.current_screen = screen

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            
            screen = self.screens[self.current_screen]
            screen.update(dt)
            
            pygame.display.update()

                




if __name__ == "__main__":
    main = Main()
    main.run()