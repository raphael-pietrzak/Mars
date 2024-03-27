import pygame
from settings import *
from pygame import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons


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



    def create_menu(self):
        self.layer1 = Layer1((50, 50), (200, 600), MENU)



    
    def event_loop(self, event):

        if self.layer1.rect.collidepoint(mouse_pos()):
            self.layer1.event_loop(event)
            # # if self.buttons_container_rect.top + event.y * 10 <= 0 and self.buttons_container_rect.bottom + event.y * 10 >= self.size[1]:
            # self.buttons_container_rect.y += event.y * 10 
            # self.buttons_container_rect.bottom = max(self.size[1], self.buttons_container_rect.bottom)  
            # self.buttons_container_rect.top = min(0, self.buttons_container_rect.top)


                
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

        self.layer1.display(dt)

        # self.ressource.draw()


class MenuLayer:
    def __init__(self, pos, size):
        self.display_surface = pygame.display.get_surface()

        # layer
        self.rect = pygame.Rect(pos, size)
        self.surface = pygame.Surface(self.rect.size)
        self.surface.set_colorkey('green')


    def display(self):
        pygame.draw.rect(self.display_surface, 'aquamarine3', self.rect, border_radius=10)
        self.display_surface.blit(self.surface, self.rect)


class Layer1(MenuLayer):
    def __init__(self, pos, size, items_dict):
        super().__init__(pos, size)
        self.buttons = []
        self.items_dict = items_dict
        self.titles = [value['name'] for value in self.items_dict.values()]

        self.create_buttons()
        self.create_layers()
        self.button_selected = 0


    def event_loop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
            self.click()
            
        

    def click(self):
        for button in self.buttons:
            offset = vector(self.rect.topleft) + vector(self.buttons_container_rect.topleft)
            if button.rect.collidepoint(mouse_pos() - offset):
                button.animation_active = True
                self.button_selected = button.index
                return button.index
        return None
    
    def create_buttons(self):
        button_size = vector(50, 50)
        padding = vector(0, 5)
        margin = vector(10, 10)
        for i in range(len(self.titles)):
            topleft = (margin.x, margin.y + (button_size.y + padding.y) * i)
            center = (topleft[0] + button_size.x//2, topleft[1] + button_size.y//2)
            button = Button(center, button_size, self.titles[i], i)
            self.buttons.append(button)

        self.buttons_container = pygame.Surface((self.rect.width, len(self.buttons) * (button_size.y + padding.y) + margin.y * 2))
        self.buttons_container_rect = self.buttons_container.get_rect(topleft=(0, 0))

    def create_layers(self):
        self.layers = []

        print(self.items_dict[0]['items'])
        for i in range(len(self.titles)):
            layer = Layer2(self.rect.topright + vector(20, 0), (200, 600), self.items_dict[i]['items'])
            self.layers.append(layer)                       

    def display_buttons(self, dt):
        self.buttons_container.fill('red')
        for button in self.buttons:
            button.update(dt, self.buttons_container)


    def display(self, dt):
        self.surface.fill('green')
        self.display_buttons(dt)
        self.surface.blit(self.buttons_container, self.buttons_container_rect)

        self.layers[self.button_selected].display(dt)

        super().display()


class Layer2(MenuLayer):
    def __init__(self, pos, size, items_dict):
        super().__init__(pos, size)
        self.buttons = []
        self.items_dict = items_dict
        self.items = [value['name'] for value in self.items_dict.values()]
        self.create_buttons()
        self.create_layers()
        self.button_selected = 0
    
    def create_buttons(self):
        button_size = vector(50, 50)
        padding = vector(0, 5)
        margin = vector(10, 10)
        for i in range(len(self.items)):
            topleft = (margin.x, margin.y + (button_size.y + padding.y) * i)
            center = (topleft[0] + button_size.x//2, topleft[1] + button_size.y//2)
            button = Button(center, button_size, self.items[i], i)
            self.buttons.append(button)

        self.buttons_container = pygame.Surface((self.rect.width, len(self.buttons) * (button_size.y + padding.y) + margin.y * 2))
        self.buttons_container_rect = self.buttons_container.get_rect(topleft=(0, 0))

    def create_layers(self):
        self.layers = []
        for i in range(len(self.items)):
            layer = Layer3(self.rect.topright + vector(20, 0), (200, 200), self.items_dict[i])
            self.layers.append(layer)

        
    def buttons_hover(self):
        for button in self.buttons:
            offset = vector(self.rect.topleft) + vector(self.buttons_container_rect.topleft)
            if button.rect.collidepoint(mouse_pos() - offset):
                self.button_selected = button.index
                button.animation_active = True
                break


    def display_buttons(self, dt):
        self.buttons_container.fill('red')
        for button in self.buttons:
            button.update(dt, self.buttons_container)


    def display(self, dt):

        self.buttons_hover()

        self.surface.fill('green')
        self.display_buttons(dt)
        self.surface.blit(self.buttons_container, self.buttons_container_rect)

        self.layers[self.button_selected].display()

        super().display()


class Layer3(MenuLayer):
    def __init__(self, pos, size, items_dict):
        super().__init__(pos, size)
        self.title = 'Description'
        self.cost = items_dict['cost']
        self.items_dict = items_dict
        self.visible = False

    def display(self):
        self.surface.fill('green')
        text = pygame.font.Font(None, 26).render(str(self.cost), True, 'white')
        text_rect = text.get_rect(center=vector(self.rect.width//2, self.rect.height//2))
        self.surface.blit(text, text_rect)
        super().display()




    
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
        pygame.draw.rect(surface, 'burlywood1', self.rect, border_radius=10)
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