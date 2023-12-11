# Créé par Charfii, le 20/11/2023 en Python 3.7
import csv
from dico_personnages import *
from random import *
import copy


#### Partie Pygame ###
import pygame
from pygame.locals import *
pygame.init()


###################### 2ème Partie ########################

def lecture_fichier(personnages):
    """ Prend en paramètres un fichier csv (str) et retourne la liste des descripteurs
        et la table contenus dans ce fichier """
    fichier_ouvert = open(personnages,mode='r',encoding='utf-8')
    contenu=list(csv.reader(fichier_ouvert, delimiter=";"))
    liste_descripteurs=contenu[0] #IMPORTANT
    table=contenu[1:] #IMPORTANT
    fichier_ouvert.close()
    return liste_descripteurs,table

def creation_dico(table):
    """ Reprend la table créée avant (dict) et retourne le dictionnaire des personnages,
        un dictionnaire comme dans la première partie """
    dico_personnages = {}
    for l in table:
        print(l,len(l))
        dico_personnages[l[0]] = {
            'Numero': l[1],
            'Type 1': l[2],
            'Type 2': l[3],
            'PV': int(l[4]),
            'Attaque': int(l[5]),
            'Défense': int(l[6]),
            'Attaque special': int(l[7]),
            'Vitesse': int(l[8]),
            'Evolution': l[9],
            'Description': l[10],
            'Nom_fichier_image' : l[11]
        }
    return dico_personnages


def affiche(pokedex):
    """ Affiche les données du pokedex (dict) sous forme d'un tableau """
    for nom,val in pokedex.items():
        for descripteurs,valeur in val.items():
            print(str(descripteurs).center(20), end="  ")
            print(str(valeur).center(20), end="\n")


###################### 3ème Partie ########################

def liste_personnages(dico_personnages):
    """ Prend en paramètres le dictionnaire (dict) et retourne la liste des personnages présents dedans """
    L_perso_nom = []
    for nom in pokemons.keys():
        L_perso_nom.append(nom)
    return L_perso_nom

def selection_par_nom(nom_pokemon):
    """ Prend en paramètres un nom de personnage (str) et retourne le dictionnaire associé à ce personnage """
    return pokedex[nom_pokemon]

def selection_par_nom_copie(nom_pokemon):
    """ Retourne la copie du dictionnaire associé au nom du personnage passé en paramètres (str) """
    return copy.deepcopy(pokedex[nom_pokemon])

def selection_attaque(dico_personnages, n):
    """ Prend en paramètres le dictionnaire (dict) et un entier n (int), puis retourne le dictionnaire des
        personnages avec une attaque égale à n """
    L_attaque = []
    for nom,val in pokemons.items():
        if int(val['Attaque']) == n:
            L_attaque.append(nom)
    return L_attaque

def selection_vitesse(dico_personnages, n):
    """ Retourne le dictionnaire des personnages (dict) qui ont une vitesse strictement supérieure à n (int) """
    L_vitesse = []
    for nom,val in pokemons.items():
        if int(val['Vitesse']) >= n:
            L_vitesse.append(nom)
    return L_vitesse

def selection(dico_personnages:dict,champ:str,operateur:str,n:str,type_data = "str"):
    """ Cherche automatiquement ce qu'on passe en paramètres """
    L = []
    for nom,val in pokemons.items():
        if eval(f"{type_data}('{val[champ]}') {operateur} {type_data}('{n}')"):
            L.append(nom)
    return L

##################### 4ème Partie ########################

def attaque(personnage_qui_attaque,personnage_qui_defend):
    """ Prend en paramètres le dictionnaire d'un personnage qui attaque (type dict) et d'un qui défend,
        puis affiche les dégâts infligés au personnage en défense par le personnage qui attaque,
        et met à jour les PV du personnage défenseur """
    alea = randint(1,4)
    degats = int((((int(personnage_qui_attaque['Attaque']) * 1.6 + int(personnage_qui_attaque['Vitesse']) * 1.4) + 4) /
    (int(personnage_qui_attaque['Défense'])*0.5 ))*alea)
    PV_restant = int(personnage_qui_defend["PV"]) - degats
    personnage_qui_defend["PV"] = PV_restant
