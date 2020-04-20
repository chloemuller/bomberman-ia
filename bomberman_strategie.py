import random
from copy import deepcopy

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

POWERUP_NOMBREBOMBES = 1
POWERUP_LONGUEURFLAMMES = 2
POWERUP_VITESSE = 3

PU_LIGNE = 0
PU_COLONNE = 1
PU_NATURE = 2


plateauDanger = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

anciennes_bombes = []


def decision(indiceJoueur, plateau, plateauCouleur, bombes_avec_none, joueurs, powerups):
    global plateauDanger
    global anciennes_bombes
    #les bombes qui ont explosées disparaissent de la liste bombe au lieu de devenir des None
    bombes = format_bombe(bombes_avec_none)
    update_plateauDanger(plateau, bombes)
    anciennes_bombes = bombes
  
    i = joueurs[indiceJoueur][J_LIGNE]
    j = joueurs[indiceJoueur][J_COLONNE]
    
    #On commence par vérifier que le joueur est en sécurité
    #Si c'est dangereux :
    if est_dangereuse(i,j,bombes,plateau) == True : 
        destination = [0,0]
        fuite_possible, destination[0], destination[1] = closer_safe_case(indiceJoueur,joueurs,plateau, bombes)
        #Et qu'il peut fuir : 
        if fuite_possible : 
            trajet = meilleur_chemin(indiceJoueur, joueurs, plateau, bombes, destination)
            #Il le fait
            return direction_de_case(indiceJoueur, joueurs, trajet[-2]), False
        #Sinon il attend en espérant que les choses s'améliorent
        else : 
            return DIRECTION_ATTENTE, False
    #Si ce n'est pas dangereux : 
    else :
        #On regarde s'il n'y a pas un powerups a proximité et on va le chercher si oui
        if closest_powerups(indiceJoueur, joueurs, plateau, bombes, powerups)[0] == True : 
            boolean, ipu, jpu = closest_powerups(indiceJoueur, joueurs, plateau, bombes, powerups)
            trajet = meilleur_chemin(indiceJoueur,joueurs,plateau,bombes,[ipu, jpu])
            if trajet_est_safe(trajet,bombes,plateau) == True :
                return direction_de_case(indiceJoueur, joueurs, trajet[-2]), False
        #Sinon on regarde la case sur laquelle il est le plus interessant de poser une bombe 
        meilleure_case = case_utile_atteignable(indiceJoueur, joueurs, plateau, plateauCouleur, bombes)
        #Si on est sur cette case
        if meilleure_case == [i,j] : 
            #Même si normalement c'est déjà vérifié : est-ce que c'est vraiment sécuritaire pour nous de poser une bombe ? 
            bombes_fictives = deepcopy(bombes)
            bombes_fictives.append([i,j,joueurs[indiceJoueur][J_LONGUEURFLAMMES], indiceJoueur])
            #Si oui :
            if closer_safe_case(indiceJoueur,joueurs,plateau, bombes_fictives)[0] == True :
                #Le joueur pose sa bombe et commence à fuir
                securite, i_securite, j_securite = closer_safe_case(indiceJoueur,joueurs,plateau, bombes_fictives)
                trajet = meilleur_chemin(indiceJoueur,joueurs,plateau,bombes_fictives,[i_securite, j_securite])
                if trajet_est_safe(trajet,bombes,plateau) == True :
                    if case_utile(i,j, indiceJoueur, joueurs, plateau, plateauCouleur, bombes) > 0 : 
                        return direction_de_case(indiceJoueur, joueurs, trajet[-2]), True
        else : 
            #Et si on est pas sur la meilleure case on se dirige vers elle
            trajet = meilleur_chemin(indiceJoueur, joueurs, plateau, bombes, meilleure_case)
            if trajet_est_safe(trajet,bombes,plateau) == True :
                return direction_de_case(indiceJoueur, joueurs, trajet[-2]), False
        #Si le trajet jusqu'à la meilleure case est dangereux on laisse le joueur se déplacer au hasard sur des cases non dandereuses
        ListeDirectionsPossibles = directions_possibles(i,j,plateau,bombes)
        ListeDirectionsPossibles.append(DIRECTION_ATTENTE)
        for direction in ListeDirectionsPossibles : 
            if est_dangereuse(suivante(i,j,direction)[0], suivante(i,j,direction)[1], bombes, plateau) == False : 
                return direction, False


