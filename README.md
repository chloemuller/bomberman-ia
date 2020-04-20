# Bomberman - Intelligence artificielle 



Ce projet provient d'un devoir d'informatique pour tous en classe préparatoire. Le jeu dans lequel évoluent les intelligences artificiels (fichier bomberman-simulation.py) était fourni par notre professeur (Laurent Jospin), nous devions chacun écrire un fichier bomberman_strategie.py. 

## Description du jeu 

_Le texte suivant est extrait du sujet du devoir_

Le jeu se joue usuellement par des déplacements quasi-continus dans l’espace discret en actionnant les touches directionnelles du clavier puis en déposant une bombe dans l’espace discret produisant des déflagrations en croix détruisant ainsi les cases en bois et les concurrents. Le personnage peut également ramassé des PowerUps – des bonus – lui permettant d’augmenter la longueur des déflagrations, le nombre de bombes qu’il peut disposer simultanément ou la vitesse de son personnage.
Nous jouerons à la variante du jeu appelée conquête de territoire : Chaque fois qu’une déflagration atteint une case vide du plateau, celle-ci est attribuée au joueur qui a posé la bombe. A la fin du temps, le joueur qui a revendiqué le plus de cases a gagné.
Les déplacements, normalement continus, ont été discrétisés par une méthode dite de simulation à événements discrets. Ainsi le jeu progresse de façon discrète au travers d’événements de différentes natures : explosion de bombe, propagation de la déflagration, ou tour d’un joueur. Plus la vitesse d’un joueur est importante plus l’événement correspondant se produit à intervalle rapproché.

## Détails

Ici lancer le fichier bomberman_stratégie.py lance un combat entre deux joueurs codés par l'IA bomberman_strategie.py
