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
        
        first = len(body['moves'])# Check nbre de coups
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
            print("-------", body['moves'], "-------")
            power = 0
            print("First player with: X ({}) !".format(power))
            cube = int(input("Cube : "))
            direction = str(input("Direction : "))
            print("-----------------------------------")
            print("Send : X in", cube, "from", direction)
            print("-----------------------------------")
            return {'move' :{'cube' : cube, 'direction': direction}}

        elif first%2 == 1: #Second joueur
            power = 1
            print("Second player with: O ({}) !".format(power))
            cube = int(input("Cube : "))
            direction = str(input("Direction : "))
            print("-----------------------------------")
            print("Send : O in", cube, "from", direction)
            print("-----------------------------------")
            return {'move' :{'cube' : cube, 'direction': direction}}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_port': port})
    cherrypy.quickstart(Server())