def suivante(i,j,direction):
    if direction == DIRECTION_NORD:
        return i-1, j
    if direction == DIRECTION_EST:
        return i, j+1
    if direction == DIRECTION_SUD:
        return i+1, j
    if direction == DIRECTION_OUEST:
        return i, j-1
    if direction == DIRECTION_ATTENTE:
        return i, j

def a_une_bombe(i,j,bombes):
    if bombes == []:
        return False, 0
    for bomb in bombes : 
        if bomb[B_LIGNE] == i and bomb[B_COLONNE]==j : 
            return True, bomb[B_LONGUEURFLAMMES]
    return False, 0


def directions_possibles(i,j,plateau,bombes):
    """donne les directions dans lesquelles on peut se déplacer à partir de la case i, j
    prend en compte qu'on ne peut pas marcher sur une bombe
    ne propose pas d'attendre"""
    L = [DIRECTION_NORD, DIRECTION_EST, DIRECTION_SUD, DIRECTION_OUEST]
    D = []
    for direction in L : 
        iprime = suivante(i,j,direction)[0]
        jprime = suivante(i,j,direction)[1]
        if plateau[iprime][jprime] == PLATEAU_VIDE and a_une_bombe(iprime,jprime,bombes)[0] == False:
            D.append(direction)
    random.shuffle(D)
    return D


def est_dangereuse(i,j,bombes,plateau):
    iinitial = i 
    jinitial = j 
    if bombes == [] : 
        return False
    if a_une_bombe(i,j, bombes)[0] == True : 
        return True
    ListeFlammes = []
    for bomb in bombes : 
        ListeFlammes.append(bomb[B_LONGUEURFLAMMES])
    FlammeMax = max(ListeFlammes)
    L = [DIRECTION_NORD, DIRECTION_EST, DIRECTION_SUD, DIRECTION_OUEST]
    D = []
    for direction in L : 
        iprime = suivante(i,j,direction)[0]
        jprime = suivante(i,j,direction)[1]
        if plateau[iprime][jprime] == PLATEAU_VIDE :
            D.append(direction)   
    for direction in D :
        k = 0
        i = iinitial
        j = jinitial
        stop = False
        while k <= FlammeMax and not stop : 
            if plateau[suivante(i,j,direction)[0]][suivante(i,j,direction)[1]] != 0 : 
                stop = True
            if a_une_bombe(suivante(i,j,direction)[0], suivante(i,j,direction)[1], bombes)[0] == True : 
                longueur_de_flamme = a_une_bombe(suivante(i,j,direction)[0], suivante(i,j,direction)[1], bombes)[1] 
                if k <= longueur_de_flamme : 
                    return True 
            k += 1 
            i,j = suivante(i,j,direction)
    return False



#On définit les frontières sur le modèle suivant : front = [[i1,j1], [i2,j2], [i3,j3]]

def creer_map(indiceJoueur, plateau,joueurs) : 
    """fonction qui crée une copie du labyrinthe dans laquelle on met des ∞ (codé par des -1) partout, sauf
à l’endroit du personnage où on met un 0."""
    map = deepcopy(plateau)
    for i in range(len(map)):
        for j in range(len(map[i])):
            map[i][j] = -1
    map[joueurs[indiceJoueur][J_LIGNE]][joueurs[indiceJoueur][J_COLONNE]] = 0 
    return map



