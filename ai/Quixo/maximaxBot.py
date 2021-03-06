import cherrypy
import sys
import random
import numpy as np

class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''

        body = cherrypy.request.json

        game = body["game"]
        print("")
        print("######################################")
        print("############# Smart bot #############")
        print("######################################")
        print("")
        print("--------------------------------------")
        print("State of the game :")
        print(np.resize(game, (5, 5)))
        
        first = len(body['moves'])
        for i in body['moves']:
            for j in i:
                if j == 'badMove' or j == 'timeOut':
                    first -= 1

        print("")
        print("##########", first, "move(s) #########")   
        print("--------------------------------------")
        print("")
        print("--Logs:--")
    
        winPhrases = ["Ne pas vendre la peau de l'ours avant de l'avoir tuer", "Prends-en de la graine", "Qu'on m'apporte un extincteur... Je suis on fire", "Appelle-moi quand tu seras coder !", "Quand tu m’arriveras à la cheville, tu pourras faire mes lacets", "Les gagnants trouvent des moyens et les perdants des excuses", "Tu m’as vendu du rêve j’aimerais être remboursé !", "Je suis rapide comme le guépard !", "Je vais gagner, tu vas perdre... Faut pas chercher plus loin !", "Qui s'y frotte s'y pique"]

        if first%2 == 0: #Premier joueur
            power = 0
            print("First player with: X ({}) !".format(power))
            cube, direction, phrase = AI().bestCube(power, game)
            if phrase == None:
                phrase = random.choice(winPhrases)
                winPhrases.remove(phrase)
            if cube == None and direction == None:
                print("Ca marche pas")
                cube, direction, phrase = AI().aleatoire(AI().firstList, power, game)
            print("-----------------------------------")
            print("Send : X in", cube, "from", direction)
            maj = playTheGame().move(game, cube, direction, power)
            print(np.resize(maj, (5, 5)))
            print("-----------------------------------")
            return {'move' :{'cube' : cube, 'direction': direction}, "message" : phrase}

        elif first%2 == 1: #Second joueur
            power = 1
            print("Second player with: O ({}) !".format(power))
            cube, direction, phrase = AI().bestCube(power, game)
            if phrase == None:
                phrase = random.choice(winPhrases)
                winPhrases.remove(phrase)
            if cube == None and direction == None:
                print("Ca marche pas")
                cube, direction, phrase = AI().aleatoire(AI().firstList, power, game)
            print("-----------------------------------")
            print("Send : O in", cube, "from", direction)
            maj = playTheGame().move(game, cube, direction, power)
            print(np.resize(maj, (5, 5)))
            print("-----------------------------------")
            return {'move' :{'cube' : cube, 'direction': direction}, "message" : phrase}

class playTheGame():
    def __init__(self, *args, **kwargs):
        self.increment = {'N': -5, 'S': 5, 'E': 1, 'W': -1}
        self.forbidden = {'E':[4, 9, 14, 19, 24], 'W':[0, 5, 10, 15, 20], 'N':[0, 1, 2, 3, 4], 'S':[20, 21, 22, 23, 24]}
    
    def move(self, game, cube, dir, power):
        print("\nBouge le cube : {} par le {}".format(cube, dir))
        while cube >= 0:
            if cube not in self.forbidden[dir]:
                print("Moving cube :{}...".format(cube))
                nextcube = cube+self.increment[dir]
                game[cube] = game[nextcube]
                cube = nextcube
            else :
                game[cube] = power
                return game

