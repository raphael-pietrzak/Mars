# Carrousel


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
images = []
for i in range(1, 5):
    image = pygame.image.load(f'pictures/image{i}.jpeg')
    images.append(image)

# Redimensionnement des images LD
size = 50
for index, image in enumerate(images):
    images[index] = pygame.transform.scale(image, (size, size))

# Création du menu
menu_items = images
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

# Définition de la zone de défilement pour le carrousel
scroll_area = pygame.Surface((screen.get_width(), menu_rects[0].height))
scroll_area_rect = scroll_area.get_rect()
scroll_area_rect.left = 0
scroll_area_rect.top = 0

# Définition de la vitesse de défilement du carrousel
scroll_speed = 5

# Définition de la position de départ du carrousel
scroll_position = 0

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
        if event.type == pygame.KEYDOWN:
            # Défilement du carrousel avec les touches gauche et droite
            if event.key == pygame.K_LEFT:
                scroll_position += scroll_speed
            elif event.key == pygame.K_RIGHT:
                scroll_position -= scroll_speed
    # Dessin du menu
    screen.fill(BLACK)
    
    # Dessin du carrousel dans la zone de défilement
    x = 0  # Coordonnée x du premier élément du carrousel
    for index, item in enumerate(menu_items):
        rect = menu_rects[index]
        rect.left = x - scroll_position
        if index == current_item:
            # Dessin d'un contour autour de l'image et agrandissement léger de l'image
            pygame.draw.rect(screen, WHITE, rect, 2)
            item = pygame.transform.scale(item, (int(rect.width * 1.1), int(rect.height * 1.1)))
        scroll_area.blit(item, rect)
        x = rect.right + 10  # Mise à jour de la coordonnée x pour l'élément suivant
    
    # Dessin de la zone de défilement sur l'écran
    screen.blit(scroll_area, scroll_area_rect)
    
    # Mise à jour de l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
