# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 13:52:48 2018

@author: Laurent
"""
TEMPS_BASE = 1
TEMPS_PROPAGATION = 0.0001
TEMPS_EXPLOSION = 5.5

E_TEMPS = 0
E_NATURE = 1

EVENEMENT_TOUR_JOUEUR = 1
EVENEMENT_EXPLOSION_BOMBE = 2
EVENEMENT_PROPAGATION = 3

PLATEAU_VIDE = 0
PLATEAU_PIERRE = 1
PLATEAU_BOIS = 2

DIRECTION_NORD = 0
DIRECTION_EST = 1
DIRECTION_SUD = 2
DIRECTION_OUEST = 3
DIRECTION_ATTENTE = 4

B_LIGNE = 0
B_COLONNE = 1
B_LONGUEURFLAMMES = 2
B_JOUEUR = 3

J_LIGNE = 0
J_COLONNE = 1
J_DECISION = 2
J_LONGUEURFLAMMES = 3
J_NOMBREBOMBES = 4
J_BOMBESRESTANTES = 5
J_VITESSE = 6

POWERUP_NOMBREBOMBES = 0
POWERUP_LONGUEURFLAMMES = 1
POWERUP_VITESSE = 2

PU_LIGNE = 0
PU_COLONNE = 1
PU_NATURE = 2

from random import randrange
from copy import deepcopy
from tkinter import *

def attente(vitesse):
    return TEMPS_BASE * 0.9**vitesse
    
def cree_plateau_initial(lignes, colonnes, nombreDeTrous):
    plateau = [[PLATEAU_BOIS for i in range(colonnes+2)] for j in range(lignes+2)]
    for i in range(2, lignes+1,2):
        for j in range(2, colonnes+1, 2):
            plateau[i][j]=PLATEAU_PIERRE
    for i in range(0, lignes+2):
        plateau[i][0] = PLATEAU_PIERRE
        plateau[i][-1] = PLATEAU_PIERRE
        
    for j in range(0, colonnes+2):
        plateau[0][j] = PLATEAU_PIERRE
        plateau[-1][j] = PLATEAU_PIERRE
        
    plateau[1][1] = plateau[1][2] = plateau[2][1] = PLATEAU_VIDE
    plateau[1][-2] = plateau[1][-3] = plateau[2][-2] = PLATEAU_VIDE
    plateau[-2][1] = plateau[-2][2] = plateau[-3][1] = PLATEAU_VIDE
    plateau[-2][-2] = plateau[-2][-3] = plateau[-3][-2] = PLATEAU_VIDE
    
    for i in range(nombreDeTrous):
        i,j=0,0
        while plateau[i][j] != PLATEAU_BOIS:
            i=randrange(lignes)
            j=randrange(colonnes)
        plateau[i][j] = PLATEAU_VIDE
    return plateau

def affiche_plateau(canvas, plateau, plateauCouleur, bombes, joueurs, powerups):
    canvas.delete(ALL)
    
    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if plateau[i][j]==PLATEAU_PIERRE:
                canvas.create_rectangle(j*TAILLE_TUILE, i*TAILLE_TUILE, j*TAILLE_TUILE+TAILLE_TUILE, i*TAILLE_TUILE+TAILLE_TUILE, fill="black")
            elif plateau[i][j]==PLATEAU_BOIS:
                canvas.create_rectangle(j*TAILLE_TUILE, i*TAILLE_TUILE, j*TAILLE_TUILE+TAILLE_TUILE, i*TAILLE_TUILE+TAILLE_TUILE, fill="brown")
            else:
                if plateauCouleur[i][j]!=-1:
                    couleurJoueur = COULEURS_JOUEURS[plateauCouleur[i][j]]
                    canvas.create_rectangle(j*TAILLE_TUILE, i*TAILLE_TUILE, j*TAILLE_TUILE+TAILLE_TUILE, i*TAILLE_TUILE+TAILLE_TUILE, fill=couleurJoueur, outline = couleurJoueur)
                if trouve_objet(i,j, bombes)!=None:
                    canvas.create_oval(j*TAILLE_TUILE+5, i*TAILLE_TUILE+5, j*TAILLE_TUILE+TAILLE_TUILE-5, i*TAILLE_TUILE+TAILLE_TUILE-5, fill="cyan")
                if trouve_objet(i,j, joueurs)!=None:
                    couleurJoueur = COULEURS_JOUEURS[trouve_objet(i,j, joueurs)]
                    trace_bomberman(canvas, j*TAILLE_TUILE, i*TAILLE_TUILE, couleurJoueur)
                if trouve_objet(i,j, powerups)!=None:
                    couleurPowerup = COULEURS_POWERUPS[powerups[trouve_objet(i,j, powerups)][PU_NATURE]]
                    canvas.create_polygon(j*TAILLE_TUILE+TAILLE_TUILE/2, i*TAILLE_TUILE, j*TAILLE_TUILE, i*TAILLE_TUILE+TAILLE_TUILE/2, j*TAILLE_TUILE+TAILLE_TUILE/2, (i+1)*TAILLE_TUILE, (j+1)*TAILLE_TUILE, i*TAILLE_TUILE + TAILLE_TUILE/2, fill=couleurPowerup)
    
def trace_bomberman(canvas, x, y, couleur):
    canvas.create_oval(x+15, y+15, x+TAILLE_TUILE-15, y+TAILLE_TUILE, fill=couleur)
    canvas.create_oval(x+10, y, x+TAILLE_TUILE-10, y+TAILLE_TUILE-20, fill=couleur)
    canvas.create_oval(x+13, y+5, x+TAILLE_TUILE-13, y+TAILLE_TUILE-26, fill="pink")
                    
def affiche_infos(canvas, joueurs, plateauCouleur):
    canvas.delete(ALL)
    for i in range(len(joueurs)):
        if joueurs[i]!=None:
            couleur = COULEURS_JOUEURS[i]
            j=2
            couleurPowerup = COULEURS_POWERUPS[POWERUP_NOMBREBOMBES]
            canvas.create_polygon(j*TAILLE_TUILE+TAILLE_TUILE/2, i*TAILLE_TUILE, j*TAILLE_TUILE, i*TAILLE_TUILE+TAILLE_TUILE/2, j*TAILLE_TUILE+TAILLE_TUILE/2, (i+1)*TAILLE_TUILE, (j+1)*TAILLE_TUILE, i*TAILLE_TUILE + TAILLE_TUILE/2, fill=couleurPowerup)
            canvas.create_text((j+1)*TAILLE_TUILE+TAILLE_TUILE/2, (i+0.5)*TAILLE_TUILE, text=joueurs[i][J_NOMBREBOMBES])
            j=4
            couleurPowerup = COULEURS_POWERUPS[POWERUP_LONGUEURFLAMMES]
            canvas.create_polygon(j*TAILLE_TUILE+TAILLE_TUILE/2, i*TAILLE_TUILE, j*TAILLE_TUILE, i*TAILLE_TUILE+TAILLE_TUILE/2, j*TAILLE_TUILE+TAILLE_TUILE/2, (i+1)*TAILLE_TUILE, (j+1)*TAILLE_TUILE, i*TAILLE_TUILE + TAILLE_TUILE/2, fill=couleurPowerup)
            canvas.create_text((j+1)*TAILLE_TUILE+TAILLE_TUILE/2, (i+0.5)*TAILLE_TUILE, text=joueurs[i][J_LONGUEURFLAMMES])
            
            j=6
            couleurPowerup = COULEURS_POWERUPS[POWERUP_VITESSE]
            canvas.create_polygon(j*TAILLE_TUILE+TAILLE_TUILE/2, i*TAILLE_TUILE, j*TAILLE_TUILE, i*TAILLE_TUILE+TAILLE_TUILE/2, j*TAILLE_TUILE+TAILLE_TUILE/2, (i+1)*TAILLE_TUILE, (j+1)*TAILLE_TUILE, i*TAILLE_TUILE + TAILLE_TUILE/2, fill=couleurPowerup)
            canvas.create_text((j+1)*TAILLE_TUILE+TAILLE_TUILE/2, (i+0.5)*TAILLE_TUILE, text=joueurs[i][J_VITESSE])     
        
            j=8
            canvas.create_text((j+1)*TAILLE_TUILE+TAILLE_TUILE/2, (i+0.5)*TAILLE_TUILE, text=score(plateauCouleur, i)) 
            
        else:
            couleur = "gray"
        trace_bomberman(canvas, 0, HAUTEUR_JOUEUR*i,couleur)

def score(plateauCouleur, indiceJoueur):
    score = 0
    for i in range(len(plateauCouleur)):
        for j in range(len(plateauCouleur[i])):
            if plateauCouleur[i][j] == indiceJoueur :
                score += 1
    return score

def ajoute_evenement(evenements, evenement):
    for i in range(0,len(evenements)):
        if evenement[0]<evenements[i][0]:
            evenements.insert(i,evenement)
            return
    evenements.append(evenement)
        
def prochain(i,j,direction):
    if direction == DIRECTION_NORD:
        i-=1
    elif direction == DIRECTION_SUD:
        i+=1
    elif direction == DIRECTION_OUEST:
        j-=1
    elif direction == DIRECTION_EST:
        j+=1
    return i,j

def trouve_objet(i,j, liste):
    for indice in range(len(liste)):
        if liste[indice]!=None and liste[indice][0]==i and liste[indice][1]==j:
            return indice

def casse(plateau, powerups, i,j):
    plateau[i][j]=PLATEAU_VIDE
    if randrange(0,4)==0:
        powerups.append([i,j, randrange(3)])
    return
    
def execute_evenement(evenements, evenement, plateau, plateauCouleur, bombes, joueurs, powerups):
    if evenement[E_NATURE]==EVENEMENT_TOUR_JOUEUR:
        temps, nature, indiceJoueur = evenement
        joueur = joueurs[indiceJoueur]
        if joueur == None:
            return
        i, j = joueur[J_LIGNE], joueur[J_COLONNE]

        direction,bombe = joueur[J_DECISION](indiceJoueur, deepcopy(plateau), deepcopy(plateauCouleur), deepcopy(bombes), deepcopy(joueurs), deepcopy(powerups))
            
        if joueurs[indiceJoueur][J_BOMBESRESTANTES]>0 and bombe:
            joueur[J_BOMBESRESTANTES]-=1
            bombes.append([i,j,joueur[J_LONGUEURFLAMMES],indiceJoueur])
            ajoute_evenement(evenements, [evenement[0]+TEMPS_EXPLOSION, EVENEMENT_EXPLOSION_BOMBE, len(bombes)-1])
        ip,jp = prochain(i,j,direction)
        if plateau[ip][jp]==PLATEAU_VIDE and trouve_objet(ip, jp, bombes)==None:
            joueur[J_LIGNE]=ip
            joueur[J_COLONNE]=jp
        indicePowerup = trouve_objet(i,j,powerups)
        if indicePowerup != None:
            powerup = powerups.pop(indicePowerup)
            if powerup[PU_NATURE]==POWERUP_LONGUEURFLAMMES:
                joueur[J_LONGUEURFLAMMES]+=1
            elif powerup[PU_NATURE]==POWERUP_NOMBREBOMBES:
                joueur[J_NOMBREBOMBES]+=1
                joueur[J_BOMBESRESTANTES]+=1
            elif powerup[PU_NATURE]==POWERUP_VITESSE:
                joueur[J_VITESSE]+=1
        ajoute_evenement(evenements, [temps+attente(joueur[J_VITESSE]), EVENEMENT_TOUR_JOUEUR, indiceJoueur])            
    elif evenement[E_NATURE]==EVENEMENT_EXPLOSION_BOMBE:
        temps, nature, indiceBombe = evenement
        # print("EXPLOSION")
        # print("temps", temps)
        if bombes[indiceBombe]==None:
            return
        
        
        i,j,longueurFlammes, indiceJoueur = bombes[indiceBombe]
        indJoueur = bombes[indiceBombe][B_JOUEUR]
        bombes[indiceBombe] = None
        
        for direction in [DIRECTION_NORD, DIRECTION_SUD, DIRECTION_EST, DIRECTION_OUEST]:
            ajoute_evenement(evenements, [evenement[0], EVENEMENT_PROPAGATION, i, j, direction, longueurFlammes, indJoueur])
        if joueurs[indiceJoueur]!=None:
            joueurs[indiceJoueur][J_BOMBESRESTANTES]+=1
    elif evenement[E_NATURE]==EVENEMENT_PROPAGATION:
        temps, nature, i, j, direction, longueurFlammes, indJoueur = evenement
        # print("PROPAGATION")
        # print("time", temps)
        # print("i,j", i, j)
        if plateau[i][j]==PLATEAU_PIERRE:
            # Pierre : indestuctible donc pas d'effet
            return
        elif plateau[i][j]==PLATEAU_BOIS:
            # Bois : destructible, on détruit
            casse(plateau, powerups, i,j)
            return
        else:
            # On colore la case avec la couleur du joueur
            plateauCouleur[i][j] = indJoueur
            # On détruit le powerup s'il y en a un                
            indicePowerup = trouve_objet(i,j,powerups)
            if indicePowerup != None:
                powerups.pop(indicePowerup)
                
            # On tue tous les joueurs qui sont à cet endroit
            indiceJoueur = trouve_objet(i,j,joueurs)
            while indiceJoueur != None:
                joueurs[indiceJoueur] = None
                indiceJoueur = trouve_objet(i,j,joueurs)
            
            # On fait exploser la bombe s'il y en a une
            indiceBombe = trouve_objet(i,j,bombes)            
            if indiceBombe != None:
                ajoute_evenement(evenements, [evenement[0],EVENEMENT_EXPLOSION_BOMBE, indiceBombe])
                longueurFlammes = 0
                
            # Si on est pas au bout de la flamme, on propage
            if longueurFlammes>0:
                ip, jp = prochain(i,j,direction)
                ajoute_evenement(evenements, [evenement[0]+TEMPS_PROPAGATION, EVENEMENT_PROPAGATION, ip, jp, direction, longueurFlammes-1, indJoueur])
        

TAILLE_TUILE = 40
HAUTEUR_JOUEUR = TAILLE_TUILE
LARGEUR_INFOS = 500
COULEURS_JOUEURS = ["red", "blue", "green", "yellow"]
COULEURS_POWERUPS = [ "cyan", "orangered", "yellow"]

def simulation(strategies):
    def pas_de_jeu():
        if len(joueurs) - joueurs.count(None) > 1:
            evenement = evenements.pop(0)
            execute_evenement(evenements, evenement, plateau, plateauCouleur, bombes, joueurs, powerups)
            affiche_plateau(canvas, plateau, plateauCouleur, bombes, joueurs, powerups)
            affiche_infos(canvasInfosJoueurs, joueurs,plateauCouleur)
            temps = int((evenements[0][0]-evenement[0])/3*1000)
            if temps != 0:
                fenetre.after(temps, pas_de_jeu)
            else:
                pas_de_jeu()
    dimensions = 13,21
    positionsInitiales=[(1, 1), (dimensions[0]-2, dimensions[1]-2), (1, dimensions[1]-2), (dimensions[0]-2, 1)]
    
    
    plateau = cree_plateau_initial(dimensions[0]-2, dimensions[1]-2, 20)
    plateauCouleur = [[-1 for j in range(dimensions[1])] for i in range(dimensions[0])]
    
    evenements = []
    
    bombes = []
    joueurs = []
    powerups = []
    
    fenetre = Tk()
    canvas = Canvas(width=dimensions[1]*TAILLE_TUILE, height=dimensions[0]*TAILLE_TUILE)
    canvas.pack()
    
    joueurs = []
    
    for i in range(len(strategies)):
        joueur = [positionsInitiales[i][0], positionsInitiales[i][1], strategies[i].decision, 2, 1, 1, 0]
        joueurs.append(joueur)
        ajoute_evenement(evenements, [0, EVENEMENT_TOUR_JOUEUR, i])    
    
    canvasInfosJoueurs = Canvas(width = LARGEUR_INFOS, height=len(joueurs)*HAUTEUR_JOUEUR)
    canvasInfosJoueurs.pack()
    
    pas_de_jeu()

    fenetre.mainloop()
    return 

import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__



import bomberman_strategie

simulation([bomberman_strategie, bomberman_strategie])
