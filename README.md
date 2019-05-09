# AI-Quixo

## Strategy

A chaque coups, l'IA a un chemin de réflexion : 

1. Analyse si le bot peut gagner : 
    - Si oui : Application du mouvement gagnant
    - Si non : Poursuite du chemin de reflexion (étape 2.)
2. Analyse si l'adversaire peut gagner au coup suivant : 
    - Si oui : 
        * Analyse des coups brisant sa suite de symboles
        * Application du mouvement de blocage
    - Si non : Poursuite du chemin de reflexion (étape 3.)
3. Tentative de développement du jeu personnel :
    - Si 1er coup : Mouvement alléatoire
    - Sinon : Tentative de développement de la plus grande chaine de symbole
    
## Location   

The python script's location : `/ai/smartBot.py`

## Students

Guillaume Caestecker "*@Arkhesus*" (17036) & Guillaume Bouillon "*@Guigxs*" (17076)
