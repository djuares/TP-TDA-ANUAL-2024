from random import randint, seed
import time
from ..tp3.src.backtracking import bt
from ..tp3.src.pl import pl
from ..tp3.src.aprox import ap

def generar_set_datos(cantidad):
    set_datos = []

    for i in range(1, cantidad+1):
        n = i * 3
        m = i * 3
        k = i * 2
        barcos = [randint(1, 16) for _ in range(k)]
        demandas_filas = [randint(0, 15) for _ in range(n)]
        demandas_columnas = [randint(0, 15) for _ in range(m)]

        set_datos.append((barcos, demandas_filas, demandas_columnas))
    
    return set_datos

def mediciones_tiempo(set_datos, algoritmo):
    mediciones = []

    for i in range(len(set_datos)):
        barcos, demandas_filas, demandas_columnas = set_datos[i]

        time_start = time.time()
        algoritmo(demandas_filas, demandas_columnas, barcos)
        time_end = time.time()

        mediciones.append((i+1, time_end - time_start))

    return mediciones
