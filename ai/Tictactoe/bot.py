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
        print("######## AI  ########")
        print("")
        print("--------------------------")
        print("State of the game :")
        print(np.resize(game, (3, 3)))
        print("--------------------------")

        first = 0
        for i in game:
            if i != None:
                first += 1

        print("")
        print("##########", first, "move(s) ##########")   
        print("")

        if first%2 == 0: #Premier joueur
            power = 0
            print("First player with: X ({}) !".format(power))
            choix = AI().bestMove(power, game)
            return {"move" : choix}

        elif first%2 == 1: #Scond joueur
            power = 1
            print("Second player with: O ({}) !".format(power))
            choix = AI().bestMove(power, game)
            return {"move" : choix}

class AI():
    def bestMove(self, player, matrix):
        #Test les coups gagnant
        jeu = matrix
        choice = []
        for i in range(len(jeu)):
            if jeu[i] == None:
                print("Try for", i)
                choice.append(i)
                jeu[i] = player

                if self.win(player, jeu) == True:
                    print("I win!")
                    print(np.resize(jeu, (3, 3)))
                    return i

                jeu[i] = None

        #Blocage de l'adversaire
        if player == 1:
            adversaire = 0
        else:
            adversaire = 1

        for i in range(len(jeu)):
            if jeu[i] == None:
                print("Try for", i)
                jeu[i] = adversaire

                if self.win(adversaire, jeu) == True:
                    print("I block!")
                    print(np.resize(jeu, (3, 3)))
                    return i

                jeu[i] = None

        return random.choice(choice) #Renvoit un nobre aléatoire 


    def win(self, player, matrix): #Check si le coup est gangnant
        if (matrix[0]==player and matrix[1]==player and matrix[2]==player) or (matrix[3]==player and matrix[4]==player and matrix[5]==player) or (matrix[6]==player and matrix[7]==player and matrix[8]==player) or (matrix[0]==player and matrix[3]==player and matrix[6]==player) or (matrix[1]==player and matrix[4]==player and matrix[7]==player) or (matrix[2]==player and matrix[5]==player and matrix[8]==player) or (matrix[0]==player and matrix[4]==player and matrix[8]==player) or (matrix[2]==player and matrix[4]==player and matrix[6]==player):
            return True
        else:
            return False 
                
                        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_port': port})
    cherrypy.quickstart(Server())