def front_sup(front, map, plateau,bombes): 
    front_superieure = []
    for case in front : 
        liste_direction = directions_possibles(case[0], case[1], plateau, bombes)
        for direction in liste_direction : 
            front_superieure.append([suivante(case[0], case[1], direction)[0], suivante(case[0], case[1], direction)[1]])
    #ATTENTION, si on fait remove directement les cases de front_superieure alors qu'on fait un for sur les éléments de front_superieure alors on oublie d'en supprimer la moitié
    front_sans_double = []
    for case in front_superieure : 
        if map[case[0]][case[1]] == -1 : 
            if case not in front_sans_double : 
                front_sans_double.append(case)
    random.shuffle(front_sans_double)
    return front_sans_double





#On met destination sous la forme : destination = [ObjectifI, ObjectifJ]
def meilleur_chemin(indiceJoueur, joueurs, plateau, bombes, destination):
    """renvoie None si la destination n'es pas atteignable
    renvoie le trajet jusqu'à la destination sinon
    avec trajet = [[case 0], [case 1], [destination]]"""
    global plateauDanger
    map = creer_map(indiceJoueur, plateau,joueurs)
    i = joueurs[indiceJoueur][J_LIGNE]
    j = joueurs[indiceJoueur][J_COLONNE]
    front = front_sup([[i,j]], map, plateau,bombes)
    count = 0
    while destination not in front :
        if front == [] : 
            return None
        count += 1 
        for case in front :
            if map[case[0]][case[1]] == -1 :
                map[case[0]][case[1]] = count
        front = front_sup(front, map, plateau, bombes)
    count += 1
    trajet = [destination]
    while [i,j] not in trajet : 
        case_étudiée= [trajet[-1][0], trajet[-1][1]]
        #On remplace bombes par [] parce qu'au moment ou on essaye de retracer le chemin entre la case safe et la case ou on est une bombe fictive est posée là ou on est donc la case est considérée comme innateignable et le trajet n'abouti jamais
        D = directions_possibles(case_étudiée[0], case_étudiée[1], plateau, [])
        longueur_trajet = len(trajet)
        while len(trajet) == longueur_trajet :
            danger = "infini"
            for direction in D : 
                case_suivante_i, case_suivante_j = suivante(trajet[-1][0], trajet[-1][1], direction)
                if map[case_suivante_i][case_suivante_j] == count - 1 :
                    if danger == "infini" or danger > plateauDanger[case_suivante_i][case_suivante_j]:
                        trajet.append([case_suivante_i, case_suivante_j])
            count -= 1
    return trajet
    


def format_bombe(bombes_avec_none):
    """Cette fonction transforme la liste de bombes qui nous est transmise de manière à ce que les bombes qui ont explosées ne soient plus marquées par des none et n'apparaissent tout simplement plus"""
    bombes = deepcopy(bombes_avec_none)
    while None in bombes : 
        bombes.remove(None)
    return bombes



def closer_safe_case(indiceJoueur, joueurs, plateau, bombes):
    map = creer_map(indiceJoueur, plateau,joueurs)
    i = joueurs[indiceJoueur][J_LIGNE]
    j = joueurs[indiceJoueur][J_COLONNE]
    front = front_sup([[i,j]], map, plateau,bombes)
    count = 0
    while front != [] :
        count += 1 
        for case in front :
            if est_dangereuse(case[0], case[1], bombes, plateau) == False : 
                map[case[0]][case[1]] = count
                return True, case[0], case[1]
            else : 
                map[case[0]][case[1]] = count
        front = front_sup(front, map, plateau, bombes)
    return False, None, None



