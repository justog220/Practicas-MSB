import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from concurrent.futures import ThreadPoolExecutor
import copy

class AutomataMiocardico:
    def __init__(self):
        self.estado = 'R'
        self.E = -90
        self.UR = 90
        self.UP = 120

    def auto_excitar(self):
        self.estado = 'E'

    def calc_E(self, vecinos):
        vecinos = [i - self.E for i in vecinos] 
        CC_k = sum(vecinos)
        if self.estado == 'R':
            if CC_k > self.UR:
                self.estado = 'E'
        elif self.estado == 'E':
            self.E += 60
            if self.E >= 30:
                self.estado = 'PRA'
        elif self.estado == 'PRA':
            self.E *= 0.96
            if self.E <= 1/1000:
                self.estado = 'PRR'
        elif self.estado == 'PRR':
            if CC_k > self.UP:
                self.auto_excitar()
            else:
                self.E -= 1
                if self.E <= -90:
                    self.E = -90
                    self.estado = 'R'

def calculate_neighbors(f, c, G):
    filas = len(G)
    columnas = len(G[0])
    vecinos = [
        G[f-1][c].E if f > 0 else G[filas-1][c].E,
        G[f][(c+1)%columnas].E,
        G[(f+1)%filas][c].E,
        G[f][c-1].E if c > 0 else G[f][columnas-1].E
    ]
    return vecinos

filas = 10
columnas = 10

if filas % 2 == 0:
    filas += 1

if columnas % 2 == 0:
    columnas += 1

centro = (int(filas / 2), int(columnas / 2))

segundos = 5
ts = np.arange(0, segundos, 0.001)

G = [[AutomataMiocardico() for j in range(columnas)] for i in range(filas)]
vmin, vmax = -90, 50
im = plt.imshow([[G[i][j].E for j in range(columnas)] for i in range(filas)], vmin=vmin, vmax=vmax)

def update(frame):
    if (frame-0.5) % 1 == 0:
        G[centro[0]][centro[1]].auto_excitar()

    with ThreadPoolExecutor() as executor:
        results = [executor.submit(calculate_neighbors, f, c, G) for f in range(filas) for c in range(columnas)]
        results = [result.result() for result in results]

    G_futura = copy.deepcopy(G)

    for f in range(filas):
        for c in range(columnas):
            G_futura[f][c].calc_E(results[f * columnas + c])

    for f in range(filas):
        for c in range(columnas):
            G[f][c] = G_futura[f][c]

    im.set_data([[G[i][j].E for j in range(columnas)] for i in range(filas)])
    return [im]

ani = FuncAnimation(plt.gcf(), update, frames=len(ts), interval=1, blit=True, repeat=False)
plt.show()
