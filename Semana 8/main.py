from math import sqrt

class Boid:
	def __init__(self, x_0, y_0, v_0):
		self.x = x_0
		self.y = y_0
		self.v = v_0

	def calcular_distancia_euclidea(self, vecino):
		return sqrt((self.x-vecino.x)**2+(self.y-vecino.y)**2)

	def calcular_a(self, vecinos):
		suma = [0, 0]
		for vecino in vecinos:
			suma[0] += vecino.v[0] - self.v[0]
			suma[1] += vecino.v[1] - self.v[1]

		return [suma[0]/len(vecinos), suma[1]/len(vecinos)]

	def calcular_s(self, vecinos):
		suma = [0, 0]
		for vecino in vecinos:
			suma[0] += self.x - vecino.x
			suma[1] += self.y - vecino.y

		return suma

	def calcular_c(self, vecinos):
		suma = [0, 0]
		for vecino in vecinos:
			suma[0] += vecino.x - self.x
			suma[1] += vecino.y - self.y

		return [suma[0]/len(vecinos), suma[1]/len(vecinos)]

	def calcular_velocidad(self, vecinos_a, vecinos_s, vecinos_c):
		a = self.calcular_a(vecinos_a)
		s = self.calcular_s(vecinos_s)
		c = self.calcular_c(vecinos_c)

		return [self.v[0]+w_a*a[0]+w_s*s[0]+w_c*c[0],
		  		self.v[1]+w_a*a[1]+w_s*s[1]+w_c*c[1]]
	
	
	def calcular_nueva_posicion(self, vecinos_a, vecinos_s, vecinos_c):
		self.v = self.calcular_velocidad(vecinos_a, vecinos_s, vecinos_c)

		self.x = self.x + T * self.v[0] * 10 
		self.y = self.y + T * self.v[1] * 10

from random import randint, uniform
import matplotlib.pyplot as plt

fig, ax = plt.subplots()


ax.set_xlim(0, 20)
ax.set_ylim(0, 20)
ax.set_xticks(range(0, 21))
ax.set_yticks(range(0, 21))

class Region2D:
	def __init__(self, filas, columnas, nro_boids):
		self.filas = filas
		self.columnas = columnas
		self.nro_boids = nro_boids
		self.boids = self.inicializar_boids()
		self.distancias = [None for boid in self.boids]
		self.calcular_distancias()
		self.vecinos_a = [None for boid in self.boids]
		self.calcular_vecinos_a()
		self.vecinos_s = [None for boid in self.boids]
		self.calcular_vecinos_s()
		self.vecinos_c = [None for boid in self.boids]
		self.calcular_vecinos_c()

	def generar_v_aleatoria(self):
		vx = uniform(-1, 1)
		vy = uniform(-1, 1)

		modulo = sqrt(vx**2 + vy**2)
		factor = 5 / modulo
		vx *= factor
		vy *= factor

		return [vx, vy]

	def inicializar_boids(self):
		boids = []
		v = 5
		for i in range(self.nro_boids):
			v_0 = [None, None]
			x = randint(0, self.columnas)
			y = randint(0, self.filas)

			boids.append(Boid(x, y, self.generar_v_aleatoria()))

		return boids
	
	def calcular_distancias(self):
		for i in range(len(self.boids)):
			distancias_i = []
			for j in range(len(self.boids)):
				distancias_i.append([j, self.boids[i].calcular_distancia_euclidea(self.boids[j])])

			self.distancias[i] = distancias_i

	def calcular_vecinos(self, radio):
		vecinos = [None for i in range(len(self.distancias))]
		for i in range(len(self.distancias)):
			vecinos_i = []
			for j in self.distancias[i]:
				if j[1] < radio:
					vecinos_i.append(self.boids[j[0]])

			vecinos[i] = vecinos_i

		return vecinos

	def calcular_vecinos_a(self):
		self.vecinos_a = self.calcular_vecinos(radio_a)

	def calcular_vecinos_s(self):
		self.vecinos_s = self.calcular_vecinos(radio_s)

	def calcular_vecinos_c(self):
		self.vecinos_c = self.calcular_vecinos(radio_c)

	def iteracion(self, t):
		for boid in range(len(self.boids)):
			self.boids[boid].calcular_nueva_posicion(self.vecinos_a[boid], self.vecinos_s[boid], self.vecinos_c[boid])

		self.draw()

	def draw(self):
		x = [boid.x for boid in self.boids]
		y = [boid.y for boid in self.boids]

		ax.clear()
		ax.scatter(x, y, marker="D", alpha=0.5)

		ax.set_xlim(0, self.columnas)
		ax.set_ylim(0, self.filas)
		fig.canvas.draw()
		

T = 0.001
w_a = 0.1
w_s = 0.1
w_c = 0.1
radio_a = 4
radio_s = 0.5
radio_c = 4

import numpy as np
from matplotlib.animation import FuncAnimation
region = Region2D(10, 10, 20)
ts = np.arange(0, 5, T)

anim = FuncAnimation(fig, region.iteracion, frames=ts)
plt.show()





