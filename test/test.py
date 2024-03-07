import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('get_abs_offset() Example')

# Create a parent surface
parent_surface = pygame.Surface((200, 150))
parent_surface.fill('turquoise')  # Fill with white color

# Create a child surface
child_surface = pygame.Surface((50, 50))
child_surface.fill((0, 0, 255))  # Fill with blue color



# Blit the child surface onto the parent surface
parent_surface.blit(child_surface, (30, 20))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    abs_offset = child_surface.get_abs_offset()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Blit the parent surface onto the screen
    screen.blit(parent_surface, (50, 50))

    # Draw a rectangle around the child surface using its absolute offset
    pygame.draw.rect(screen, (255, 0, 0), (abs_offset[0] + 50, abs_offset[1] + 50, 50, 50), 2)

    # Update the display
    pygame.display.flip()