##    print(degats, alea, PV_restant, personnage_qui_defend["PV"])
    return personnage_qui_defend

def qui_en_premier(pokemon_1 : dict,pokemon_2 :dict):
    """ Prend en paramètres deux personnages de type dict et retourne un tuple qui contient
        le dictionnaire du personnage qui joue en premier puis celui du second """
    if pokemon_1['Vitesse'] >= pokemon_2['Vitesse']:
        return (pokemon_1,pokemon_2)
    else :
        return (pokemon_2,pokemon_1)


def combat(pokemon_1 : dict,pokemon_2:dict):
    """ Prend en paramètres deux personnages de type dict. Utilise les fonctions précédentes
        et retourne un tuple qui contient dans l'ordre, le dictionnaire du personnage gagnant,
        puis celui du perdant (celui qui n'a plus de PV) """
    pokemon_1, pokemon_2 = qui_en_premier(pokemon_1,pokemon_2)
    personnage_qui_attaque = pokemon_1
    personnage_qui_defend = pokemon_2
    while pokemon_1["PV"]>0 and pokemon_2["PV"]>0:
        attaque(personnage_qui_attaque,personnage_qui_defend)
        temp = personnage_qui_attaque
        personnage_qui_attaque = personnage_qui_defend
        personnage_qui_defend = temp
##        print(pokemon_1["PV"],pokemon_2["PV"])

    if pokemon_1["PV"] <= 0:
        pokemon_gagnant = pokemon_2
        pokemon_perdu = pokemon_1
    if pokemon_2["PV"]<=0:
        pokemon_gagnant = pokemon_1
        pokemon_perdu = pokemon_2
    return pokemon_gagnant,pokemon_perdu


##################### 5ème Partie ########################

descripteurs,table = lecture_fichier('personnages-1.csv') # Lire le fichier csv

pokedex = creation_dico(table) # Créer le dico

### Design de la fenetre ###

largeur = 1000
hauteur = 600
menu = "Images/menu.png"
selection_pokemons = "Images/selection_pokemons.png"
fight = "Images/fight.png"
img_fight = "Images/attaque.png"
taille_image = (1000,600)
taille_image_pokemons = (100,100)
titre_fenetre = "Pokémon Fight"
BLUE =  (40, 120, 230)
PINK = (255, 122, 241)


def menu_choix():

    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption(titre_fenetre)
    menu_choix = pygame.image.load(selection_pokemons).convert() #Affiche le fond "selection_pokemons"
    menu_redi_2 = pygame.transform.scale(menu_choix, taille_image) #Affiche le fond "menu"
    fenetre.blit(menu_redi_2, (0,0))

    coord_x = 80
    coord_y = 0

    for nom,fiche in pokedex.items():
        nom=pygame.image.load("Images/"+fiche['Nom_fichier_image'])
##        print(coord_x,coord_y)
        nom_redi_3 = pygame.transform.scale(nom,taille_image_pokemons)
        fenetre.blit(nom_redi_3,(coord_x,coord_y))
        coord_x += 120
        if coord_x > 800:
            coord_y += 140
            coord_x = 80
    pygame.display.flip()

