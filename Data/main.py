import sys
import pygame
import menu
from menu import menu_rects, current_item


class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dx, dy):
        # Mise à jour de la position du sprite
        self.rect.x += dx
        self.rect.y += dy

    def draw_rects(self, screen, color, thickness):
        # Dessin du rect du sprite à l'écran
        pygame.draw.rect(screen, color, self.rect, thickness)


# Initialisation de pygame
pygame.init()

# Définition de la fenêtre de jeu
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()


# Chargement des images
image1 = pygame.image.load("pictures/ground.png")
image2 = pygame.image.load("pictures/ground.png")
image3 = pygame.image.load("pictures/ground.png")
image4 = pygame.image.load("pictures/ground.png")

# Création des sprites
sprite1 = Sprite(10, 10, image1)
sprite2 = Sprite(image1.get_width(), 10, image2)
sprite3 = Sprite(10, image1.get_height(), image3)
sprite4 = Sprite(image1.get_width(), image1.get_height(), image4)

# Création du groupe de sprites
sprites = pygame.sprite.Group()
sprites.add(sprite1)
sprites.add(sprite2)
sprites.add(sprite3)
sprites.add(sprite4)

# Création du groupe de bâtiments
buildings = pygame.sprite.Group()

# Variable indiquant si le clic de la souris est enfoncé
click = False

# Variable indiquant qu'on pose un bâtiment
building_being_placed = False

# Police de caractères pour afficher le texte à l'écran
font = pygame.font.Font(None, 36)

# Boucle principale de jeu
while True:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Mise à jour de la variable click et de la position de la souris
            if not hovered:
                click = True
                last_x, last_y = event.pos
            else:
                building_being_placed = True
                building_image = pygame.image.load("pictures/house.jpeg")
                x, y = pygame.mouse.get_pos()
                building_sprite = Sprite(x, y, building_image)
                buildings.add(building_sprite)

            # Vérification si l'utilisateur a cliqué sur un élément du menu
            # for index, rect in enumerate(menu_rects):
            #     if rect.collidepoint(event.pos):
            #         current_item = index
            #         if index == 1:
            #             running = False
            #         elif index == 0:
            #             # Code pour ajouter une image à l'écran
            #             pass

        elif event.type == pygame.MOUSEBUTTONUP:
            # Mise à jour de la variable click
            click = False
            building_being_placed = False


        elif event.type == pygame.MOUSEMOTION:
            # Vérification si la souris est sur un élément du menu
            hovered = False
            for index, rect in enumerate(menu_rects):
                if rect.collidepoint(event.pos):
                    current_item = index
                    hovered = True
                    break
            if not hovered:
                current_item = -1

        elif event.type == pygame.KEYDOWN:
            # Déplacement du groupe de sprites en fonction de la touche pressée
            if event.key == pygame.K_UP:
                sprites.update(dx=0, dy=-10)
            elif event.key == pygame.K_DOWN:
                sprites.update(dx=0, dy=10)
            elif event.key == pygame.K_LEFT:
                sprites.update(dx=-10, dy=0)
            elif event.key == pygame.K_RIGHT:
                sprites.update(dx=10, dy=0)

    # Si le clic de la souris est enfoncé, déplacement du groupe de sprites
    if click:
        # Récupération de la position actuelle de la souris
        x, y = pygame.mouse.get_pos()
        # Calcul du déplacement du groupe de sprites
        dx = x - last_x
        dy = y - last_y
        sprites.update(dx, dy)
        # Mise à jour de la position de la souris
        last_x, last_y = x, y

    # Vérification de la position des sprites par rapport à l'écran
    for sprite in sprites:
        if sprite.rect.right < 0:
            # Déplacement du groupe de sprites vers la droite
            sprites.update(dx=sprite.image.get_width(), dy=0)
        elif sprite.rect.left > screen_width:
            # Déplacement du groupe de sprites vers la gauche
            sprites.update(dx=-sprite.image.get_width(), dy=0)
        elif sprite.rect.bottom < 0:
            # Déplacement du groupe de sprites vers le bas
            sprites.update(dx=0, dy=sprite.image.get_height())
        elif sprite.rect.top > screen_height:
            # Déplacement du groupe de sprites vers le haut
            sprites.update(dx=0, dy=-sprite.image.get_height())

    # Mise à jour de l'affichage
    screen.fill((0, 0, 0))

    sprites.draw(screen)
    

    # Affichage des coordonnées de la première sprite en haut à gauche de l'écran
    text = font.render(
        f"Coordonnées : ({sprite1.rect.x}, {sprite1.rect.y})", True, (255, 255, 255)
    )
    screen.blit(text, (10, 10))

    current_item = menu.draw_menu(current_item)

    pygame.display.flip()
