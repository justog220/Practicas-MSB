import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import copy
class AutomataMiocardico:
    def __init__(self):
        self.estado = 'R'
        self.E = -90
        self.UR = 90
        self.UP = 120

    def auto_excitar(self):
        self.estado = 'E'

    def calc_E(self, vec_1_E, vec_2_E, vec_3_E, vec_4_E):
        vecinos = [vec_1_E, vec_2_E, vec_3_E, vec_4_E]
        vecinos = [i - self.E for i in vecinos] 
        CC_k = sum(vecinos)
        # print(CC_k)
        if self.estado == 'R':
            if CC_k > self.UR:
                self.estado = 'E'
        elif self.estado == 'E':
            self.E += 60
            if self.E >= 30:
                self.estado = 'PRA'
        elif self.estado == 'PRA':
        # self.E = self.E * math.e**(-0.04)
            self.E = self.E * 0.96
            if self.E <= 1/1000:
                self.estado = 'PRR'
        elif self.estado == 'PRR':
            if CC_k > self.UP:
                self.E = 'E'
                self.E = self.E + 60
            else:
                self.E = self.E - 1
                if self.E <= -90:
                    self.E = -90
                    self.estado = 'R'
                                    
# fig, ax = plt.subplots()

filas = 50
columnas = 50


if filas%2 == 0:
    filas += 1
    
if columnas%2 == 0:
    columnas += 1
    
centro = (int(filas/2), int(columnas/2))


segundos = 5
ts = np.arange(0, segundos, 0.001)

artists = []

G = [[AutomataMiocardico() for j in range(columnas)] for i in range(filas)]
    
vmin, vmax = -90, 50
im = plt.imshow([[G[i][j].E for j in range(columnas)] for i in range(filas)], vmin=vmin, vmax=vmax)

count = 0

for t in ts:
    # print(t)
    if (t-0.5)%1 == 0:
        G[centro[0]][centro[1]].auto_excitar()
    
    G_futura = copy.deepcopy(G)

    for f in range(filas):
        for c in range(columnas):
            vecinos = [
                G[f-1][c].E if f > 0 else G[filas-1][c].E,
                G[f][(c+1)%columnas].E,
                G[(f+1)%filas][c].E,
                G[f][c-1].E if c > 0 else G[f][columnas-1].E
            ]
            G_futura[f][c] = copy.copy(G[f][c])
            G_futura[f][c].calc_E(vecinos[0], vecinos[1], vecinos[2], vecinos[3])     

    G = [linea[:] for linea in G_futura]

    if count%15 == 0:
        print("Draw ", t)
        im.set_data([[G[i][j].E for j in range(columnas)] for i in range(filas)])

        plt.draw()
        plt.pause(0.00000001)

    count+=1