def direction_de_case(indiceJoueur, joueurs, destination):
    """permet de trouver la direction à renvoyer à partir de l'indice d'une case adjacente sur laquelle on veut se diriger"""
    i_joueurs = joueurs[indiceJoueur][J_LIGNE]
    j_joueurs = joueurs[indiceJoueur][J_COLONNE]
    i_destination = destination[0]
    j_destination = destination[1]
    direction = None
    if i_joueurs - i_destination == 1 : 
        direction = DIRECTION_NORD
    if i_joueurs - i_destination == -1 : 
        direction = DIRECTION_SUD
    if j_joueurs - j_destination == -1 and direction == None :
        direction = DIRECTION_EST
    if j_joueurs - j_destination == 1 and direction == None :
        direction = DIRECTION_OUEST
    return direction

def trajet_est_safe(trajet, bombes, plateau):
    for case in trajet : 
        i = case[0]
        j = case[1]
        if est_dangereuse(i, j, bombes, plateau) == True : 
            return False
    return True


def case_utile(i,j, indiceJoueur, joueurs, plateau, plateauCouleur,bombes):
    """Attribue à la case un nombre représentant son interet"""
    feu = joueurs[indiceJoueur][J_LONGUEURFLAMMES]
    interet = 0
    if plateauCouleur[i][j] == -1 :
        interet += 2
    if plateauCouleur[i][j] >= 0 and plateauCouleur[i][j] != indiceJoueur : 
        interet += 3 
    L = [DIRECTION_NORD, DIRECTION_EST, DIRECTION_SUD, DIRECTION_OUEST]
     #On enregistre dans les variables iinitial et jinitial les coordonnées de la case dont on mesure l'utilité
    iinitial = i 
    jinitial = j
    #La variable stop s'enclenchera lorsqu'on rencontre un mur de bois ou de pierre (ça ne sert à rien d'explorer plus loin dans cette direction)
    for direction in L : 
        i = iinitial
        j = jinitial
        count = 0 
        stop = False
        while count < feu and not stop : 
            iprime, jprime = suivante(i,j,direction)
            if 0 < iprime and 0 < jprime and iprime < len(plateau)-1 and jprime < len(plateau[i])-1:
                if plateau[iprime][jprime] != PLATEAU_VIDE : 
                    stop = True
                    #Détruire une case de bois permet de libérer du terrain à colorer et parfois de révéler des power ups, d'où l'intérêt de 1
                    if plateau[iprime][jprime] == PLATEAU_BOIS :
                        interet += 1 
                else :
                    #Si on colore une case vide, l'intéret est de 2
                    if plateauCouleur[iprime][jprime] == -1 :
                        interet += 2
                    #Si on colore une case déjà colorée par un autre joueur, l'intéret est de 3 puisqu'on handicape l'autre joueur
                    if plateauCouleur[iprime][jprime] >= 0 and plateauCouleur[iprime][jprime] != indiceJoueur : 
                        interet += 3 
            i, j = iprime, jprime
            count += 1 
    return interet
    
    

