# Jeu isométrique sur le thème de Mars

Bienvenue dans notre jeu isométrique sur le thème de Mars ! Dans ce jeu, vous incarnez un explorateur de l'espace chargé de découvrir les secrets de la planète rouge.

## Comment jouer ?
Pour jouer, utilisez les flèches directionnelles de votre clavier pour vous déplacer et la barre d'espace pour sauter. Vous pouvez également utiliser les touches `W`, `A`, `S`, `D` pour vous déplacer. Utilisez la souris pour viser et cliquer pour tirer avec votre laser.

## Quels sont les objectifs du jeu ?
Votre objectif principal est de parcourir les différentes zones du jeu, de résoudre des énigmes et de collecter des objets pour progresser. Vous devrez également affronter des ennemis et des boss tout au long de votre aventure.

## Quels sont les modes de jeu disponibles ?
Notre jeu vous offre plusieurs modes de jeu pour varier les plaisirs :

Mode histoire : suivez l'histoire de votre personnage et découvrez les secrets de Mars
Mode survie : affrontez des vagues d'ennemis sans fin
Mode coopération : jouez avec un ami en ligne et affrontez les ennemis ensemble

## Où puis-je obtenir de l'aide ?
Si vous rencontrez des problèmes ou si vous avez des questions sur le fonctionnement du jeu, consultez notre section [Aide et Support](https://www.youtube.com/watch?v=keyRM3h_7tk) ou envoyez-nous un message sur notre page [Contact](https://www.youtube.com/shorts/nGp_2ZAUWOs). Nous serons heureux de vous aider !



Pour créer un menu permettant d'ajouter des bâtiments sur la map dans un jeu isométrique en utilisant Pygame, vous pouvez utiliser les éléments suivants :

1- Créer une liste de bâtiments disponibles dans le jeu, avec pour chaque bâtiment une image et des coordonnées de placement sur la map.

2- Créer une fonction de dessin de menu affichant cette liste de bâtiments sous forme de boutons cliquables. Cette fonction peut utiliser la méthode blit de Pygame pour afficher chaque bâtiment en tant qu'image à l'écran, et la méthode draw.rect pour dessiner un rect autour de chaque image pour créer l'effet de bouton.

3- Gérer les événements de souris pour détecter si l'utilisateur clique sur l'un des boutons du menu. Si l'utilisateur clique sur un bouton, vous pouvez utiliser la position de la souris pour déterminer quel bâtiment a été sélectionné et ajouter ce bâtiment à la map à l'emplacement souhaité.


CheckList

- Cliqué déplacé
- Beug de la map
- Emplacement isométrique
