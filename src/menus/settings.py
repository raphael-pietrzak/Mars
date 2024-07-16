
import pygame
from pygame import Vector2 as vector
from pygame.sprite import Sprite
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_pressed

from src.settings import ASSETS


class Settings:
    def __init__(self):
        # display
        self.display_surface = pygame.display.get_surface()
        self.active = False

        # setup
        self.import_assets()
        self.create_blur_surface()

        # buttons
        self.toggle_options_group = pygame.sprite.Group()
        self.create_toggles()

        self.settings_button_image = pygame.image.load(ASSETS[1]['path'])
        self.settings_button_rect = self.settings_button_image.get_rect(topleft=(400, 0))

        # self.activation_button 
        
    # setup
    def import_assets(self):
        self.surface = pygame.image.load('assets/settings/page.png')
        self.rect = self.surface.get_rect(center=self.display_surface.get_rect().center)

        self.on_button = pygame.image.load('assets/settings/on.png')
        self.off_button = pygame.image.load('assets/settings/off.png')

        self.close_button = pygame.image.load('assets/settings/close.png')
        self.close_button_rect = self.close_button.get_rect(center = self.rect.topright + vector(-50, 50))
  
    def create_toggles(self):
        self.options = {
            'music': True,
            'sound': True,
            'mouse': False,
            'keyboard': False,
        }

        i = 0
        for key, value in self.options.items():
            image = self.on_button if value else self.off_button
            rect = image.get_rect(center=(600, 210 + i * 83))
            Toggle(self.on_button, self.off_button, rect, self.toggle_options_group, value)
            i+=1
  
    def create_blur_surface(self):
        size = self.display_surface.get_size()
        self.blur_surface = pygame.Surface(size)
        self.blur_surface.fill('black')
        self.blur_surface.set_alpha(80)
    
    # events
    def event_loop(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN:
            self.close_button_event()
            self.on_off_button_event()

    def close_button_event(self):
        if self.close_button_rect.collidepoint(mouse_pos()) and mouse_pressed()[0]:
            self.active = False

    def on_off_button_event(self):
        offset = vector(self.rect.topleft)
        self.toggle_options_group.update(offset)

    # draw
    def draw_settings_button(self):
        self.display_surface.blit(self.settings_button_image, (400, 0))

    def draw_on_off(self):
        self.toggle_options_group.draw(self.surface)

    def draw(self):
        self.draw_settings_button()
        if self.active:
            self.display_surface.blit(self.blur_surface, (0, 0))
            self.draw_on_off()
            self.display_surface.blit(self.surface, self.rect)
            self.display_surface.blit(self.close_button, self.close_button_rect)


class Toggle(Sprite):
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