def case_utile_atteignable(indiceJoueur, joueurs, plateau, plateauCouleur, bombes):
    map = creer_map(indiceJoueur, plateau,joueurs)
    plateau_utile = deepcopy(map)
    i_joueur = joueurs[indiceJoueur][J_LIGNE]
    j_joueur = joueurs[indiceJoueur][J_COLONNE]
    bombes_fictives = deepcopy(bombes)
    bombes_fictives.append([i_joueur, j_joueur, joueurs[indiceJoueur][J_LONGUEURFLAMMES], indiceJoueur])
    if closer_safe_case(indiceJoueur,joueurs, plateau, bombes_fictives)[0] == True :
        plateau_utile[i_joueur][j_joueur] = case_utile(i_joueur,j_joueur, indiceJoueur, joueurs, plateau, plateauCouleur, bombes)
    front = front_sup([[i_joueur,j_joueur]], plateau_utile, plateau,bombes)
    count = 0
    while front != [] :
        count += 1 
        for case in front :
            # On crée un "joueur fictif" sur la case à étudier pour vérifier que le joueur peut s'échapper s'il veut poser une bombe là bas
            joueurs_fictif = deepcopy(joueurs)
            joueurs_fictif[indiceJoueur][J_LIGNE] = case[0]
            joueurs_fictif[indiceJoueur][J_COLONNE] = case[1]
            bombes_fictives = deepcopy(bombes)
            bombes_fictives.append([joueurs_fictif[indiceJoueur][J_LIGNE],joueurs_fictif[indiceJoueur][J_COLONNE],joueurs_fictif[indiceJoueur][J_LONGUEURFLAMMES], indiceJoueur])
            if closer_safe_case(indiceJoueur,joueurs_fictif,plateau, bombes_fictives)[0] == True : 
                map[case[0]][case[1]] = count
                plateau_utile[case[0]][case[1]] = case_utile(case[0], case[1], indiceJoueur, joueurs, plateau, plateauCouleur, bombes)
            else : 
                #Permet à la frontière de détecter que la case a déjà été explorée (et n'est juste pas valide)
                plateau_utile[case[0]][case[1]] = -2
        front = front_sup(front, plateau_utile, plateau, bombes)
    classement = classement_interet(plateau_utile, map)
    meilleure_case = classement[0][2]
    distance_meilleure_case = classement[0][1]
    cardinal = len(classement)
    #On examinera seulement le top pourcent% du classement environ
    nombre_bombes = joueurs[indiceJoueur][J_NOMBREBOMBES]
    pourcent = pourcentage(nombre_bombes)
    top = int(cardinal * pourcent) +1 
    #Et dans ce top on prendra la case la plus proche
    for count in range(top):
        if distance_meilleure_case > classement[count][1] : 
            distance_meilleure_case = classement[count][1]
            meilleure_case = classement[count][2]
    return meilleure_case


def pourcentage(nombre_bombes):
    #Basé sur des tests cette formule semblait arbitrairement appropriée
    a = 6
    if nombre_bombes > a : 
        return 0.5
    else : 
        return (1/100) * ((25/(a-1)) * nombre_bombes + 25*((a-2)/(a-1)))


def classement_interet(plateau_utile, map):
    classement = []
    for i in range(len(plateau_utile)):
        for j in range(len(plateau_utile[i])):
            #On ne séléctionne que les cases qui ont un interêt : ni celles qui sont innateignables (-1) ou dangereuses de poser une bombe dessus (-2)
            if plateau_utile[i][j] >= 0 :
                classement.append([-1 * plateau_utile[i][j], map[i][j], [i, j] ])
    classement.sort()
    for i in range(len(classement)):
        classement[i][0] = -1 * classement[i][0]
    #On renvoie une liste des cases de la forme : [interet, distance, coordonnées] triées par interet décroissant et sous triées par distance croissante
    return classement
    


def closest_powerups(indiceJoueur, joueurs, plateau, bombes, powerups):
    map = creer_map(indiceJoueur, plateau, joueurs)
    i = joueurs[indiceJoueur][J_LIGNE]
    j = joueurs[indiceJoueur][J_COLONNE]
    front = front_sup([[i,j]], map, plateau,bombes)
    count = 0
    while front != [] :
        count += 1 
        for case in front :
            if est_dangereuse(case[0], case[1], bombes, plateau) == False : 
                map[case[0]][case[1]] = count
            else : 
                map[case[0]][case[1]] = count
        front = front_sup(front, map, plateau, bombes)
    for power in powerups :
        ipu = power[PU_LIGNE]
        jpu = power[PU_COLONNE]
        #La valeur doit être strictement supérieure à 0 pour ignorer les cases -1 non accessible et la case sur laquelle on est présentement (le powerups est pris lorsqu'on quitte cette case)
        if map[ipu][jpu] > 0 and map[ipu][jpu] <= 6 :
            return True, ipu, jpu
    return False, None, None





