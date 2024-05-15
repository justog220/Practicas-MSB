import numpy as np
import matplotlib.pyplot as plt

# TP9 Estocásticos
# ejercicios 1-4

#Fijamos la semilla del generador de números aleatorios de NumPy para garantizar reproducibilidad en los resultados.
#Establecer la semilla aleatoria en 0 asegura que cualquier llamada posterior a funciones aleatorias produzca la misma 
#secuencia de números aleatorios
np.random.seed(0)

h = 0.01  # 0.1 ms
l_max = 6000  # mayor t de simulación
t = np.arange(0, l_max * h, h)

#Creamos un arreglo V para representar el potencial de membrana. Inicializamos todos los valores en 0 excepto el primer valor que lo 
# establecemos en -70 mV, que es el potencial inicial.
V = np.zeros(l_max)
V[0] = -70  # mV

#Creamos un arreglo Im para representar la corriente aplicada. Definimos pulsos de corriente en diferentes momentos de la simulación.
Im = np.zeros(l_max)
# punto 4
Im[0:50] = 15
Im[1200:2400] = 50
Im[2400:2805] = 20
Im[3400:3600] = 70
Im[5400:5600] = 70

# tasas de activación y desactivación de las subunidades de los canales iónicos
alfa_m = np.zeros(l_max)
alfa_h = np.zeros(l_max)
alfa_n = np.zeros(l_max)
beta_m = np.zeros(l_max)
beta_h = np.zeros(l_max)
beta_n = np.zeros(l_max)

# subunidades iniciales abiertas o cerradas de los canales iónicos
mm = np.zeros(l_max)
hh = np.zeros(l_max)
nn = np.zeros(l_max)
Em = np.zeros(l_max)
g = np.zeros(l_max)

# Valores de parámetros
gNac = 120  # ms/cm2
gKc = 36  # ms/cm2
gLc = 0.3  # ms/cm2
ENa = 45  # mV
EK = 82  # mV
EL = 59  # mV
Cm = 1  # MAms/cm2

# Matrices de subunidades abiertas o cerradas de los canales iónicos
N = 10  # ejercicio 3: N=10,100,1000
sub_n = np.zeros((4, N))
sub_mh = np.zeros((4, N))

# Cantidad de canales n
can_n = np.zeros(N)
can_mh = np.zeros(N)

# Tasas de activación y desactivación de subunidades
alfa_m[0] = ((V[0] + 45) / 10) / (1 - np.exp(-1 * (V[0] + 45) / 10))
alfa_h[0] = 0.07 * np.exp(-1 * (V[0] + 70) / 20)
alfa_n[0] = ((V[0] + 60) / 100) / (1 - np.exp(-1 * (V[0] + 60) / 10))
beta_m[0] = 4 * np.exp((-1 * (V[0] + 70) / 18))
beta_h[0] = 1 / (1 + np.exp(-1 * (V[0] + 40) / 10))
beta_n[0] = 0.125 * np.exp(-1 * (V[0] + 70) / 80)

# Subunidades, valor inicial
mm[0] = alfa_m[0] / (alfa_m[0] + beta_m[0])
hh[0] = alfa_h[0] / (alfa_h[0] + beta_h[0])
nn[0] = alfa_n[0] / (alfa_n[0] + beta_n[0])

# Conductancias, valor inicial
gNa_est = np.zeros(l_max)
gK_est = np.zeros(l_max)
gL = np.zeros(l_max)
gNa_est[0] = gNac * (mm[0]) ** 3 * hh[0]
gK_est[0] = gKc * (nn[0]) ** 4
gL[0] = gLc

# Contador de subunidades
cont_n = 0
cont_mh = 0

# Valor inicial de subunidades abiertas o cerradas
# np.random.rand(4, N) genera una matriz de 4xN de nros random
sub_n = np.random.rand(4, N) < nn[0]
sub_m = np.random.rand(4, N) < mm[0]
sub_h = np.random.rand(1, N) < hh[0]

# Cantidad total de subunidades por canal
T_sub_n = 4 * N
T_sub_m = 3 * N
T_sub_h = 1 * N

# Variable para cantidad de subunidades abiertas
sub_ab_n = 0
sub_ab_m = 0
sub_ab_h = 0

