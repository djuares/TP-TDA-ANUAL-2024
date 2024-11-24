import time

TYPE = 0
DEMAND = 1
INDEX = 2

def queda_demanda_por_cumplir(demanda_filas, demanda_columnas):
    return sum(demanda_filas) + sum(demanda_columnas) > 0

def obtener_demandas_ordenadas(demanda_filas, demanda_columnas):
    demandas = []
    for i in range(len(demanda_filas)):
        demandas.append(("fila", demanda_filas[i], i))
    for j in range(len(demanda_columnas)):
        demandas.append(("columna", demanda_columnas[j], j))
    
    return sorted(demandas, key=lambda x: x[1], reverse=True)

def supera_demanda_permitida(tablero, posicion, tamaño_barco, demanda_fila, demanda_columna):
    
    n = len(tablero)
    m = len(tablero[0])
    i, j = posicion[0]
    orientacion = posicion[1]

    if orientacion == 'horizontal':
        for y in range(j, j + tamaño_barco):
            if y >= m:
                break
            if demanda_columna[y] < 1:
                return True

    elif orientacion == 'vertical':
        for x in range(i, i + tamaño_barco):
            if x >= n:
                break
            if demanda_fila[x] < 1:
                return True

    return False

def es_posicion_valida(tablero, tamaño_barco, posicion, n, m):
    x, y = posicion[0]
    orientacion = posicion[1]

    if orientacion == 'horizontal':
        for j in range(y, y + tamaño_barco):
            if j >= m or tablero[x][j] != 0:
                return False
            # Chequeo de que no haya barcos adyacentes ni diagonales
            if (x > 0 and tablero[x-1][j] != 0) or \
               (x < n-1 and tablero[x+1][j] != 0) or \
               (j > 0 and tablero[x][j-1] != 0) or \
               (j < m-1 and tablero[x][j+1] != 0) or \
               (x > 0 and j > 0 and tablero[x-1][j-1] != 0) or \
               (x > 0 and j < m-1 and tablero[x-1][j+1] != 0) or \
               (x < n-1 and j > 0 and tablero[x+1][j-1] != 0) or \
               (x < n-1 and j < m-1 and tablero[x+1][j+1] != 0):
                return False
    elif orientacion == 'vertical':
        for i in range(x, x + tamaño_barco):
            if i >= n or tablero[i][y] != 0:
                return False
            # Chequeo de que no haya barcos adyacentes ni diagonales
            if (y > 0 and tablero[i][y-1] != 0) or \
               (y < m-1 and tablero[i][y+1] != 0) or \
               (i > 0 and tablero[i-1][y] != 0) or \
               (i < n-1 and tablero[i+1][y] != 0) or \
               (i > 0 and y > 0 and tablero[i-1][y-1] != 0) or \
               (i > 0 and y < m-1 and tablero[i-1][y+1] != 0) or \
               (i < n-1 and y > 0 and tablero[i+1][y-1] != 0) or \
               (i < n-1 and y < m-1 and tablero[i+1][y+1] != 0):
                return False

    return True

def posicion_valida(tablero, tamaño_barco, n, m, demanda_filas, demanda_columnas, tipo, indice):
    if tipo == "fila":
        for j in range(m):
            if j + tamaño_barco <= m:
                if es_posicion_valida(tablero, tamaño_barco, ((indice, j), "horizontal"), n, m) and not supera_demanda_permitida(tablero, ((indice, j), "horizontal"), tamaño_barco, demanda_filas, demanda_columnas):
                    return ((indice, j), "horizontal")
    else:
        for i in range(n):
            if i + tamaño_barco <= n:
                if es_posicion_valida(tablero, tamaño_barco, ((i, indice), "vertical"), n, m) and not supera_demanda_permitida(tablero, ((i, indice), "vertical"), tamaño_barco, demanda_filas, demanda_columnas):
                    return ((i, indice), "vertical")
    
def batalla_naval_individual_aprox(tablero, demanda_filas, demanda_columnas, barcos):

    indice_barco = 1
    flag_marcado = True

    while queda_demanda_por_cumplir(demanda_filas, demanda_columnas) and len(barcos) > 0:
        if not flag_marcado:
            break

        flag_marcado = False
        demandas = obtener_demandas_ordenadas(demanda_filas, demanda_columnas)

        for demanda in demandas:
            tipo = demanda[TYPE]
            nro_demanda = demanda[DEMAND]
            indice = demanda[INDEX]
            
            for barco in barcos:
                posicion = posicion_valida(tablero, barco, len(tablero), len(tablero[0]), demanda_filas, demanda_columnas, tipo, indice)
                if posicion is None:
                    continue
                if tipo == "fila":
                    if nro_demanda >= barco:
                        for j in range(posicion[0][1], posicion[0][1] + barco):
                            tablero[indice][j] = indice_barco
                            demanda_columnas[j] -= 1
                        demanda_filas[indice] -= barco
                        barcos.remove(barco)
                        indice_barco += 1
                        flag_marcado = True
                        break
                
                else:
                    if barco <= len(tablero) and nro_demanda >= barco:
                        for i in range(posicion[0][0], posicion[0][0] + barco):
                            tablero[i][indice] = indice_barco
                            demanda_filas[i] -= 1
                        demanda_columnas[indice] -= barco
                        barcos.remove(barco)
                        indice_barco += 1
                        flag_marcado = True
                        break
                
            if flag_marcado:
                break
    return tablero, sum(demanda_filas) + sum(demanda_columnas)


def crear_tablero_vacio(n, m):
    return [[0] * m for _ in range(n)]

def ap(demanda_fila, demanda_columna, barcos):
    tablero = crear_tablero_vacio(len(demanda_fila), len(demanda_columna))
    t1 = time.time()
    barcos.sort(reverse=True)
    mejor_tablero, mejor_demanda_inc = batalla_naval_individual_aprox(tablero, demanda_fila.copy(), demanda_columna.copy(), barcos)
    t2 = time.time()
    print(f"Tiempo de ejecución: {t2 - t1}")
    return mejor_tablero, mejor_demanda_inc
    