class AI():
    def __init__(self, *args, **kwargs):
        self.firstList = [0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23, 24]
        self.firstDirections = ['N', 'S', 'E', 'W']
        self.forbidden = {'E':[4, 9, 14, 19, 24], 'W':[0, 5, 10, 15, 20], 'N':[0, 1, 2, 3, 4], 'S':[20, 21, 22, 23, 24]}
        self.increment = {'N': -5, 'S': 5, 'E': 1, 'W': -1}
        self.gagne = [
                        [ 0,  1,  2,  3,  4],
                        [ 5,  6,  7,  8,  9],
                        [10, 11, 12, 13, 14],
                        [15, 16, 17, 18, 19],
                        [20, 21, 22, 23, 24],
                        [ 0,  5, 10, 15, 20],
                        [ 1,  6, 11, 16, 21],
                        [ 2,  7, 12, 17, 22],
                        [ 3,  8, 13, 18, 23],
                        [ 4,  9, 14, 19, 24],
                        [ 0,  6, 12, 18, 24],
                        [ 4,  8, 12, 16, 20]]

    def win(self, power, game): #Test si le jeu est gangant ou non 
        for i in range(len(self.gagne)):
            win = 0
            for j in self.gagne[i]:
                if game[j] == power:
                    win += 1
            return win

    def checkList(self, power, game, ligne):
        matrix = np.resize(game, 25)
        matrixDesIndices = np.where(matrix == power)[0]
        listeDesIndices = matrixDesIndices.tolist()
        
        a = len(self.commun(listeDesIndices, ligne))
        print("Liste des indices de {} sur la ligne {}: {}".format(power, ligne, self.commun(listeDesIndices, ligne)))
        return a
    
    def indexLongestList(self, power, game):
        maxByLine = []
        for i in range(len(self.gagne)):
            maxByLine.append(self.checkList(power, game, self.gagne[i]))
        
        maxi = max(maxByLine)
        return maxByLine.index(maxi), maxi, maxByLine

    def giveHole(self, power, game, ligne):
        matrix = np.resize(game, 25)
        matrixDesIndices = np.where(matrix == power)[0]
        listeDesIndices = matrixDesIndices.tolist()

        for i in ligne:
            if i not in listeDesIndices:
                return i

    def makeChoice(self, power, jeu):
        choice = []
        for i in range(len(self.gagne)):
            if i <= 4:
                for j in self.gagne[i]:
                    if j in self.firstList:
                        if jeu[j] == None or jeu[j] == power:
                            choice.append(j)
        print("Création d'une liste de choix... :", choice)
        return choice


    def bestCube(self, power, game):
        print("\n\nDebut de l'ia : recherche du meilleur cube...\n\n")
        jeu = game.copy()
        if power == 1:
            otherPower = 0
        else:
            otherPower = 1
        
        choice = self.makeChoice(power, jeu)

        # Gagne quand ligne de 4
        print("\nNiveau de recherche: 1\n")
        print("Essaye de voir si il y a 4 cubes alignés...")
        for i in range(len(self.gagne)):
            if self.checkList(power, jeu, self.gagne[i]) == 4:
                print("\nOn peut gagner !")
                print("Check des lignes gagnates...")
                for cube in self.firstList:
                    for direction in self.firstDirections:
                        if cube not in self.forbidden[direction] and game[cube] != otherPower:
                            won = self.checkList(power, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
                            otherWon = self.checkList(otherPower, jeu, self.gagne[i])
                            jeu = game.copy()
                            print('Cubes alignés :', won)
                            #Niveau 1 
                            if won == 5 and otherWon != 5: 
                                print("ON A GAGNE !")
                                print("Cube et dicrection trouvés : {} par {}".format(cube, direction))
                                return (cube, direction, "J'ai gagné grand fou")
                            if otherWon == 5:
                                print("!!!!!!!!!!!!!!!!!!!!!!Attention, ce coup peut avantager l'autre!!!!!!!!!!!!!!!!!!!!!!")
        
        cste = 0   
        print("\nImpossible de gagner, niveau de recherche: 2\n")
        if cste == 0:
            #Niveau 2
            niveau = self.blocage(power, game)
            if niveau == False:
                cste += 1
                print("\nImpossible de bloquer, niveau de recherche: 3\n")
            else:
                cube, direction, phrase = niveau
                return cube, direction, phrase

        if cste == 1:
            #Niveau 3
            niveau = self.notWin(power, game)
            if niveau == False:
                cste += 1
                print("\nImpossible de se rapprocher de la victoire, niveau de recherche: 4\n")
            else:
                cube, direction, phrase = niveau
                return cube, direction, phrase 

        if cste == 2:
            #Niveau 4
            niveau = self.build(power, game, choice)
            if niveau == False:
                print("\nImpossible de jouer une stratiégie!\n")
                cste += 1
            else:
                cube, direction, phrase = niveau
                return cube, direction, phrase    

        cube, direction, phrase = self.aleatoire(choice, power, game)
        return cube, direction, phrase

    def notWin(self, power, game):
        jeu = game.copy()
        choice = self.makeChoice(power, jeu)

        if power == 1:
            otherPower = 0
        else:
            otherPower = 1

        print("Tentative de se rapprocher de la victoire...")
        for i in range(len(self.gagne)):
            if self.checkList(power, jeu, self.gagne[i]) == 4:
                trou = self.giveHole(power, jeu, self.gagne[i])
                if 0 <= i <= 4:
                    newCube = trou%5
                    print("Il faut bouger par le N ou le S, le cube :", trou)
                    if jeu[self.forbidden['S'][newCube]] != otherPower and jeu[self.forbidden['N'][newCube]] != otherPower:
                        if i == 1:
                            return self.forbidden['S'][newCube], "N", "Bien essayé"
                        else:
                            return self.forbidden['N'][newCube], "S", "Bien essayé"
                    else:
                        z = 0
                        while z == 0:
                            print("Impossible de trouver le bon cube et la bonne direction !")
                            print("Génération d'un choix aléatoire qui ne casse pas notre jeu...")
                            cube, direction, phrase = self.aleatoire(choice, power, jeu)
                            won = self.indexLongestList(power, jeu)[1]
                            win = self.checkList(power, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
                            jeu = game.copy()
                            if win == won:
                                print("Cube et direction trouvés :", cube, direction)
                                z = 1
                                return cube, direction, phrase

                elif 5 <= i <= 9:
                    print("Il faut bouger par l'E ou l'W, le cube :", trou)
                    newCube = int(trou/5)
                    if jeu[self.forbidden['W'][newCube]] != otherPower and jeu[self.forbidden['E'][newCube]] != otherPower:
                        if i == 6:
                            return self.forbidden['E'][newCube], "W", "Bien essayé"
                        else:
                            return self.forbidden['W'][newCube], "E", "Bien essayé"
                    else:
                        z = 0
                        while z == 0:
                            print("Impossible de trouver le bon cube et la bonne direction !")
                            cube, direction, phrase = self.aleatoire(choice, power, jeu)
                            won = self.indexLongestList(power, jeu)[1]
                            win = self.checkList(power, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
                            jeu = game.copy()
                            if win == won:
                                print("Cube et direction trouvés :", cube, direction)
                                z = 1
                                return cube, direction, phrase

        return False
    
    def blocage(self, power, game):
        jeu = game.copy()
        if power == 1:
            otherPower = 0
        else:
            otherPower = 1

        # Bloquage de l'adversaire
        print("Tentative de blocage...")
        for i in range(len(self.gagne)):
            x = self.checkList(otherPower, jeu, self.gagne[i])
            if x == 4:
                print("L'adversaire a une suide te 4 cubes!")
                if 0 <= i <= 4:
                    print("Il faut bouger par le N ou le S")
                    a = self.forbidden["N"].copy()
                    for cube in (a + self.forbidden["S"]):
                        for direction in ["N", "S"]:
                            if cube not in self.forbidden[direction] and game[cube] != otherPower:
                                won = self.checkList(otherPower, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
                                jeu = game.copy()
                                print('Cubes alignés :', won) 
                                if won < x: 
                                    print("Blocage réussi")
                                    print("Cube et dicrection trouvés : {} par {}".format(cube, direction))
                                    return (cube, direction, None)

                    return False                    

                elif 5 <= i <= 9:
                    print("Il faut bouger par l'E ou l'W")
                    a = self.forbidden["W"].copy()
                    for cube in (a + self.forbidden["E"]):
                        for direction in ["E", "W"]:
                            if cube not in self.forbidden[direction] and game[cube] != otherPower:
                                won = self.checkList(otherPower, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
                                jeu = game.copy()
                                print('Cubes alignés :', won)
                                if won < x:
                                    print("Blocage réussi")
                                    print("Cube et dicrection trouvés : {} par {}".format(cube, direction)) 
                                    return (cube, direction, None)

                    return False
                else:
                    print("Il faut bouger par le N ou le S ou l'E ou l'W")
                    for cube in (self.firstList):
                        for direction in ["N", "S", "E", "W"]:
                            if cube not in self.forbidden[direction] and game[cube] != otherPower:
                                won = self.checkList(otherPower, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
                                jeu = game.copy()
                                print('Cubes alignés :', won)
                                if won < x: 
                                    print("Blocage réussi")
                                    print("Cube et dicrection trouvés : {} par {}".format(cube, direction))
                                    return (cube, direction, None)

                    return False
            # elif x == 3:
            #     if 0 <= i <= 4:
            #         print("N ou S")
            #         a = self.forbidden["N"].copy()
            #         for cube in (a + self.forbidden["S"]):
            #             for direction in ["N", "S"]:
            #                 if cube not in self.forbidden[direction] and game[cube] != otherPower:
            #                     won = self.checkList(otherPower, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
            #                     jeu = game.copy()
            #                     print('Won :', won) 
            #                     if won < x: 
            #                         print("Cube et dicrection trouvés : {} par {}".format(cube, direction))
            #                         return (cube, direction)
            #              return False

            #     elif 5 <= i <= 9:
            #         print("E ou W")
            #         a = self.forbidden["W"].copy()
            #         for cube in (a + self.forbidden["E"]):
            #             for direction in ["E", "W"]:
            #                 if cube not in self.forbidden[direction] and game[cube] != otherPower:
            #                     won = self.checkList(otherPower, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
            #                     jeu = game.copy()
            #                     print('Won :', won)
            #                     if won < x:
            #                         print("Cube et dicrection trouvés : {} par {}".format(cube, direction)) 
            #                         return (cube, direction)
            #         return False

            #     else:
            #         print("N ou S ou E ou W")
            #         for cube in (self.firstList):
            #             for direction in ["N", "S", "E", "W"]:
            #                 if cube not in self.forbidden[direction] and game[cube] != otherPower:
            #                     won = self.checkList(otherPower, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
            #                     jeu = game.copy()
            #                     print('Won :', won)
            #                     if won < x: 
            #                         print("Cube et dicrection trouvés : {} par {}".format(cube, direction))
            #                         return (cube, direction)
            #         return False

        return False

    def build(self, power, game, choice): # Essaye de construire
        jeu = game.copy()
        if power == 1:
            otherPower = 0
        else:
            otherPower = 1

        print("Tentative de construction d'une suite...")
        indexList, maxi, liste = self.indexLongestList(power, jeu)
        print("\nListe des nombre de {} par ligne : {}".format(power, liste))

        if maxi != 0:
            print("Il y a un maximum !")
            for cube in self.firstList:
                for direction in self.firstDirections:
                    if cube not in self.forbidden[direction] and game[cube] != otherPower:
                        won = self.checkList(power, playTheGame().move(jeu, cube, direction, power), self.gagne[indexList])
                        otherWon = self.checkList(otherPower, jeu, self.gagne[indexList])
                        jeu = game.copy()
                        print('Cubes alignés :', won) 
                        if won > maxi and otherWon != 4: 
                            print("\nConstruction de la ligne...")
                            print("Cube et dicrection trouvés : {} par {}".format(cube, direction))
                            return (cube, direction, None)
            z = 1
            print("z")
            while z != 0:
                z += 1
                print("Imossible de trouver un cube !")
                cube, direction, phrase = self.aleatoire(choice, power, jeu)
                win = self.checkList(power, playTheGame().move(jeu, cube, direction, power), self.gagne[indexList])
                jeu = game.copy()
                if win == won:
                    print("Cube est direction trouvés :", cube, direction)
                    z = 0
                    return cube, direction, phrase
                if z == 500:
                    print("Ca tourne en boucle!")
                    z = 0
                    return False

        else:
            print("Pas de maximum, le jeu vient de commencer !")
            return False

    def aleatoire(self, choice, power, game):
        print("Generation d'un coup aléatoire...")
        jeu = game.copy()
        print("Choix dans la liste : ", choice)
        cube = random.choice(choice)
        if game[cube] == power or game[cube] == None:
            print("Choix d'un cube... :", cube)
            direction = self.bestDirection(power, jeu, cube)
            print("Choix d'une direction en fonction du cube... :", direction)
            return (cube, direction, "Coup aléatoire...")

    def bestDirection(self, power, game, cube):
        print("Searching for the best direction...")
        jeu = np.copy(game)
        choice = []

        for i in self.firstDirections:
            if cube not in self.forbidden[i]:
                choice.append(i)
                newJeu = playTheGame().move(jeu, cube, i, power)

                if self.win(power, newJeu) == 5:
                    print("Direction trouvée !")
                    return i
                
                else: 
                    print("Pas de direction privilégiée !")
                    jeu = np.copy(game)

        return random.choice(choice)

    def commun(self, a, b):
        l = []
        for i in a:
            if i in b:
                l.append(i)
        return l

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())