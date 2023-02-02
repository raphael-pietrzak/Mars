# Zoom Menu Pictures

import pygame

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Création de la fenêtre en mode plein écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Mon menu")

# Chargement des images du menu
factory = pygame.image.load("pictures/factory.jpeg")
quit_image = pygame.image.load("pictures/house.jpeg")

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
menu_items = [
    factory,
    quit_image,
    factory,
    quit_image,
    factory,
    quit_image,
    factory,
    quit_image,
]

# Item du menu
current_item = -1


# Création des rectangles de sélection pour chaque élément du menu
menu_rects = []
x = (
    screen.get_width() // 2 - (size + 10) * len(menu_items) // 2
)  # Coordonnée x du premier élément du menu
for index, item in enumerate(menu_items):
    rect = item.get_rect()
    rect.left = x
    rect.top = screen.get_height() - 100
    menu_rects.append(rect)
    x = rect.right + 10  # Mise à jour de la coordonnée x pour l'élément suivant


def draw_menu(current_item):
    for index, item in enumerate(menu_items):
        if index == current_item:
            # Dessin d'un contour autour de l'image et agrandissement léger de l'image
            rect = menu_rects[index]
            pygame.draw.rect(screen, WHITE, rect, 2)
            item = pygame.transform.scale(
                item, (int(rect.width * 1.1), int(rect.height * 1.1))
            )
        screen.blit(item, menu_rects[index])

    return current_item


