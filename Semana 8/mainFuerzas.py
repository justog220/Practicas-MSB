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
	

	def calcular_nueva_posicion(self, vecinos_a, vecinos_s, vecinos_c,  xmin, xmax, ymin, ymax):
		
		self.v = self.calcular_velocidad(vecinos_a, vecinos_s, vecinos_c)

		if self.x < xmin:
			self.v[0] += xmin - self.x
		elif self.x > xmax:
			self.v[0] += xmax - self.x
 
		if self.y < ymin: 
			self.v[1] += ymin - self.y
		elif self.y > ymax: 
			self.v[1] += ymax - self.y

		self.x += T * self.v[0] + 0.01 
		self.y += T * self.v[1] + 0.01

from random import randint, uniform
import matplotlib.pyplot as plt

fig, ax = plt.subplots()


ax.set_xlim(0, 20)
ax.set_ylim(0, 20)
ax.set_xticks(range(0, 21))
ax.set_yticks(range(0, 21))

class Region2D:
	def __init__(self, filas, columnas, nro_boids, case=None):
		self.filas = filas
		self.columnas = columnas
		self.nro_boids = nro_boids
		if not case:
			self.boids = self.inicializar_boids()
		else:
			if case == 3:
				self.boids = self.inicializar_boids_caso_3()
			elif case == 4:
				self.boids = self.inicializar_boids_caso_4()
			elif case == 5:
				self.boids = self.inicializar_boids_caso_5()
		self.distancias = [None for boid in self.boids]
		self.calcular_distancias()
		self.vecinos_a = [None for boid in self.boids]
		self.calcular_vecinos_a()
		self.vecinos_s = [None for boid in self.boids]
		self.calcular_vecinos_s()
		self.vecinos_c = [None for boid in self.boids]
		self.calcular_vecinos_c()

		self.xmin = 0
		self.xmax = self.columnas
		self.ymin = 0
		self.ymax = self.filas

	def generar_v_aleatoria(self):
		vx = uniform(-1, 1)
		vy = uniform(-1, 1)

		modulo = sqrt(vx**2 + vy**2)
		factor = 70 / modulo
		vx *= factor
		vy *= factor

		return [vx, vy]


	def inicializar_boids(self):
		boids = []
		v = 5
		for i in range(self.nro_boids):
			x = randint(0, self.columnas)
			y = randint(0, self.filas)

			boids.append(Boid(x, y, self.generar_v_aleatoria()))

		return boids
	
	def inicializar_boids_caso_3(self):
		boids = []
		v = 5

		vx = 5
		vy = 5
		# Defino boid solitario :(
		v_0 = [None, None]
		x = 0
		y = 0
		# boids.append(Boid(x, y, [vx, vy]))
		boids.append(Boid(x, y, self.generar_v_aleatoria()))

		# Defino grupo de boids
		x_0 = self.columnas
		y_0 = self.filas
		despl = 0
		for i in range(self.nro_boids-1):
			x = x_0 #- despl
			y = y_0 - despl
			despl += 0.1
			# boids.append(Boid(x, y, [-vx,-vy]))
			boids.append(Boid(x, y, self.generar_v_aleatoria()))

		return boids

	def inicializar_boids_caso_4(self):
		boids = []

		vx, vy = 50, 50

		tamanio_grupo = int(self.nro_boids/2)

		x_0 = 0
		y_0 = 0
		despl = 0
		for i in range(tamanio_grupo):
			x = x_0 #+ despl
			y = y_0 + despl
			despl += 0.1
			# boids.append(Boid(x, y, [vx, vy]))
			boids.append(Boid(x, y, self.generar_v_aleatoria()))


		x_0 = self.columnas
		y_0 = self.filas
		despl = 0
		for i in range(tamanio_grupo):
			x = x_0# - despl
			y = y_0 - despl
			despl += 0.1
			# boids.append(Boid(x, y, [-vx, -vy]))
			boids.append(Boid(x, y, self.generar_v_aleatoria()))

		return boids
	
	def inicializar_boids_caso_5(self):
		boids = []

		vx, vy = 2, 2

		tamanio_grupo = int(self.nro_boids/2)

		x_0 = 0
		y_0 = 0
		despl = 0
		for i in range(2):
			x = x_0 + despl
			y = y_0 + despl
			despl += 0.1
			# boids.append(Boid(x, y, [vx, vy]))
			boids.append(Boid(x, y, self.generar_v_aleatoria()))


		x_0 = self.columnas
		y_0 = self.filas
		despl = 0
		for i in range(10):
			x = x_0 - despl
			y = y_0 - despl
			despl += 0.1
			# boids.append(Boid(x, y, [-vx, -vy]))
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
		print(t)
		for boid in range(len(self.boids)):
			self.boids[boid].calcular_nueva_posicion(self.vecinos_a[boid], self.vecinos_s[boid], self.vecinos_c[boid], self.xmin, self.xmax, self.ymin, self.ymax)

		self.draw()

	
	def draw(self):
		x = [boid.x for boid in self.boids]
		y = [boid.y for boid in self.boids]

		ax.clear()
		ax.scatter(x, y, marker="D", alpha=0.5)

		ax.set_xlim(self.xmin-2, self.xmax+2)
		ax.set_ylim(self.ymin-2, self.ymax+2)
		fig.canvas.draw()
		

T = 0.001
w_a = 0.1
w_s = 0.7
w_c = 0.1
radio_a = 4
radio_s = 0.5
radio_c = 4

import numpy as np
from matplotlib.animation import FuncAnimation

ts = np.arange(0, 5, T)

# print("Encuentro dos boids")
# region1 = Region2D(5, 5, 2)
# anim = FuncAnimation(fig, region1.iteracion, frames=ts)
# plt.show()

# print("Varios boids se encuentran")
# region2 = Region2D(10, 10, 10)
# anim = FuncAnimation(fig, region2.iteracion, frames=ts)
# plt.show()

# print("Un boid se encuentra con un grupo de boids")
# region2 = Region2D(10, 10, 4, case=3)
# anim = FuncAnimation(fig, region2.iteracion, frames=ts)
# plt.show()

# print("Dos grupos de boids de igual tamaño se encuentran")
# region2 = Region2D(10, 10, 20, case=4)
# anim = FuncAnimation(fig, region2.iteracion, frames=ts)
# plt.show()

print("Dos grupos de boids de diferente tamaño se encuentran")
region2 = Region2D(10, 10, 20, case=5)
anim = FuncAnimation(fig, region2.iteracion, frames=ts)
plt.show()




