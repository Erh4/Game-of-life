from random import randint
import pygame


class Cellule:
    def __init__(self):
        """Initialise une cellule"""
        self.actuel = False
        self.futur = False
        self.liste_voisines = None
        
    def est_vivant(self):
        """Renvoie l'état actuel"""
        return self.actuel
    
    def set_voisins(self, liste):
        """Affecte à la liste des voisines la :liste:"""
        self.liste_voisines = liste
        
    def get_voisins(self):
        """Renvoie la liste des cellules voisines de la cellule"""
        return self.liste_voisines
    
    def naitre(self):
        """met l'état futur à True"""
        self.futur = True 
        
    def mourir(self):
        """met l'état futur à False"""
        self.futur = False
        
    def basculer(self):
        """Fait passer l'état actuel à l'état futur"""
        self.actuel = self.futur
        
    def __str__(self):
        """Affichage de la cellule dans la grille"""
        if self.est_vivant():
            print('X')
        else:
            print('-')
            
    def calcul_etat_futur(self):
        """Implémente les reègles d'évolition d'une cellule en changeant l'état futur"""
        if len(self.get_voisins()) in [2,3]:
            if len(self.get_voisins()) == 3 or self.est_vivant():
                self.naitre()
        else:
            self.mourir()

class Grille:
    def __init__(self, largeur, hauteur, matrice = None):
        """Initialise la grille de cellules"""
        self.largeur = largeur
        self.hauteur = hauteur

        if matrice == None:
            self.matrice = [[Cellule() for i in range(self.largeur)] for j in range(self.hauteur)]
        else:
            self.matrice = matrice
    
    def get_cellule(self, x, y):
        """Renvoie la cellule située dans la case (i,j) de la grille
        :x: int() position x dans la grille
        :y: int() position y dans la grille"""
        return self.matrice[y][x]
    
    def get_largeur(self):
        """Récupère la largeur de la grille"""
        return self.largeur
    
    def hauteur(self):
        """Récupère la hauteur de la grille"""
        return self.hauteur
    
    def get_voisins(self, x, y):
        """Renvoie la liste des voisins d'une cellule
        :x: int() position x dans la grille
        :y: int() position y dans la grille"""
        return self.get_cellule(x,y).get_voisins()
    
    def affecte_voisins(self, x, y):
        """Affecte à chaque cellule de la grille la liste de ses voisins
        :x: int() position x dans la grille
        :y: int() position y dans la grille
        Renvoie la liste des voisins"""
        liste_case_voisine = []
        for hauteur_case in range(3):
            for largeur_case in range(3):
                posX = x-1+largeur_case
                posY = y-1+hauteur_case
                
                if posX < 0:
                    posX = self.largeur-1
                    
                if posX > self.largeur-1:
                    posX = 0
                    
                if posY < 0:
                    posY = self.hauteur-1
                
                if posY > self.hauteur-1:
                    posY = 0
                    
                if self.get_cellule(posX, posY).est_vivant():
                    if self.get_cellule(posX, posY) != self.get_cellule(x,y):
                        liste_case_voisine.append(self.get_cellule(posX, posY))

  
        return liste_case_voisine
    
    def __str__(self):
        """Affiche la grille"""
        chaine = ""
        for ligne in self.matrice:
            for case in ligne:
                if case.est_vivant():
                    chaine += "X"
                else:
                    chaine += "-"
                chaine += " "
            chaine += "\n"
        return chaine

    def remplir_alea(self, taux,g):
        """Change aléatoirement l'état d'une cellule selon le taux définie
        :taux: int() entre 1 et 100"""
        for i in range(self.largeur):
            for j in range(self.hauteur):
                #print(i,j)
                d = randint(1,100)

                if d <= taux:
                    self.get_cellule(i, j).actuel = True
                    g.matrix[i][j] = 1



    def actualise(self,g):
        """Actualise l'entièreté des cellules de la grille dans leur état futur"""
        for i in range(self.largeur):
            for j in range(self.hauteur):
                self.get_cellule(i, j).basculer()
                if self.get_cellule(i,j).est_vivant():
                    g.matrix[i][j] = 1
                else:
                    g.matrix[i][j] = 0


    def jeu(self,g, fenetre):
        """Analyse toutes les cellules de la grille et calcule leur état futur"""
        for i in range(self.largeur):
            for j in range(self.hauteur):
                self.get_cellule(i, j).liste_voisines = self.affecte_voisins(i, j)
                self.get_cellule(i, j).calcul_etat_futur()
        self.actualise(g)
        fenetre.fill((250, 250, 150))  # efface la fenetre avec la couleur
        dessin_cellules(g, 20, fenetre)  # dessinne les cellules
        dessin_grille(g, 20, fenetre)  # dessine la grille
        pygame.display.flip()  # affiche des présentations graphiques (nécessaire)

