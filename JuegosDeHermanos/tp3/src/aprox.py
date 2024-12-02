import time

TYPE = 0
DEMAND = 1
INDEX = 2

def queda_demanda_por_cumplir(demanda_filas, demanda_columnas):
    return sum(demanda_filas) + sum(demanda_columnas) > 0

def obtener_max_demanda(demanda_filas, demanda_columnas):
    max_demanda_filas = max(demanda_filas)
    max_demanda_columnas = max(demanda_columnas)
    
    if max_demanda_filas > max_demanda_columnas:
        return demanda_filas.index(max_demanda_filas), "fila"
    else:
        return demanda_columnas.index(max_demanda_columnas), "columna"

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

def posicion_valida(tablero, tamaño_barco, n, m, demanda_filas, demanda_columnas, indice, tipo):
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

def marcar_barco_y_actualizar_demandas(tablero, tamaño_barco, posicion, demanda_filas, demanda_columnas):
    x, y = posicion[0]
    orientacion = posicion[1]

    if orientacion == 'horizontal':
        for j in range(y, y + tamaño_barco):
            tablero[x][j] = 1
            demanda_filas[x] -= 1
            demanda_columnas[j] -= 1
    elif orientacion == 'vertical':
        for i in range(x, x + tamaño_barco):
            tablero[i][y] = 1
            demanda_filas[i] -= 1
            demanda_columnas[y] -= 1

def batalla_naval_individual_aprox(tablero, demanda_filas, demanda_columnas, barcos):

    indice_barco = 1
    flag_marcado = True
    n = len(tablero)
    m = len(tablero[0])

    # Mientras haya demanda por cumplir y barcos por ubicar
    while queda_demanda_por_cumplir(demanda_filas, demanda_columnas) and len(barcos) > 0:
        if not flag_marcado:
            break

        flag_marcado = False

        # Obtengo el indice de la fila/columna con mayor demanda y su tipo (fila/columna)
        indice_max_demanda, tipo = obtener_max_demanda(demanda_filas, demanda_columnas)

        for barco in barcos:
            
            # Obtengo una posicion valida para ubicar el barco de mayor tamaño
            posicion = posicion_valida(tablero, barco, n, m, demanda_filas, demanda_columnas, indice_max_demanda, tipo)
            if posicion is None:
                continue
            
            if tipo == "fila":
                if demanda_filas[indice_max_demanda] >= barco:
                    marcar_barco_y_actualizar_demandas(tablero, barco, posicion, demanda_filas, demanda_columnas)
                    barcos.remove(barco)
                    indice_barco += 1
                    flag_marcado = True
                    break
            
            else:
                if barco <= len(tablero) and demanda_columnas[indice_max_demanda] >= barco:
                    marcar_barco_y_actualizar_demandas(tablero, barco, posicion, demanda_filas, demanda_columnas)
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
    