def selection_equipe_1():
    """
    attente d'un clic et qui retourne les coordonnées du clic
    ou mets fin au jeu
    """
    equipe_1 = []
    running = True  # Variable pour contrôler la boucle principale

    while running and len(equipe_1)<3:

        for event in pygame.event.get():

            if event.type == QUIT:
                running = False  # Quitter la boucle principale si l'utilisateur ferme la fenêtre

            if event.type == MOUSEBUTTONDOWN :
                if event.button == 1:

                    clic_x = event.pos[0]
                    clic_y = event.pos[1]

                    if 80 <= clic_x <= 180 and 0 <= clic_y <= 140:
                        equipe_1.append(selection_par_nom_copie("Victini"))

                    if 200 <= clic_x <= 300  and 0 <= clic_y <= 140:
                        equipe_1.append(selection_par_nom_copie("Vipelierre"))

                    if 320 <= clic_x <= 420  and 0 <= clic_y <= 140:
                        equipe_1.append(selection_par_nom_copie("Lianaja"))

                    if 440 <= clic_x <= 540 and 0 <= clic_y <= 140:
                        equipe_1.append(selection_par_nom_copie("Majaspic"))

                    if 560 <= clic_x <= 660 and 0 <= clic_y <= 140:
                        equipe_1.append(selection_par_nom_copie("Gruikui"))

                    if 680 <= clic_x <= 780 and 0 <= clic_y <= 140:
                        equipe_1.append(selection_par_nom_copie("Grotichon"))

                    if 800 <= clic_x <= 900 and 0 <= clic_y <= 140:
                        equipe_1.append(selection_par_nom_copie("Roitiflam"))

                    if 80 <= clic_x <= 180 and 150 <= clic_y <= 290:
                        equipe_1.append(selection_par_nom_copie("Moustillon"))

                    if 200 <= clic_x <= 300  and 150 <= clic_y <= 290:
                        equipe_1.append(selection_par_nom_copie("Mateloutre"))

                    if 320 <= clic_x <= 420  and 150 <= clic_y <= 290:
                        equipe_1.append(selection_par_nom_copie("Clamiral"))

                    if 440 <= clic_x <= 540 and 150 <= clic_y <= 290:
                        equipe_1.append(selection_par_nom_copie("Ratentif"))

                    if 560 <= clic_x <= 660 and 150 <= clic_y <= 290:
                        equipe_1.append(selection_par_nom_copie("Miradar"))

                    if 680 <= clic_x <= 780 and 150 <= clic_y <= 290:
                        equipe_1.append(selection_par_nom_copie("Ponchiot"))

                    if 800 <= clic_x <= 900 and 150 <= clic_y <= 290:
                        equipe_1.append(selection_par_nom_copie("Ponchien"))

                    if 80 <= clic_x <= 180 and 300 <= clic_y <= 440:
                        equipe_1.append(selection_par_nom_copie("Mastouffe"))

                    if 200 <= clic_x <= 300  and 300 <= clic_y <= 440:
                        equipe_1.append(selection_par_nom_copie("Chacripan"))

                    if 320 <= clic_x <= 420  and 300 <= clic_y <= 440:
                        equipe_1.append(selection_par_nom_copie("Léopardus"))

                    if 440 <= clic_x <= 540 and 300 <= clic_y <= 440:
                        equipe_1.append(selection_par_nom_copie("Feuillajou"))

                    if 560 <= clic_x <= 660 and 300 <= clic_y <= 440:
                        equipe_1.append(selection_par_nom_copie("Feuiloutan"))

                    if 680 <= clic_x <= 780 and 300 <= clic_y <= 440:
                        equipe_1.append(selection_par_nom_copie("Flamajou"))

                    if 800 <= clic_x <= 900 and 300 <= clic_y <= 440:
                        equipe_1.append(selection_par_nom_copie("Flamoutan"))

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False  # Quitter la boucle principale lorsque la touche Échap est pressée

            print(equipe_1)
    return equipe_1,equipe_1[0],equipe_1[1],equipe_1[2]

