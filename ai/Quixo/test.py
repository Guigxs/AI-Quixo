import numpy as np
import random
game =[0, 0, 0, 0, 0, 0, 0, None, 0, None, 0, None, 1, None, None, 0, None, None, None, None, 0, None, None, None, None]
game = np.eye(5)
game = np.arange(2, 27)
matrix = list(range(25))
inc = {'N': 5, 'S': -5, 'E': 1, 'W': -1}
increment = {'N': -5, 'S': 5, 'E': 1, 'W': -1}
forbidden = {'E':[4, 9, 14, 19, 24], 'W':[0, 5, 10, 15, 20], 'N':[0, 1, 2, 3, 4], 'S':[20, 21, 22, 23, 24]}


tableau = np.resize(game, (5, 5))

print(tableau)
print(np.sum(tableau[:,:], axis= 0))

tableau = np.eye(5)
print(tableau.T)
print(tableau)

print(np.trace(tableau))
print(np.trace(tableau))