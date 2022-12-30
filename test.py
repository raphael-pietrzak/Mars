# Menu

import pygame

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Mon menu')

# Chargement de la police
font = pygame.font.Font(None, 32)

# Création du menu
menu_items = ['Ajouter une image', 'Quitter','Tower', 'House', 'Factory']
current_item = 0

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_item = (current_item - 1) % len(menu_items)
            if event.key == pygame.K_DOWN:
                current_item = (current_item + 1) % len(menu_items)
            if event.key == pygame.K_RETURN:
                if menu_items[current_item] == 'Quitter':
                    running = False
                elif menu_items[current_item] == 'Ajouter une image':
                    # Code pour ajouter une image à l'écran
                    pass
    
    # Dessin du menu
    screen.fill(BLACK)
    for index, item in enumerate(menu_items):
        if index == current_item:
            color = WHITE
        else:
            color = (200, 200, 200)
        text = font.render(item, True, color)
        text_rect = text.get_rect()
        text_rect.center = (200, 150 + index * 30)
        screen.blit(text, text_rect)
    
    # Mise à jour de l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()