def selection_equipe_2():
    equipe_2 = []
    running = True  # Variable pour contrôler la boucle principale

    while running and len(equipe_2)<3:

        for event in pygame.event.get():

            if event.type == QUIT:
                running = False  # Quitter la boucle principale si l'utilisateur ferme la fenêtre

            if event.type == MOUSEBUTTONDOWN :
                if event.button == 1:

                    clic_x = event.pos[0]
                    clic_y = event.pos[1]

                    if 80 <= clic_x <= 180 and 0 <= clic_y <= 140:
                        equipe_2.append(selection_par_nom_copie("Victini"))

                    if 200 <= clic_x <= 300  and 0 <= clic_y <= 140:
                        equipe_2.append(selection_par_nom_copie("Vipelierre"))

                    if 320 <= clic_x <= 420  and 0 <= clic_y <= 140:
                        equipe_2.append(selection_par_nom_copie("Lianaja"))

                    if 440 <= clic_x <= 540 and 0 <= clic_y <= 140:
                        equipe_2.append(selection_par_nom_copie("Majaspic"))

                    if 560 <= clic_x <= 660 and 0 <= clic_y <= 140:
                        equipe_2.append(selection_par_nom_copie("Gruikui"))

                    if 680 <= clic_x <= 780 and 0 <= clic_y <= 140:
                        equipe_2.append(selection_par_nom_copie("Grotichon"))

                    if 800 <= clic_x <= 900 and 0 <= clic_y <= 140:
                        equipe_2.append(selection_par_nom_copie("Roitiflam"))

                    if 80 <= clic_x <= 180 and 150 <= clic_y <= 290:
                        equipe_2.append(selection_par_nom_copie("Moustillon"))

                    if 200 <= clic_x <= 300  and 150 <= clic_y <= 290:
                        equipe_2.append(selection_par_nom_copie("Mateloutre"))

                    if 320 <= clic_x <= 420  and 150 <= clic_y <= 290:
                        equipe_2.append(selection_par_nom_copie("Clamiral"))

                    if 440 <= clic_x <= 540 and 150 <= clic_y <= 290:
                        equipe_2.append(selection_par_nom_copie("Ratentif"))

                    if 560 <= clic_x <= 660 and 150 <= clic_y <= 290:
                        equipe_2.append(selection_par_nom_copie("Miradar"))

                    if 680 <= clic_x <= 780 and 150 <= clic_y <= 290:
                        equipe_2.append(selection_par_nom_copie("Ponchiot"))

                    if 800 <= clic_x <= 900 and 150 <= clic_y <= 290:
                        equipe_2.append(selection_par_nom_copie("Ponchien"))

                    if 80 <= clic_x <= 180 and 300 <= clic_y <= 440:
                        equipe_2.append(selection_par_nom_copie("Mastouffe"))

                    if 200 <= clic_x <= 300  and 300 <= clic_y <= 440:
                        equipe_2.append(selection_par_nom_copie("Chacripan"))

                    if 320 <= clic_x <= 420  and 300 <= clic_y <= 440:
                        equipe_2.append(selection_par_nom_copie("Léopardus"))

                    if 440 <= clic_x <= 540 and 300 <= clic_y <= 440:
                        equipe_2.append(selection_par_nom_copie("Feuillajou"))

                    if 560 <= clic_x <= 660 and 300 <= clic_y <= 440:
                        equipe_2.append(selection_par_nom_copie("Feuiloutan"))

                    if 680 <= clic_x <= 780 and 300 <= clic_y <= 440:
                        equipe_2.append(selection_par_nom_copie("Flamajou"))

                    if 800 <= clic_x <= 900 and 300 <= clic_y <= 440:
                        equipe_2.append(selection_par_nom_copie("Flamoutan"))


            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False  # Quitter la boucle principale lorsque la touche Échap est pressée

            print(equipe_2)
    return equipe_2,equipe_2[0],equipe_2[1],equipe_2[2]


def musique_2():
    #Inistialisation de la musique
    pygame.mixer.music.load('Music/battle.mp3')
    #Volume de la musique
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)


def combat_affiche(equipe_1,pokemon_1,pokemon_2,pokemon_3,equipe_2,pokemon_4,pokemon_5,pokemon_6):
    vainqueur_1 = 0
    vainqueur_2 = 0

    pos_img_x = 250
    pos_img_x_2 = 650
    pos_img_y = 230

    pos_x = 400
    pos_y = 400

    pos_pv_y = 20

    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption(titre_fenetre)
    fight_affiche = pygame.image.load(fight).convert() #Affiche le fond "fight"
    fight_affiche_2 = pygame.transform.scale(fight_affiche, taille_image) #Affiche le fond "fight"
    fenetre.blit(fight_affiche_2, (0,0))

    if pokemon_1:
        nom_image=pygame.image.load("Images/"+pokemon_1['Nom_fichier_image'])
        fenetre.blit(nom_image,(pos_img_x,pos_img_y))
    if pokemon_4:
        nom_image=pygame.image.load("Images/"+pokemon_4['Nom_fichier_image'])
        fenetre.blit(nom_image,(pos_img_x_2,pos_img_y))

    pokemon_1, pokemon_4 = qui_en_premier(pokemon_1,pokemon_4)
    personnage_qui_attaque = pokemon_1
    personnage_qui_defend = pokemon_4

    while pokemon_1["PV"]>0 and pokemon_4["PV"]>0:

        attaque(personnage_qui_attaque,personnage_qui_defend)
        temp = personnage_qui_attaque
        personnage_qui_attaque = personnage_qui_defend
        personnage_qui_defend = temp
