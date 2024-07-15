
import pygame
from pygame.math import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos

class Component:
    def __init__(self, image, center):
        self.display_surface = pygame.display.get_surface()
        self.init_image = image.copy()
        self.image = image
        self.rect = image.get_rect(center=center)
        self.initial_rect = self.rect.copy()

        self.animation_active = False
        self.is_press_active = False

        self.press_animation_steps = [-10]
        self.release_animation_steps = [10, 0]
        self.animation_steps = self.press_animation_steps

        self.animation_speed = 0.15
        self.current_step_index = 0

        self.initial_x = 0
        self.current_x = 0
        self.target_x = self.animation_steps[self.current_step_index]
        self.offset = vector()

    # animation controls
    def start_press_animation(self):
        self.animation_active = True
        self.is_press_active = True

    def start_release_animation(self):
        if self.is_press_active:
            self.extend_animation_with_release_steps()
        else:
            self.animation_steps = self.release_animation_steps
            self.animation_active = True

        self.is_press_active = False

    def reset_animation(self):
        self.animation_active = False
        self.is_press_active = False
        self.animation_steps = self.press_animation_steps
        self.current_step_index = 0
        self.target_x = self.animation_steps[self.current_step_index]
        self.current_x = 0
        self.update_rect(0)

    # animation
    def extend_animation_with_release_steps(self):
        press_list = self.press_animation_steps
        release_list = self.release_animation_steps
        self.animation_steps = press_list + release_list

    def advance_to_next_step(self):
        if self.is_last_step():
            if not self.is_press_active:
                self.reset_animation()
        else:
            self.current_step_index += 1
            self.update_rect(self.target_x)
            self.target_x = self.animation_steps[self.current_step_index]

    def has_reached_target_x(self, x):
        return abs(self.current_x - self.target_x) < abs(x)

    def is_last_step(self):
        return self.current_step_index >= len(self.animation_steps) - 1

    def animate(self, dt):
        if self.animation_active:
            direction = 1 if self.target_x > self.current_x else -1
            x_increment = direction * self.animation_speed * dt * 1000
            if self.has_reached_target_x(x_increment):
                self.advance_to_next_step()
            else:
                self.current_x += x_increment
                self.update_rect(self.current_x)

    # event
    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.start_press_animation()
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.animation_active:
                self.start_release_animation()


    # draw
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    # update
    def update_rect(self, x):
        self.rect.width = self.initial_rect.width + x
        self.rect.height = self.initial_rect.height + x
        self.rect.center = self.initial_rect.center

        factor = 1 + x / 100
        self.image = pygame.transform.scale_by(self.init_image, factor)

    def update(self, dt):
        self.animate(dt)

class Button:
    def __init__(self, image, rect, action):
        self.image = image
        self.rect = rect
        self.action = action
        self.offset = vector()
    
    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mouse_pos() - self.offset):
                self.action()

    def draw(self, surface):
        surface.blit(self.image, self.rect)