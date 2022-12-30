#Menu Colors

import pygame

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Mon menu')

# Chargement de la police
font = pygame.font.Font(None, 32)

# Création du menu
menu_items = ['Ajouter une image', 'Quitter']
current_item = 0

# Création des rectangles de sélection pour chaque élément du menu
menu_rects = []
for index, item in enumerate(menu_items):
    text = font.render(item, True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (200, 150 + index * 30)
    menu_rects.append(text_rect)

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Vérification si l'utilisateur a cliqué sur un élément du menu
            for index, rect in enumerate(menu_rects):
                if rect.collidepoint(event.pos):
                    current_item = index
                    if menu_items[current_item] == 'Quitter':
                        running = False
                    elif menu_items[current_item] == 'Ajouter une image':
                        # Code pour ajouter une image à l'écran
                        pass
        if event.type == pygame.MOUSEMOTION:
            # Vérification si la souris est sur un élément du menu
            for index, rect in enumerate(menu_rects):
                if rect.collidepoint(event.pos):
                    current_item = index
                    break
    
    # Dessin du menu
    screen.fill(BLACK)
    for index, item in enumerate(menu_items):
        color = WHITE if index == current_item else (200, 200, 200)
        text = font.render(item, True, color)
        text_rect = text.get_rect()
        text_rect.center = (200, 150 + index * 30)
        screen.blit(text, text_rect)
    
    # Mise à jour de l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
