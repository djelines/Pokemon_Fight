# Créé par chari, le 01/12/2023 en Python 3.7
import pygame
from pygame.locals import *
pygame.init()

largeur = 1000
hauteur = 600
menu = "Images/menu.png"
taille_image = (1000,600)
titre_fenetre = "Pokémon Fight"


def musique():
    #Inistialisation de la musique
    pygame.mixer.music.load('Music/castlevania.mp3')
    #Volume de la musique
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)


def creation_fenetre(largeur,hauteur):
    """ création d'une fenêtre de taille largeur x hauteur"""
    global fenetre
    #création d'une fenêtre de taille largeur x hauteur
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption(titre_fenetre)
    menu_background = pygame.image.load(menu).convert()
    #Affiche le fond "menu"
    menu_redi = pygame.transform.scale(menu_background, taille_image)
    fenetre.blit(menu_redi, (0,0))
    pygame.display.flip()


    #Boucle principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                    running = False  # Quitter la boucle principale si l'utilisateur ferme la fenêtre
            elif event.type == KEYDOWN and event.key == K_ESCAPE :
                    running = False # Quitter la boucle principale si l'utilisateur appuie sur échap
            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Vérifier le clic de souris
                # Récupérer les coordonnées du clic
                x, y = event.pos
                x2, y2 = event.pos
                # Vérifier si le clic est dans la zone du texte "Exit"
                if (largeur // 2.34 <= x <= largeur // 2.34 + 200) and (hauteur // 1.4 <= y <= hauteur // 1.4 + 50):
                    running = False  # Quitter la boucle principale si l'utilisateur a cliqué sur "Exit"
                if (largeur // 2.34 <= x <= largeur // 2.34 + 200) and (hauteur // 1.7 <= y <= hauteur // 1.7 + 50):
                    running = False  # Quitter la boucle principale si l'utilisateur a cliqué sur "Play"
                    import Pokedex_v1 #Importation du jeu si le joueur appuie sur "play"
musique()
creation_fenetre(largeur,hauteur)
pygame.quit()
