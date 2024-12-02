from random import randint, seed
import time
from ..tp3.src.backtracking import bt
from ..tp3.src.pl import pl
from ..tp3.src.aprox import ap


# Genera n sets de datos de tamaño incremental para el problema de las monedas. 
# Si se especifica una semilla, se utilizara para generar los datos.
def generar_set_datos_monedas(semilla, n):
    if semilla != None:
        seed(semilla)

    set_datos = []

    for i in range(1, n+1):
        set_datos.append([randint(1, 10000) for _ in range(i * 10)])
    
    return set_datos

# Genera n sets de datos de tamaño incremental para el problema de la Batalla Naval. 
# Si se especifica una semilla, se utilizara para generar los datos.
def generar_set_datos_batalla_naval(semilla, n):
    if semilla != None:
        seed(semilla)

    set_datos = []

    for i in range(1, n+1):
        n = i * 3
        m = i * 3
        k = i * 2
        barcos = [randint(1, min(i * 3, 16)) for _ in range(k)]
        demandas_filas = [randint(0, min(i * 3, 15)) for _ in range(n)]
        demandas_columnas = [randint(0, min(i * 3, 15)) for _ in range(m)]

        set_datos.append((barcos, demandas_filas, demandas_columnas))

    return set_datos


# Realiza mediciones de tiempo para un set de datos del problema de la Batalla Naval y un algoritmo dado [bt, pl, ap].
def mediciones_tiempo_batalla_naval(set_datos, algoritmo):
    mediciones = []

    for i in range(len(set_datos)):
        barcos, demandas_filas, demandas_columnas = set_datos[i]

        time_start = time.time()
        algoritmo(demandas_filas, demandas_columnas, barcos)
        time_end = time.time()

        mediciones.append((i+1, time_end - time_start))

    return mediciones

# Realiza mediciones de tiempo para un set de datos del problema de las monedas y un algoritmo dado [greedy, pd].
def mediciones_tiempo_monedas(set_datos, algoritmo):
    mediciones = []

    for i in range(len(set_datos)):
        monedas = set_datos[i]

        time_start = time.time()
        algoritmo(monedas)
        time_end = time.time()

        mediciones.append((i+1, time_end - time_start))

    return mediciones
