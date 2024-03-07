import pygame
from settings import *
from pygame import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_pressed


class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_menu()
        self.is_dragging = False

    def create_menu(self, cols=1, rows=10):
        button_size = vector(50, 50)
        padding = vector(0, 5)
        margin = vector(10, 10)
        self.size = (button_size.x + margin.x * 2, button_size.y * rows + padding.y * (rows - 1) + margin.y * 2)
        self.rect = pygame.Rect((0,0), self.size)
        self.rect.center = (50, WINDOW_HEIGHT//2)
        self.surface = pygame.Surface(self.size)
        self.surface.set_colorkey('green')

        self.buttons = []
        for i in range(4):
            topleft = (margin.x, margin.y + (button_size.y + padding.y) * i)
            center = (topleft[0] + button_size.x//2, topleft[1] + button_size.y//2)
            button = Button(center, button_size, f'{i}', i)
            self.buttons.append(button)

        self.buttons_container = pygame.Surface((self.size[0], len(self.buttons) * (button_size.y + padding.y) + margin.y * 2))
        self.buttons_container_rect = self.buttons_container.get_rect(topleft=(0, 0))
        self.buttons_container.set_colorkey('red')



    
    def event_loop(self, event):
        if event.type == pygame.MOUSEWHEEL:
            # if self.buttons_container_rect.top + event.y * 10 <= 0 and self.buttons_container_rect.bottom + event.y * 10 >= self.size[1]:
            self.buttons_container_rect.y += event.y * 10 
            self.buttons_container_rect.bottom = max(self.size[1], self.buttons_container_rect.bottom)  
            self.buttons_container_rect.top = min(0, self.buttons_container_rect.top)
                
    def click(self):
        for button in self.buttons: 
            offset = vector(self.rect.topleft) + vector(self.buttons_container_rect.topleft)
            if button.rect.collidepoint(mouse_pos() - offset):
                button.animation_active = True
                # self.is_dragging = True
                return button.index
        return None


    def draw_preview(self):
        if self.is_dragging:
            preview_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            preview_surface.fill('red')
            preview_rect = preview_surface.get_rect(center=mouse_pos())
            self.display_surface.blit(preview_surface, preview_rect)  
        


    def update(self, dt):
        self.draw_preview()

        pygame.draw.rect(self.display_surface, 'gray', self.rect, border_radius=10)
        self.buttons_container.fill('red')
        for button in self.buttons:
            button.update(dt, self.buttons_container)

        self.surface.fill('green')
        self.surface.blit(self.buttons_container, self.buttons_container_rect)
        self.display_surface.blit(self.surface, self.rect)





    
class Button:
    def __init__(self, center, size, text, index):
        self.index = index
        self.size = vector(size)
        self.center = center
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = center
        self.text = text
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 26)

        # Animation
        self.animation_speed = 200
        self.animation_active = False
        self.down_animation = [40]
        self.up_animation = [55, 50]
        self.animation = [40, 55, 50]
        self.animation_index = 0

    def display(self, surface):
        pygame.draw.rect(surface, 'blue', self.rect, border_radius=10)
        text = self.font.render(self.text, True, 'white')
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
    
    def animate(self, dt):
        if self.animation_index >= len(self.animation):
            self.animation_index = 0
            self.animation_active = False


        if self.animation_active:
            size_goal = self.animation[self.animation_index]
            direction = 1 if self.size.x - size_goal < 0 else -1
            self.size += vector(1, 1) * dt * self.animation_speed * direction
            self.rect.size = self.size
            self.rect.center = self.center
            
            if (direction == 1 and self.size.x > size_goal) or (direction == -1 and self.size.x < size_goal):
                self.size = vector(size_goal, size_goal)
                self.rect.size = self.size
                self.animation_index += 1
            
                
    
    def update(self, dt, surface):
        self.animate(dt)
        self.display(surface)


