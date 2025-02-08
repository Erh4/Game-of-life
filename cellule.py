from random import randint
from time import sleep

class Cellule:
    def __init__(self):
        self.actuel = False
        self.futur = False
        self.liste_voisines = None
        
    def est_vivant(self):
        return self.actuel
    
    def set_voisins(self, liste):
        self.liste_voisines = liste
        
    def get_voisins(self):
        return self.liste_voisines
    
    def naitre(self):
        self.futur = True 
        
    def mourir(self):
        self.futur = False
        
    def basculer(self):
        self.futur = self.actuel
        
    def __str__(self):
        if self.est_vivant():
            print('X')
        else:
            print('-')
            
    def calcul_etat_futur(self):
        #print("?")
        if not len(self.liste_voisines) in [2,3] and self.est_vivant():
            self.mourir()
            #print("morte")
        if not self.est_vivant() and len(self.liste_voisines) == 3:
            self.naitre()
            #print("née")
            
            
class Grille:
    def __init__(self, largeur, hauteur, matrice = None):
        self.largeur = largeur
        self.hauteur = hauteur
        if matrice == None:
            self.matrice = [[Cellule() for i in range(self.largeur)] for j in range(hauteur)]
            
        else:
            self.matrice = matrice
    
    def get_cellule(self, x, y):
        return self.matrice[y][x]
    
    def get_largeur(self):
        return self.largeur
    
    def hauteur(self):
        return self.hauteur
    
    def get_voisins(self, i, j):
        return self.get_cellule(i,j).get_voisins()
    
    def affecte_voisins(self, x, y):
        liste_case_voisine = []
        for hauteur_case in range(3):
            for largeur_case in range(3):
                posX = x-1+largeur_case
                posY = y-1+hauteur_case
                
                if posX < 0:
                    posX = self.largeur
                    
                if posX > self.largeur-1:
                    posX = 0
                    
                if posY < 0:
                    posY = self.hauteur
                
                if posY > self.hauteur-1:
                    posY = 0
                    
                if self.get_cellule(posX, posY).est_vivant():
                    if self.get_cellule(posX, posY) != self.get_cellule(x,y):
                        liste_case_voisine.append(self.get_cellule(posX, posY))
  
        return liste_case_voisine
    
    def __str__(self):
        chaine = ""
        for ligne in self.matrice:
            for case in ligne:
                if case.est_vivant():
                    chaine += "X"
                else:
                    chaine += "-"
                
            chaine += "\n"
        return chaine

    def remplir_alea(self, taux):
        for i in range(self.largeur):
            for j in range(self.hauteur):
                
                d = randint(1,100)
                if d <= taux:
                    self.get_cellule(i, j).actuel = True
                    
    def jeu(self):
        for i in range(self.largeur):
            for j in range(self.hauteur):
                self.get_cellule(i, j).liste_voisines = self.affecte_voisins(i, j)
                print(self.get_cellule(i, j).actuel)
                print(self.get_cellule(i, j).liste_voisines)
                self.get_cellule(i, j).calcul_etat_futur()
                
        for i in range(self.largeur):
            for j in range(self.hauteur):
                self.get_cellule(i, j).basculer()
        
                
                
grille = Grille(10,10)
grille.remplir_alea(30)
#print(grille.affecte_voisins(1, 2))

for i in range(2):
    grille.jeu()
    print(grille)
    #sleep(3)