class Interface():
    def __init__(self, larg, haut):
        """ une simple liste de coordonnée x,y de valeur 0 correspond à eteind
        exemple 4 par 3 : [[0000],[0000],[0000]]"""
        self.matrix = [[0 for h in range(haut)] for l in range(larg)]


def dessin_grille(g, cote, fenetre):
    """ dessine les ligne de la grille """
    xfin = pygame.display.get_window_size()[0]
    yfin = pygame.display.get_window_size()[1]
    for pos in range(len(g.matrix)):
        pygame.draw.line(fenetre, (255, 100, 100), (pos * cote, 0), (pos * cote, xfin), 2)  # définition d'une ligne
        pygame.draw.line(fenetre, (255, 100, 100), (0, pos * cote), (xfin, pos * cote), 2)  # définition d'une ligne


def des_carre(x, y, coul, cote, fenetre):
    """dessine la couleur du carré de coordonnée x,y"""
    pygame.draw.rect(fenetre, coul, (x * cote, y * cote, cote, cote))


def dessin_cellules(g, cote, fenetre):
    """ dessine les carrés de la grille soit allumé soit eteint"""
    for celX in range(len(g.matrix)):  # chaque verticale
        for celY in range(len(g.matrix[0])):  # chaque cellule de la verticale
            if g.matrix[celX][celY] == 0:
                des_carre(celX, celY, (100, 100, 100), cote, fenetre)
            else:
                des_carre(celX, celY, (220, 220, 220), cote, fenetre)

def interface(largeur, hauteur, type_jeu, lambdaleatoire):  # fonction principale
    """Interface principale du jeu qui va initialiser la fenetre et permettre à l'utilisateur de modifier s'il le souhaite le cases de départ"""
    fenetre = pygame.display.set_mode((largeur * 20, hauteur * 20))  # instance fenêtre graphique
    grille = Grille(largeur, hauteur)
    g = Interface(largeur, hauteur)  # largeur, hauteur
    fenetre.fill((250, 250, 150))  # couleur
    run = True  # boucke du script pour l'arret
    cote = 20  # nbre de pixel d'un coté
    if type_jeu == 1:
        grille.remplir_alea(lambdaleatoire, g)
    while run:  # boucle sans fin!!
        for event in pygame.event.get():  # parcours les évéments pygame
            if event.type == pygame.QUIT:  # croix en haut à droite de la fenetre (True or False)
                run = False  # fin du while
            if type_jeu == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:  # evenement appui

                    if pygame.mouse.get_pressed() == (1, 0, 0):  # détection button gauche
                        i = pygame.mouse.get_pos()[0] // cote  # coordonnée x de la souris
                        j = pygame.mouse.get_pos()[1] // cote  # sur y #

                        if g.matrix[i][j] == 0:
                            g.matrix[i][j] = 1
                            grille.get_cellule(i, j).actuel = True
                        else:
                            g.matrix[i][j] = 0
                            grille.get_cellule(i, j).actuel = False

                if event.type == pygame.MOUSEBUTTONUP:  # evement lacher bouton
                    pass  # ne fain rien

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    jeu_run = True
                    while jeu_run:
                        grille.jeu(g, fenetre)
                        for event1 in pygame.event.get():
                            if event1.type == pygame.QUIT:  # croix en haut à droite de la fenetre (True or False)
                                jeu_run = False
                                run = False  # fin du while

        fenetre.fill((250, 250, 150))  # efface la fenetre avec la couleur
        dessin_cellules(g, cote, fenetre)  # dessinne les cellules
        dessin_grille(g, cote, fenetre)  # dessine la grille
        pygame.display.flip()  # affiche des présentations graphiques (nécessaire)

    pygame.quit()  # méthode de fermeture de l'instance fenêtre

def main():
    """Demande à l'utilisateur les paramètres de base de la simulation puis lance l'interface"""
    largeur = int(input("Largeur de la grille (max 96): "))
    hauteur = int(input("Hauteur de la grille (max 50): "))

    type_jeu = int(input("0) Dessin manuel\t1)Dessin aléatoire\n-->"))

    if type_jeu == 1:
        lambdaleatoire = int(input("Taux de cellules en vie (entre 1 et 100) : "))
    else:
        lambdaleatoire = None

    interface(largeur, hauteur, type_jeu, lambdaleatoire)

main()