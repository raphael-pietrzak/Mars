from blob import Editor
from settings import *

import pygame

class Main:
    def __init__(self):
        pygame.init()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("BLOB TEST")

        self.editor = Editor()
        self.clock = pygame.time.Clock()
        

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.editor.update(dt)
            pygame.display.update()



if __name__ == "__main__":
    main = Main()
    main.run()