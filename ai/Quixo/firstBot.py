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
            cube = AI().bestCube(power, game)
            direction = AI().bestDirection(power, game, cube)
            print("-----------------------------------")
            print("Send : X in", cube, "from", direction)
            maj = playTheGame().move(game, cube, direction, power)
            print(np.resize(maj, (5, 5)))
            print("-----------------------------------")
            return {'move' :{'cube' : cube, 'direction': direction}}

        elif first%2 == 1: #Second joueur
            power = 1
            print("Second player with: O ({}) !".format(power))
            cube = AI().bestCube(power, game)
            direction = AI().bestDirection(power, game, cube)
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
        while cube >= 0:
            if cube not in self.forbidden[dir]:
                print("Moving cube :{}...".format(cube))
                game[cube] = game[(cube)+self.increment[dir]]
                cube += self.increment[dir]
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
            if win == 5:
                return win

            if win == 4:
                return win

    def bestCube(self, power, game):
        print("Searching for the best cube...")
        jeu = game
        choice = []

        for i in self.firstList:
            if jeu[i] == None or jeu[i] == power:
                print("Try for", i)
                choice.append(i)
                y = jeu[i]
                jeu[i] = power
                
                if self.win(power, jeu) == 5:
                    print("I CHOOSE MY CUBE !")
                    return i

                jeu[i] = y

        # Bloquage de l'adversaire
        print("Trying to block...")
        if power == 1:
            otherPower = 0
        else:
            otherPower = 1

        jeuReshape = jeu.reshape(25)
        indList = np.where(jeuReshape == otherPower)
        print(indList[0])

        for l in range(len(self.gagne)):
            if len(indList & self.gagne[l]) >= 3:
                if 0 <= l <= 4:
                    pass

                elif 5 <= l <= 9:
                    pass

                else:
                    pass

                   


        return random.choice(choice)
    
    def bestDirection(self, power, game, cube):
        print("Searching for the best direction...")
        choice = []

        for i in self.firstDirections:
            if cube not in self.forbidden[i]:
                choice.append(i)
                print("TEST\n")
                jeu = playTheGame().move(game, cube, i, power)

                if self.win(power, jeu) == 5:
                    print("I CHOOSE MY DIRECTION !")
                    return i

                jeu = game
        #Bloquage de l'adversaire
        # if power == 1:
        #     power = 0
        # else:
        #     power = 1

        # for i in self.firstDirections:
        #     if cube not in self.forbidden[i]:
        #         jeu = playTheGame().move(game, cube, i, power)

        #         if self.win(power, jeu) in [4, 5]:
        #             print("I BLOCK WITH THE DIRECTION !")
        #             return i

        #         jeu = game

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