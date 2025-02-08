# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 10:36:54 2021

@author: charamond
"""

import pygame 		# import de la bibliothèque pygame

fenetre = pygame.display.set_mode((500,500)) # instance fenêtre graphique


class Grille():
    def __init__(self,larg,haut):
        """ une simple liste de coordonnée x,y de valeur 0 correspond à eteind 
        exemple 4 par 3 : [[0000],[0000],[0000]]"""
        self.matrix = [[ 0 for h in range(haut)]for l in range(larg)]

def dessin_grille(g,cote):
    """ dessine les ligne de la grille """
    xfin = pygame.display.get_window_size()[0]
    yfin = pygame.display.get_window_size()[1]
    for pos in range(len(g.matrix)):
        pygame.draw.line(fenetre,(255,100,100),(pos*cote,0),(pos*cote,xfin),2) # définition d'une ligne
        pygame.draw.line(fenetre,(255,100,100),(0,pos*cote),(xfin,pos*cote),2) # définition d'une ligne

def des_carre(x,y,coul,cote):
    """dessine la couleur du carré de coordonnée x,y"""
    pygame.draw.rect(fenetre, coul,(x*cote,y*cote,cote,cote))
    

def dessin_cellules(g,cote):
    """ dessine les carrés de la grille soit allumé soit eteint"""
    for celX in range(len(g.matrix)):           # chaque verticale
        for celY in range(len(g.matrix[0])) :   # chaque cellule de la verticale
            if g.matrix[celX][celY] == 0:
                des_carre(celX,celY,(100,100,100),cote)
            else :
                des_carre(celX,celY,(220,220,220),cote)

def main1():     # fonction principale
    g = Grille(20,20)                           # largeur, hauteur
    fenetre.fill((250,250,150))                 # couleur
    run = True                                  # boucke du script pour l'arret
    cote = int(pygame.display.get_window_size()[0]/20) # nbre de pixel d'un coté
    
    while run:                                  # boucle sans fin!!
        for event in pygame.event.get():        # parcours les évéments pygame
            if event.type == pygame.QUIT:       # croix en haut à droite de la fenetre (True or False)
                run = False                     # fin du while
            if event.type == pygame.MOUSEBUTTONDOWN:        # evenement appui
                
                if pygame.mouse.get_pressed() == (1,0,0):   # détection button gauche
                    i = pygame.mouse.get_pos()[0] // cote   # coordonnée x de la souris
                    j = pygame.mouse.get_pos()[1] // cote   # sur y # 
                    
                    if g.matrix[i][j] == 0:
                        g.matrix[i][j] = 1
                    else: 
                        g.matrix[i][j] = 0
            
            if event.type == pygame.MOUSEBUTTONUP:  # evement lacher bouton
                pass                                # ne fain rien 

        fenetre.fill((250,250,150))         # efface la fenetre avec la couleur
        dessin_cellules(g,cote)             # dessinne les cellules
        dessin_grille(g,cote)               # dessine la grille
        pygame.display.flip()               # affiche des présentations graphiques (nécessaire)

            
    pygame.quit()                           # méthode de fermeture de l'instance fenêtre



if __name__ == "__main__" :    
    main1()