##        print(pokemon_1["PV"],pokemon_4["PV"])

        attaque_img = pygame.image.load(img_fight).convert_alpha()
        attaque_img_2 = pygame.transform.scale(attaque_img,(325,150))
        fenetre.blit(attaque_img_2,(330,225))
        pygame.display.flip()

        font = pygame.font.SysFont('Comic Sans MS', 20)
        texte_pv_1 = font.render(f'{pokemon_1["PV"]}', True, BLUE)
        texte_pv_2 = font.render(f'{pokemon_4["PV"]}', True, PINK)

        fenetre.blit(texte_pv_1, (250, pos_pv_y))
        fenetre.blit(texte_pv_2, (700, pos_pv_y))
        pygame.time.wait(1000)
        pos_pv_y += 20

        pygame.display.flip()

    pokemon_gagnant,pokemon_perdu = combat(pokemon_1,pokemon_4)


    if pokemon_1 == pokemon_gagnant:
        vainqueur_1 += 1
    else :
        vainqueur_2 += 1
##    print(vainqueur_1,vainqueur_2)
    pygame.display.flip()
    pygame.time.wait(1000)
    fenetre.blit(fight_affiche_2,(0,0))

    if pokemon_2:
        nom_image=pygame.image.load("Images/"+pokemon_2['Nom_fichier_image'])
        fenetre.blit(nom_image,(pos_img_x,pos_img_y))
    if pokemon_5:
        nom_image=pygame.image.load("Images/"+pokemon_5['Nom_fichier_image'])
        fenetre.blit(nom_image,(pos_img_x_2,pos_img_y))

    pokemon_2, pokemon_5 = qui_en_premier(pokemon_2,pokemon_5)
    personnage_qui_attaque = pokemon_2
    personnage_qui_defend = pokemon_5

    pos_pv_y = 20
    while pokemon_2["PV"]>0 and pokemon_5["PV"]>0:

        attaque(personnage_qui_attaque,personnage_qui_defend)
        temp = personnage_qui_attaque
        personnage_qui_attaque = personnage_qui_defend
        personnage_qui_defend = temp
##        print(pokemon_2["PV"],pokemon_5["PV"])

        attaque_img = pygame.image.load(img_fight).convert_alpha()
        attaque_img_2 = pygame.transform.scale(attaque_img,(325,150))
        fenetre.blit(attaque_img_2,(330,225))
        pygame.display.flip()

        font = pygame.font.SysFont('Comic Sans MS', 20)
        texte_pv_1 = font.render(f'{pokemon_2["PV"]}', True, BLUE)
        texte_pv_2 = font.render(f'{pokemon_5["PV"]}', True, PINK)

        fenetre.blit(texte_pv_1, (250, pos_pv_y))
        fenetre.blit(texte_pv_2, (700, pos_pv_y))
        pygame.time.wait(1000)
        pos_pv_y += 20

        pygame.display.flip()

    pokemon_gagnant,pokemon_perdu = combat(pokemon_2,pokemon_5)

    if pokemon_2 == pokemon_gagnant:
        vainqueur_1 += 1
    else :
        vainqueur_2 += 1
##    print(vainqueur_1,vainqueur_2)
    pygame.display.flip()
    pygame.time.wait(1000)
    fenetre.blit(fight_affiche_2,(0,0))

    if pokemon_3:
        nom_image=pygame.image.load("Images/"+pokemon_3['Nom_fichier_image'])
        fenetre.blit(nom_image,(pos_img_x,pos_img_y))
    if pokemon_6:
        nom_image=pygame.image.load("Images/"+pokemon_6['Nom_fichier_image'])
        fenetre.blit(nom_image,(pos_img_x_2,pos_img_y))

    pokemon_3, pokemon_6 = qui_en_premier(pokemon_3,pokemon_6)
    personnage_qui_attaque = pokemon_3
    personnage_qui_defend = pokemon_6

    pos_pv_y = 20
    while pokemon_3["PV"]>0 and pokemon_6["PV"]>0:

        attaque(personnage_qui_attaque,personnage_qui_defend)
        temp = personnage_qui_attaque
        personnage_qui_attaque = personnage_qui_defend
        personnage_qui_defend = temp