def update_plateauDanger(plateau, bombes):
    global plateauDanger
    global anciennes_bombes
   #On définit bombes_nouvelles quoi qu'il arrive pour que le for bomb un bombes_nouvelles ait un sens quoi qu'il en soit
    bombes_nouvelles = []
    #Si les bombes ont évoluées :
    if anciennes_bombes != bombes : 
        #On trie les bombes : explosées, celles qui étaient déjà là, et les nouvelles
        bombes_a_retirer = []
        #Les bombes a retirer sont celles qui sont dans anciennes_bombes et pas dans bombes 
        for bomb in anciennes_bombes : 
            if bomb != None : 
                if bomb not in bombes : 
                    bombes_a_retirer.append(bomb)
        #Les bombes nouvelles sont celles qui sont dans bombes mais pas dans anciennes_bombes 
        for bomb in bombes : 
            if bomb != None : 
                if bomb not in anciennes_bombes : 
                    bombes_nouvelles.append(bomb)
        #Les bombes qui étaient déjà là au tour précedent sont les bombes actuelles moins les bombes nouvelles
        bombes = format_bombe(bombes)
        bombes_deja_la = deepcopy(bombes)
        for bomb in bombes : 
            if bomb in bombes_nouvelles : 
                bombes_deja_la.remove(bomb)
        #Maintenant que toutes nos bombes sont categorisées, on retire le danger des bombes qui ont explosées
        for bomb in bombes_a_retirer : 
            retirer_bombe(plateau, bomb)
        #Et comme parfois le danger se superpose, on rajoute le "danger sous jacent" qui n'était pas prioritaire
        for bomb in bombes_deja_la : 
            check_bombes_deja_la(plateau, bomb)
    #Même si la quantité de bombe n'a pas évolué, le niveau de danger augmente pour tout le monde : 
    for i in range(len(plateauDanger)):
        for j in range(len(plateauDanger[i])):
            if plateauDanger[i][j] != 0 : 
                plateauDanger[i][j] += 1 
    #Puis on rajoute les nouvelles bombes
    for bomb in bombes_nouvelles : 
        check_bombes_deja_la(plateau, bomb)
    


def check_bombes_deja_la(plateau, bomb):
    global plateauDanger
    global anciennes_bombes
    iinitial = bomb[B_LIGNE]
    jinitial = bomb[B_COLONNE]
    flamme = bomb[B_LONGUEURFLAMMES]
    danger = plateauDanger[iinitial][jinitial]
    if danger == 0 : 
        danger = 1
    D = directions_possibles(iinitial, jinitial, plateau, [])
    for direction in D :     
        k = 0
        i = iinitial
        j = jinitial
        stop = False
        while k <= flamme and not stop : 
            if plateau[suivante(i,j,direction)[0]][suivante(i,j,direction)[1]] != 0 : 
                stop = True
            if plateauDanger[i][j] == 0 : 
                plateauDanger[i][j] = danger
            k += 1 
            i,j = suivante(i,j,direction)
    return False
    
def retirer_bombe(plateau, bomb):
    global plateauDanger
    global anciennes_bombes
    iinitial = bomb[B_LIGNE]
    jinitial = bomb[B_COLONNE]
    flamme = bomb[B_LONGUEURFLAMMES]
    danger = plateauDanger[iinitial][jinitial]
    D = directions_possibles(iinitial, jinitial, plateau, [])
    for direction in D : 
        k = 0 
        i = iinitial
        j = jinitial
        stop = False
        while k <= flamme and not stop : 
            if plateau[suivante(i,j,direction)[0]][suivante(i,j,direction)[1]] != 0 : 
                stop = True
            if plateauDanger[suivante(i,j,direction)[0]][suivante(i,j,direction)[1]] == danger : 
                plateauDanger[suivante(i,j,direction)[0]][suivante(i,j,direction)[1]] = 0 
            k += 1 
            i,j = suivante(i,j,direction)
    plateauDanger[iinitial][jinitial] = 0 
    return False
