
import pygame
# from main import sprites


# Initialisation de pygame
pygame.init()

# Définition de la fenêtre de jeu
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()

# Police de caractères pour afficher le texte à l'écran
font = pygame.font.Font(None, 36)

# Liste des bâtiments disponibles dans le jeu
buildings = [
    {"name": "Maison", "image": pygame.image.load("pictures/house.jpeg"), "x": 10, "y": 10},
    {"name": "Tour", "image": pygame.image.load("pictures/tower.jpeg"), "x": 50, "y": 50},
    {"name": "Usine", "image": pygame.image.load("pictures/factory.jpeg"), "x": 100, "y": 100},
]

# Taille des boutons du menu
button_width, button_height = 100, 50

# Marges entre les boutons du menu
button_margin_x, button_margin_y = 10, 10

# Offset du menu par rapport à l'écran
menu_offset_x, menu_offset_y = 10, 10

# Fonction de dessin du menu
def draw_menu():
    # Initialisation des coordonnées de placement du premier bouton du menu
    x, y = menu_offset_x, menu_offset_y

    # Pour chaque bâtiment de la liste, affichage de l'image en tant que bouton cliquable
    for building in buildings:
        # Création du rect du bouton
        rect = pygame.Rect(x, y, button_width, button_height)

        # Dessin du rect du bouton à l'écran
        pygame.draw.rect(screen, (255,0,0), rect, 1)

        # Affichage de l'image du bâtiment à l'intérieur du rect du bouton
        screen.blit(building["image"], rect)

        # Affichage du nom du bâtiment sous l'image
        text = font.render(building["name"], True, (255,0,0))
        text_rect = text.get_rect()
        text_rect.center = (x + button_width // 2, y + button_height + button_margin_y)
        screen.blit(text, text_rect)

        # Mise à jour des coordonnées de placement
        x += button_width + button_margin_x
        y += button_height + button_margin_y
