
import time
import random
from tp1.tp1 import greedy

# Generar lista de monedas de tamaño n con valores aleatorios
n = 10000
monedas = [random.randint(1, 100) for _ in range(n)]

# Medición de tiempo
start_time = time.time()
ganancias = greedy(monedas)
end_time = time.time()

print("Tiempo de ejecución: ", end_time - start_time)
