import numpy as np
import random
game =[0, 0, 0, 0, 0, 0, 0, None, 0, None, 0, None, 1, None, None, 0, None, None, None, None, 0, None, None, None, None]

matrix = list(range(25))
inc = {'N': 5, 'S': -5, 'E': 1, 'W': -1}
increment = {'N': -5, 'S': 5, 'E': 1, 'W': -1}
forbidden = {'E':[4, 9, 14, 19, 24], 'W':[0, 5, 10, 15, 20], 'N':[0, 1, 2, 3, 4], 'S':[20, 21, 22, 23, 24]}
gagne = [
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
for i in range(len(gagne)):
    win = 0
    for j in gagne[i]:
        if game[j] == 0:
            win += 1
    if win == 5:
        print("win ligne:", i)
