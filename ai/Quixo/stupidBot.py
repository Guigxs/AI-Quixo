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
        print("############# Stupid bot #############")
        print("######################################")
        print("")
        print("--------------------------------------")
        print("State of the game :")
        print(np.resize(game, (5, 5)))
        
        first = len(body['moves'])

        print("")
        print("##########", first, "move(s) #########")   
        print("--------------------------------------")
        print("")
        print("--Logs:--")


        if first%2 == 0: #Premier joueur
            power = 0
            choice = AI().makeChoice(power, game)
            print("Liste des choix :", choice)
            print("First player with: X ({}) !".format(power))
            cube = AI().cube(power, game, choice)
            direction = AI().direction(power, game, cube)
            print("-----------------------------------")
            print("Send : X in", cube, "from", direction)
            print("-----------------------------------")
            return {'move' :{'cube' : cube, 'direction': direction}}

        elif first%2 == 1: #Second joueur
            power = 1
            choice = AI().makeChoice(power, game)
            print("Liste des choix :", choice)
            print("Second player with: O ({}) !".format(power))
            cube = AI().cube(power, game, choice)
            direction = AI().direction(power, game, cube)
            print("-----------------------------------")
            print("Send : O in", cube, "from", direction)
            print("-----------------------------------")
            return {'move' :{'cube' : cube, 'direction': direction}}

class AI():
    def __init__(self, *args, **kwargs):
        self.firstList = [0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23, 24]
        self.firstDirections = ['N', 'S', 'E', 'W']
        self.forbidden = {'E':[4, 9, 14, 19, 24], 'W':[0, 5, 10, 15, 20], 'N':[0, 1, 2, 3, 4], 'S':[20, 21, 22, 23, 24]}

    def makeChoice(self, power, game):
        choice = []
        for i in range(len(game)):
            if i in self.firstList:
                if game[i] == power or game[i] == None:
                    choice.append(i)
        
        return choice

    def cube(self, player, game, choice):
        print("Random cube is coming...")
        choixCube = random.choice(choice)
        print("Cube :", choixCube)

        return choixCube
    
    def direction(self, player, game, cube):
        choixDirection = random.choice(self.firstDirections)
        print("Check if {} is forbidden...".format(choixDirection))
        if cube in self.forbidden[choixDirection]:
            print("Forbiden!")
            print("Retry...")
            return self.direction(player, game, cube)
            
        print("Direction ok!")
        
        return choixDirection

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_port': port})
    cherrypy.quickstart(Server())