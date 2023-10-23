from random import *
import numpy as np
import math

size = 8
child1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
matriz = np.zeros((size, size), dtype=np.float)

for i in range(size):
    for j in range(size):
        if (i % 2 == 0):
            matriz[i][j] = math.sqrt((i*size)+(j+1))
        else:
            matriz[i][j] = math.log10((i*size)+(j+1))

print(matriz)