##        print(pokemon_3["PV"],pokemon_6["PV"])

        attaque_img = pygame.image.load(img_fight).convert_alpha()
        attaque_img_2 = pygame.transform.scale(attaque_img,(325,150))
        fenetre.blit(attaque_img_2,(330,225))
        pygame.display.flip()

        font = pygame.font.SysFont('Comic Sans MS', 20)
        texte_pv_1 = font.render(f'{pokemon_3["PV"]}', True, BLUE)
        texte_pv_2 = font.render(f'{pokemon_6["PV"]}', True, PINK)

        fenetre.blit(texte_pv_1, (250, pos_pv_y))
        fenetre.blit(texte_pv_2, (700, pos_pv_y))
        pygame.time.wait(1000)
        pos_pv_y += 20

        pygame.display.flip()
    pokemon_gagnant,pokemon_perdu = combat(pokemon_3,pokemon_6)

    if pokemon_3 == pokemon_gagnant:
        vainqueur_1 += 1
    else :
        vainqueur_2 += 1
##    print(vainqueur_1,vainqueur_2)
    pygame.display.flip()
    pygame.time.wait(1000)
    fenetre.blit(fight_affiche_2,(0,0))

    if vainqueur_1>vainqueur_2:
        for pokemon_equipe_1 in equipe_1:
            nom_image=pygame.image.load("Images/"+pokemon_equipe_1['Nom_fichier_image'])
            fenetre.blit(nom_image,(pos_x,pos_y))
            pos_x += 50

    if vainqueur_2>vainqueur_1:
        for pokemon_equipe_2 in equipe_2:
            nom_image=pygame.image.load("Images/"+pokemon_equipe_2['Nom_fichier_image'])
            fenetre.blit(nom_image,(pos_x,pos_y))
            pos_x += 50
    pygame.display.flip()




#### Fin du pygame ###

# JEU
menu_choix()
pygame.mixer.music.stop( )
musique_2()
equipe_1, pokemon_1,pokemon_2,pokemon_3= selection_equipe_1()
equipe_2, pokemon_4,pokemon_5,pokemon_6 = selection_equipe_2()
combat_affiche(equipe_1,pokemon_1,pokemon_2,pokemon_3,equipe_2,pokemon_4,pokemon_5,pokemon_6)
pygame.time.wait(2000)
pygame.quit()


###################### Main ########################

##descripteurs,table = lecture_fichier('personnages-1.csv') # Lire le fichier csv

##pokedex = creation_dico(table) # Créer le dico

##affiche(pokedex) # Afficher le dico
##
##print("")
##print(liste_personnages(pokedex)) # Pour avoir la liste de tous les pokemons
##
##print("")
##print(selection_par_nom("Victini")) # Pour ouvrir le dico du pokemon selectionner
##
##print("")
##selection_par_nom_copie("Vipelierre")
##
##print("")
##print(selection_attaque(pokedex, 100)) # Le dico des pokemons avec une attaque égale à n
##
##print("")
##print(selection_vitesse(pokedex, 100)) # Le dico des pokemons avec une vitesse supérieure égale à n
##
##print("")
##print(selection(pokedex,"Attaque", ">=","60",type_data = "int"))
##
##print("")
##v1 = selection_par_nom("Victini")
##v2=selection_par_nom("Vipelierre")
##print(attaque(v1,v2))
##
##print("")
##print(attaque(selection_par_nom("Moustillon"),selection_par_nom("Grotichon")))
##
##print("vitesse :")
##v3 = selection_par_nom("Moustillon")
##v4=selection_par_nom("Vipelierre")
##print(qui_en_premier(v3,v4))
##
##print("combat :")
##v5 = selection_par_nom("Moustillon")
##v6 = selection_par_nom("Flamoutan")
##print(combat(v5,v6))