for n in range(1, l_max):
    # se actualizan las tasas de activación y desactivación de las subunidades de los canales iónicos
    a_h = 0.07 * np.exp(-(V[n - 1] + 70) / 20)
    b_h = 1 / (1 + np.exp(-(V[n - 1] + 40) / 10))
    a_m = ((V[n - 1] + 45) / 10) / (1 - np.exp(-(V[n - 1] + 45) / 10))
    a_n = ((V[n - 1] + 60) / 100) / (1 - np.exp(-(V[n - 1] + 60) / 10))
    b_n = 0.125 * np.exp(-(V[n - 1] + 70) / 80)
    b_m = 4 * np.exp(-(V[n - 1] + 70) / 18)

    # todos los canales cerrados
    can_n[:] = 0
    can_mh[:] = 0

    # todas las subunidades cerradas
    sub_ab_n = 0
    sub_ab_m = 0
    sub_ab_h = 0

    # se actualizan las subunidades de los canales iónicos estocásticamente
    # Se generan números aleatorios y se comparan con las tasas de activación
    # y desactivación para determinar si las subunidades se abren o cierran.
    for j in range(N):
        cont_n = 0
        # para cada subunidad_n de K...
        for k in range(4):
            r = np.random.rand()
            if sub_n[k, j] == 1:  # cierro los canales al azar
                if r < b_n * h:
                    sub_n[k, j] = 0
            else:  # abro los canales al azar
                if r < a_n * h:
                    sub_n[k, j] = 1
            if sub_n[k, j] == 1:  # chequeo si todas se abrieron
                cont_n += 1
                sub_ab_n += 1

        if cont_n == 4:  # si están las cuatro subunidades abiertas, abre canal
            can_n[j] = 1

        # subunidades_m Na
        cont_mh = 0
        for k in range(3):
            r = np.random.rand()
            if sub_m[k, j] == 1:  # abierta->cerrar
                if r < b_m * h:
                    sub_m[k, j] = 0
            else:  # cerrada->abrir
                if r < a_m * h:
                    sub_m[k, j] = 1

            if sub_m[k, j] == 1:
                cont_mh += 1
                sub_ab_m += 1

        # subunidad_h de Na
        r = np.random.rand()
        if sub_m[3, j] == 1:  # abierta->cerrar
            if r < b_h * h:
                sub_m[3, j] = 0
        else:  # cerrada->abrir
            if r < a_h * h:
                sub_m[3, j] = 1

        if sub_m[3, j] == 1:
            cont_mh += 1
            sub_ab_h += 1

        if cont_mh == 4:
            can_mh[j] = 1

    # sumo la cantidad de canales abiertos n y mh
    ab_n = np.sum(can_n)
    ab_mh = np.sum(can_mh)

    # se estima la conductancia de los canales dividiendo la cantidad de
    # subunidades abiertas entre el número total de canales.
    gNa_est[n] = gNac * (ab_mh / N)
    gK_est[n] = gKc * (ab_n / N)
    gL[n] = gLc

    # Se actualiza el potencial de membrana (V) utilizando la corriente
    # aplicada (Im) y las conductancias estimadas de los canales iónicos.
    if n == 500:  # punto 2
        V[n] = 15 + V[n - 1] + h * (-1 / Cm * (-Im[n] + (V[n - 1] - ENa) * gNa_est[n] + (V[n - 1] + EK) * gK_est[n] + (V[n - 1] + EL) * gL[n]))
    else:
        V[n] = V[n - 1] + h * (-1 / Cm * (-Im[n] + (V[n - 1] - ENa) * gNa_est[n] + (V[n - 1] + EK) * gK_est[n] + (V[n - 1] + EL) * gL[n]))

plt.subplot(3, 1, 1)
plt.plot(t, Im)
plt.title("Corriente")
plt.ylabel("uA")
plt.xlabel("ms")

plt.subplot(3, 1, 2)
plt.plot(t, V)
plt.title("Voltaje")
plt.ylabel("mV")
plt.xlabel("ms")
plt.ylim([-80, 30])

#Estas conductancias representan la permeabilidad de la membrana neuronal a los iones de sodio y potasio, que son fundamentales para la 
#generación y propagación del potencial de acción.
plt.subplot(3, 1, 3)
plt.plot(t, gK_est, 'r')
plt.plot(t, gNa_est, 'b')
plt.ylabel("mSiemens/cm2")
plt.xlabel("ms")
plt.title("Canal Naest(azul) y Kest(rojo)")
plt.ylim([-0, 70])

plt.tight_layout()
plt.show()
