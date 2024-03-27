import pygame
from settings import *
from pygame import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_pressed


class Menu:
    def __init__(self):
        # MENU LAYER 1
            # [Buildings, Units, Resources]
        # MENU LAYER 2
            # [House, Farm, Factory, Bank]
            # [Soldier, Archer, Knight, Mage]
            # [Wood, Stone, Iron, Gold]
        # MENU LAYER 3
            # [House : 100, 10, (2, 2)]
            # [Farm : 200, 20, (2, 3)]
            # ...
        
        self.display_surface = pygame.display.get_surface()
        self.menu_items = MENU
        self.create_menu()
        self.is_dragging = False
        self.ressource = Ressources('Wood', 100, (50, 50))
        self.rect = pygame.Rect((0, 0), (200, 50))



    def create_menu(self, cols=1, rows=10):

        first_layer_rect = pygame.Rect((0, 0), (50, 500))
        first_layer_rect.center = (50, WINDOW_HEIGHT//2)

        second_layer_rect = pygame.Rect((0, 0), (300, 500))
        second_layer_rect.topleft = (first_layer_rect.right + 20, first_layer_rect.top)

        third_layer_rect = pygame.Rect((0, 0), (200, 200))
        third_layer_rect.topleft = (second_layer_rect.right + 20, first_layer_rect.top)

        self.menu_layers = []

        layer1_items = [value['name'] for key, value in self.menu_items.items()]
        self.layer1 = MenuLayer('Catégories', first_layer_rect, layer1_items)

        layer2_items = [value['name'] for key, value in self.menu_items[0]['items'].items()]
        self.layer2 = MenuLayer('Bâtiments', second_layer_rect, layer2_items)

        layer3_items = [f"{value['name']} : {value['cost']}, {value['income']}, {value['size']}" for key, value in self.menu_items[0]['items'].items()]
        self.layer3 = MenuLayer('Description', third_layer_rect, layer3_items)






        # button_size = vector(50, 50)
        # padding = vector(0, 5)
        # margin = vector(10, 10)
        # self.size = (button_size.x + margin.x * 2, button_size.y * rows + padding.y * (rows - 1) + margin.y * 2)
        # self.rect = pygame.Rect((0,0), self.size)
        # self.rect.center = (50, WINDOW_HEIGHT//2)
        # self.surface = pygame.Surface(self.size)
        # self.surface.set_colorkey('green')

        # self.buttons = []
        # titles = ['4', '6', '9', '12']
        # for i in range(len(titles)):
        #     topleft = (margin.x, margin.y + (button_size.y + padding.y) * i)
        #     center = (topleft[0] + button_size.x//2, topleft[1] + button_size.y//2)
        #     button = Button(center, button_size, titles[i], i)
        #     self.buttons.append(button)

        # self.buttons_container = pygame.Surface((self.size[0], len(self.buttons) * (button_size.y + padding.y) + margin.y * 2))
        # self.buttons_container_rect = self.buttons_container.get_rect(topleft=(0, 0))
        # self.buttons_container.set_colorkey('red')



    
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

        self.layer1.display()
        self.layer2.display()
        self.layer3.display()

        # pygame.draw.rect(self.display_surface, 'gray', self.rect, border_radius=10)
        # self.buttons_container.fill('red')
        # for button in self.buttons:
        #     button.update(dt, self.buttons_container)

        # self.surface.fill('green')
        # self.surface.blit(self.buttons_container, self.buttons_container_rect)
        # self.display_surface.blit(self.surface, self.rect)

        self.ressource.draw()


class MenuLayer:
    def __init__(self, title, rect, items):
        self.title = title
        self.rect = rect
        self.items = items
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface(self.rect.size)
        self.create_buttons()
        self.font = pygame.font.Font(None, 26)
        self.surface.set_colorkey('red')
    
    def create_buttons(self):
        self.buttons = []
        for i in range(len(self.items)):
            button = Button((self.rect.centerx, self.rect.y + 50 * i), (200, 50), self.items[i], i)
            self.buttons.append(button)
    
    def display_buttons(self):
        self.surface.fill('red')    
        for button in self.buttons:
            button.display(self.surface)

    
    def display(self):
        pygame.draw.rect(self.display_surface, 'blue', self.rect, border_radius=10)
        text = self.font.render(self.title, True, 'white')
        text_rect = text.get_rect(center=self.rect.center)
        self.display_surface.blit(text, text_rect)
        self.display_buttons()
        self.display_surface.blit(self.surface, self.rect)


class Description:
    def __init__(self, title, cost, income, size):
        self.title = title
        self.cost = cost
        self.income = income
        self.size = size
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 26)
        self.rect = pygame.Rect((0, 0), (200, 200))
        self.rect.topleft = (WINDOW_WIDTH - 200, 0)
    
    def display(self):
        pygame.draw.rect(self.display_surface, 'blue', self.rect, border_radius=10)
        text = self.font.render(f'{self.title}', True, 'white')
        text_rect = text.get_rect(center=self.rect.center)
        self.display_surface.blit(text, text_rect)


    
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
        pygame.draw.rect(surface, 'green', self.rect, border_radius=10)
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



class Ressources:
    def __init__(self, title, amount, pos):
        self.display_surface = pygame.display.get_surface()
        self.title = title
        self.amount = amount
        self.pos = pos
        self.font = pygame.font.Font(None, 26)
        self.rect = pygame.Rect(self.pos, (200, 50))



    def draw(self):
        pygame.draw.rect(self.display_surface, 'blue', self.rect, border_radius=10)
        text = self.font.render(f'{self.title}: {self.amount}', True, 'white')
        text_rect = text.get_rect(center=self.rect.center)
        self.display_surface.blit(text, text_rect)