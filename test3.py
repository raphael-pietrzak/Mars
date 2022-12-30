# Zoom Menu Pictures

import pygame

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Création de la fenêtre en mode plein écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Mon menu')

# Chargement des images du menu
factory = pygame.image.load('pictures/factory.jpeg')
quit_image = pygame.image.load('pictures/house.jpeg')

# # Redimensionnement des images LD
# size = max(factory.get_size())
# factory = pygame.transform.scale(factory, (size, size))
# quit_image = pygame.transform.scale(quit_image, (size, size))

# Redimensionnement des images HD
size = max(factory.get_size())
size = 75
factory = pygame.transform.smoothscale(factory, (size, size))
quit_image = pygame.transform.smoothscale(quit_image, (size, size))


# Création du menu
menu_items = [factory, quit_image]
current_item = 0

# Création des rectangles de sélection pour chaque élément du menu
menu_rects = []
x = 0  # Coordonnée x du premier élément du menu
for index, item in enumerate(menu_items):
    rect = item.get_rect()
    rect.left = x
    rect.top = 0
    menu_rects.append(rect)
    x = rect.right + 10  # Mise à jour de la coordonnée x pour l'élément suivant


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
                    if index == 1:
                        running = False
                    elif index == 0:
                        # Code pour ajouter une image à l'écran
                        pass
        if event.type == pygame.MOUSEMOTION:
            # Vérification si la souris est sur un élément du menu
            hovered = False
            for index, rect in enumerate(menu_rects):
                if rect.collidepoint(event.pos):
                    current_item = index
                    hovered = True
                    break
            if not hovered:
                current_item = -1
    
   # Dessin du menu
    screen.fill(BLACK)
    for index, item in enumerate(menu_items):
        if index == current_item:
            # Dessin d'un contour autour de l'image et agrandissement léger de l'image
            rect = menu_rects[index]
            pygame.draw.rect(screen, WHITE, rect, 2)
            item = pygame.transform.scale(item, (int(rect.width * 1.1), int(rect.height * 1.1)))
        screen.blit(item, menu_rects[index])
    
    # Mise à jour de l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
