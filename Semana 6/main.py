import math
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
			self.E = self.E * math.e**(-0.04)
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
                              
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
fig, ax = plt.subplots()

filas = 100
columnas = 100


if filas%2 == 0:
    filas += 1
    
if columnas%2 == 0:
    columnas += 1
    
centro = (int(filas/2), int(columnas/2))


segundos = 2
ts = np.arange(0, segundos, 0.001)

artists = []
def update(t):
    global G
    G_futura = G
    if (t-0.5)%1 == 0:
        G[centro[0]][centro[1]].auto_excitar()
    for f in range(filas):
        for c in range(columnas):
            if f == 0:
                if c == 0:
                    G_futura[f][c].calc_E(G[f][c].E, G[f][c+1].E, G[f+1][c].E, G[f][columnas-1].E)
                elif c == columnas-1:
                    G_futura[f][c].calc_E(G[f][c].E, G[f][0].E, G[f+1][c].E, G[f][c-1].E)
                else:
                    G_futura[f][c].calc_E(G[f][c].E, G[f][c+1].E, G[f+1][c].E, G[f][c-1].E)
            elif f == filas-1:
                if c == 0:
                    G_futura[f][c].calc_E(G[f-1][c].E, G[f][c+1].E, G[f][c].E, G[f][c-1].E)
                elif c == columnas-1:
                    G_futura[f][c].calc_E(G[f-1][c].E, G[f][0].E, G[f][c].E, G[f][c-1].E)
                else:
                    G_futura[f][c].calc_E(G[f-1][c].E, G[f][c+1].E, G[f][c].E, G[f][c-1].E)
            elif c == 0:
                if f == 0:
                    G_futura[f][c].calc_E(G[f][c].E, G[f][c+1].E, G[f+1][c].E, G[f][columnas-1].E)
                elif f == filas-1:
                    G_futura[f][c].calc_E(G[f-1][c].E, G[f][c+1].E, G[f][c].E, G[f][columnas-1].E)
                else:
                    G_futura[f][c].calc_E(G[f][c].E, G[f][c+1].E, G[f+1][c].E, G[f][columnas-1].E)
            elif c == columnas-1:
                if f == 0:
                    G_futura[f][c].calc_E(G[f][c].E, G[f][0].E, G[f+1][c].E, G[f][c-1].E)
                elif f == filas-1:
                    G_futura[f][c].calc_E(G[f-1][c].E, G[f][0].E, G[f][c].E, G[f][c-1].E)
                else:
                    G_futura[f][c].calc_E(G[f-1][c].E, G[f][0].E, G[f][c].E, G[f][c-1].E)
            else:
                G_futura[f][c].calc_E(G[f-1][c].E, G[f][c+1].E, G[f+1][c].E, G[f][c-1].E)        
                    
                    
            G = G_futura
    im.set_array([[G[i][j].E for j in range(columnas)] for i in range(filas)])

    return [im]

G = [[AutomataMiocardico() for j in range(columnas)] for i in range(filas)]

im = ax.imshow([[G[i][j].E for j in range(columnas)] for i in range(filas)])

plt.colorbar(im)

ani = FuncAnimation(fig, update, frames=ts, interval=1)

import matplotlib
matplotlib.rcParams['animation.embed_limit'] = 100

ani_html = ani.to_jshtml()
with open('animacion.html', 'w') as f:
    f.write(ani_html)
# ani.save('animacion.gif', writer='ffmpeg', fps=30)
# plt.show()
