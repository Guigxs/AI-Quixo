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
         
        print("")
        print("######################################")
        print("############# Stupid bot #############")
        print("######################################")
        print("")
        print("--------------------------------------")
        print("State of the game :")
        game = body["game"]
        matrix = np.resize(game, (5, 5))
        print(matrix)
        
        first = len(body['moves'])

        print("")
        print("##########", first, "move(s) #########")  
        print("--------------------------------------")
        print("")
        print("--Logs:--")


        print("")
        print("##########", first, "move(s) ##########")   
        print("")

        if first%2 == 0: #Premier joueur
            power = 0
            choice = AI().bestCube(power, game)
            print("Liste des choix :", choice)
            print("First player with: X ({}) !".format(power))
            cube = AI().cube(power, game, choice)
            direction = AI().direction(power, game, cube)
            print("-----------------------------------")
            print("Send : X in", cube, "from", direction)
            print("-----------------------------------")
            return {'move' :{'cube' : cube, 'direction': direction}}
            
        elif first%2 == 1: #Scond joueur
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
        self.forbidden = {'N':[0, 1, 2, 3, 4], 'S':[20, 21, 22, 23, 24], 'E':[4, 9, 14, 19, 24], 'W':[0, 5, 10, 15, 20]}
        self.increment = {'N': -5, 'S': 5, 'E': 1, 'W': -1}

    # def makeChoice(self, power, game):
    #     choice = []
    #     for i in range(len(game)):
    #         if i in self.firstList:
    #             if game[i] == power or game[i] == None:
    #                 choice.append(i)
        
    #     return choice

    # def cube(self, player, game, choice):
    #     print("Random cube is coming...")
    #     choixCube = random.choice(choice)
    #     print("Cube :", choixCube)
    #     return choixCube
    
    # def direction(self, player, game, cube):
    #     choixDirection = random.choice(self.firstDirections)
    #     print("Check if {} is forbidden...".format(choixDirection))
    #     if cube in self.forbidden[choixDirection]:
    #         print("Forbiden!")
    #         print("Retry...")
    #         return self.direction(player, game, cube)
            
    #     print("Direction ok!")
    #     return choixDirection

    def bestCube(self, player, matrix):
        choice = []
        for i in range(len(matrix)):
            pass

    def bestDirection(self, player, matrix, cube):
        choice = []
        for i in range(len(self.firstDirections)):
            if cube not in self.forbidden[self.firstDirections[i]]:
                pass

    def applyDirection(self, player, matrix, cube, direction):
        colonne = cube%5
        ligne = int((cube - colonne)/5)

        game = np.resize(matrix, (5, 5))

        pass

    
    def checkAround(self, player, matrix, i):#Check si il y a des X ou O autour du cube
        if (matrix[i] == player) and ((matrix[i+1] == player and matrix[i+2] == player) or (matrix[i-1] == player and matrix[i-2] == player) or (matrix[i+6] == player and matrix[i+12] == player) or (matrix[i+5] == player and matrix[i+10] == player) or (matrix[i+4] == player and matrix[i+8] == player) or (matrix[i-5] == player and matrix[i-10] == player) or (matrix[i-6] == player and matrix[i-12] == player) or (matrix[i-4] == player and matrix[i-8] == player)):
            return True
        return False


    # def bestMove(self, player, matrix):
    #     #Test les coups gagnant
    #     jeu = matrix
    #     choice = []
    #     for i in range(len(jeu)):
    #         if jeu[i] == None:
    #             print("Try for", i)
    #             choice.append(i)
    #             jeu[i] = player

    #             if self.win(player, jeu) == True:
    #                 print("I win!")
    #                 print(np.resize(jeu, (3, 3)))
    #                 return i

    #             jeu[i] = None

    #     #Blocage de l'adversaire
    #     if player == 1:
    #         adversaire = 0
    #     else:
    #         adversaire = 1

    #     for i in range(len(jeu)):
    #         if jeu[i] == None:
    #             print("Try for", i)
    #             jeu[i] = adversaire

    #             if self.win(adversaire, jeu) == True:
    #                 print("I block!")
    #                 print(np.resize(jeu, (3, 3)))
    #                 return i

    #             jeu[i] = None

    #     return random.choice(choice) #Renvoit un nobre aléatoire 


    def win(self, player, matrix): #Check si le coup est gangnant
        if (matrix[0]==player and matrix[1]==player and matrix[2]==player and matrix[3]==player and matrix[4]==player) or (matrix[5]==player and matrix[6]==player and matrix[7]==player and matrix[8]==player and matrix[9]==player) or (matrix[10]==player and matrix[11]==player and matrix[12]==player and matrix[13]==player and matrix[14]==player) or (matrix[15]==player and matrix[16]==player and matrix[17]==player and matrix[18]==player and matrix[19]==player) or (matrix[20]==player and matrix[21]==player and matrix[22]==player and matrix[23]==player and matrix[24]==player) or (matrix[0]==player and matrix[6]==player and matrix[12]==player and matrix[18]==player and matrix[24]==player) or (matrix[20]==player and matrix[16]==player and matrix[12]==player and matrix[8]==player and matrix[4]==player) or (matrix[0]==player and matrix[5]==player and matrix[10]==player and matrix[15]==player and matrix[20]==player) or (matrix[1]==player and matrix[6]==player and matrix[11]==player and matrix[16]==player and matrix[21]==player) or (matrix[2]==player and matrix[7]==player and matrix[12]==player and matrix[17]==player and matrix[22]==player) or (matrix[3]==player and matrix[8]==player and matrix[13]==player and matrix[18]==player and matrix[23]==player) or (matrix[4]==player and matrix[9]==player and matrix[14]==player and matrix[19]==player and matrix[24]==player):
            return True
        return False 
                

    
                        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_port': port})
    cherrypy.quickstart(Server())