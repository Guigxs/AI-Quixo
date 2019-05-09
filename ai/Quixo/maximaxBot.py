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


        if first%2 == 0: #Premier joueur
            power = 0
            print("First player with: X ({}) !".format(power))
            cube, direction = AI().bestCube(power, game)
            print("-----------------------------------")
            print("Send : X in", cube, "from", direction)
            maj = playTheGame().move(game, cube, direction, power)
            print(np.resize(maj, (5, 5)))
            print("-----------------------------------")
            return {'move' :{'cube' : cube, 'direction': direction}}

        elif first%2 == 1: #Second joueur
            power = 1
            print("Second player with: O ({}) !".format(power))
            cube, direction = AI().bestCube(power, game)
            print("-----------------------------------")
            print("Send : O in", cube, "from", direction)
            maj = playTheGame().move(game, cube, direction, power)
            print(np.resize(maj, (5, 5)))
            print("-----------------------------------")
            return {'move' :{'cube' : cube, 'direction': direction}}

class playTheGame():
    def __init__(self, *args, **kwargs):
        self.increment = {'N': -5, 'S': 5, 'E': 1, 'W': -1}
        self.forbidden = {'E':[4, 9, 14, 19, 24], 'W':[0, 5, 10, 15, 20], 'N':[0, 1, 2, 3, 4], 'S':[20, 21, 22, 23, 24]}
    
    def move(self, game, cube, dir, power):
        print("Bouge le cube : {} par le {}".format(cube, dir))
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

    def bestCube(self, power, game):
        print("Searching for the best cube..\n.")
        jeu = game.copy()
        choice = []
        if power == 1:
            otherPower = 0
        else:
            otherPower = 1

        for i in range(len(self.gagne)):
            # Gagne quand ligne de 4
            if self.checkList(power, jeu, self.gagne[i]) == 4:
                print("On peut gagner !")
                print("Check des lignes gagnates...")
                for cube in self.firstList:
                    for direction in self.firstDirections:
                        if cube not in self.forbidden[direction] and game[cube] != otherPower:
                            won = self.checkList(power, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
                            jeu = game.copy()
                            print('Won :', won) 
                            if won == 5: 
                                print("ON A GAGNE !")
                                print("Cube et dicrection trouvés : {} par {}".format(cube, direction))
                                return (cube, direction)
            else:
                print("On ne peut pas ganger mtn")
                if i <= 4:
                    for j in self.gagne[i]:
                        if j in self.firstList:
                            if jeu[j] == None or jeu[j] == power:
                                choice.append(j)
                print(choice)

        for i in range(len(self.gagne)):
            # Bloquage de l'adversaire
            print("Trying to block...\n")
            x = self.checkList(otherPower, jeu, self.gagne[i])
            if x == 4:
                if 0 <= i <= 4:
                    print("N ou S")
                    a = self.forbidden["N"].copy()
                    for cube in (a + self.forbidden["S"]):
                        for direction in ["N", "S"]:
                            if cube not in self.forbidden[direction] and game[cube] != otherPower:
                                won = self.checkList(otherPower, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
                                jeu = game.copy()
                                print('Won :', won) 
                                if won < x: 
                                    print("Cube et dicrection trouvés : {} par {}".format(cube, direction))
                                    return (cube, direction)

                elif 5 <= i <= 9:
                    print("E ou W")
                    a = self.forbidden["W"].copy()
                    for cube in (a + self.forbidden["E"]):
                        for direction in ["E", "W"]:
                            if cube not in self.forbidden[direction] and game[cube] != otherPower:
                                won = self.checkList(otherPower, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
                                jeu = game.copy()
                                print('Won :', won)
                                if won < x:
                                    print("Cube et dicrection trouvés : {} par {}".format(cube, direction)) 
                                    return (cube, direction)

                else:
                    print("N ou S ou E ou W")
                    for cube in (self.firstList):
                        for direction in ["N", "S", "E", "W"]:
                            if cube not in self.forbidden[direction] and game[cube] != otherPower:
                                won = self.checkList(otherPower, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
                                jeu = game.copy()
                                print('Won :', won)
                                if won < x: 
                                    print("Cube et dicrection trouvés : {} par {}".format(cube, direction))
                                    return (cube, direction)
            # elif x == 3:
            #     if 0 <= i <= 4:
            #         print("N ou S")
            #         a = self.forbidden["N"].copy()
            #         for cube in (a + self.forbidden["S"]):
            #             for direction in ["N", "S"]:
            #                 if cube not in self.forbidden[direction] and game[cube] != otherPower:
            #                     won = self.checkList(otherPower, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
            #                     print('Won :', won) 
            #                     if won < x: 
            #                         print("Cube et dicrection trouvés : {} par {}".format(cube, direction))
            #                         return (cube, direction)

            #     elif 5 <= i <= 9:
            #         print("E ou W")
            #         a = self.forbidden["W"].copy()
            #         for cube in (a + self.forbidden["E"]):
            #             for direction in ["E", "W"]:
            #                 if cube not in self.forbidden[direction] and game[cube] != otherPower:
            #                     won = self.checkList(otherPower, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
            #                     print('Won :', won)
            #                     if won < x:
            #                         print("Cube et dicrection trouvés : {} par {}".format(cube, direction)) 
            #                         return (cube, direction)

            #     else:
            #         print("N ou S ou E ou W")
            #         for cube in (self.firstList):
            #             for direction in ["N", "S", "E", "W"]:
            #                 if cube not in self.forbidden[direction] and game[cube] != otherPower:
            #                     won = self.checkList(otherPower, playTheGame().move(jeu, cube, direction, power), self.gagne[i])
            #                     print('Won :', won)
            #                     if won < x: 
            #                         print("Cube et dicrection trouvés : {} par {}".format(cube, direction))
            #                         return (cube, direction)

        # Essaye de construire
        print("Essaye de construire\n")
        indexList, maxi, liste = self.indexLongestList(power, jeu)
        print("Liste des nombre de {} par ligne : {}".format(power, liste))

        if maxi != 0:
            print("Maxi diff de 0")
            for cube in self.firstList:
                for direction in self.firstDirections:
                    if cube not in self.forbidden[direction] and game[cube] != otherPower:
                        won = self.checkList(power, playTheGame().move(jeu, cube, direction, power), self.gagne[indexList])
                        jeu = game.copy()
                        print('Won :', won) 
                        if won > maxi: 
                            print("La ligne se construit")
                            print("Cube et dicrection trouvés : {} par {}".format(cube, direction))
                            return (cube, direction)
        else:
            cube = random.choice(choice)
            print("Random cube...", cube)
            direction = self.bestDirection(power, jeu, cube)
            print("Chox d'une direction random en fonction du cube :", direction)
            return (cube, direction)
    
    def bestDirection(self, power, game, cube):
        print("Searching for the best direction...")
        jeu = np.copy(game)
        choice = []

        for i in self.firstDirections:
            if cube not in self.forbidden[i]:
                choice.append(i)
                print("TEST\n")
                newJeu = playTheGame().move(jeu, cube, i, power)

                if self.win(power, newJeu) == 5:
                    print("I CHOOSE MY DIRECTION !")
                    return i
                
                else: 
                    print("Pas de best direction")
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

    cherrypy.config.update({'server.socket_port': port})
    cherrypy.quickstart(Server())