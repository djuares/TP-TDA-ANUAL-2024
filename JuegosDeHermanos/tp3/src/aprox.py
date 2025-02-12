import time

def queda_demanda_por_cumplir(demanda_filas, demanda_columnas):
    return sum(demanda_filas) + sum(demanda_columnas) > 0

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
    n = len(tablero)
    m = len(tablero[0])
    
    while queda_demanda_por_cumplir(demanda_filas, demanda_columnas) and barcos:
        flag_marcado = False
        
        # Obtenemos todos los indices de las demandas junto con su orientacion (fila/columna)
        demandas = [(i, "fila", demanda_filas[i]) for i in range(n) if demanda_filas[i] > 0] + \
                   [(j, "columna", demanda_columnas[j]) for j in range(m) if demanda_columnas[j] > 0]
        
        # Ordenar por demanda de mayor a menor
        demandas.sort(key=lambda x: x[2], reverse=True)
        
        for indice_max_demanda, tipo, _ in demandas:
            for barco in barcos:
                posicion = posicion_valida(tablero, barco, n, m, demanda_filas, demanda_columnas, indice_max_demanda, tipo)
                
                if posicion is not None and not supera_demanda_permitida(tablero, posicion, barco, demanda_filas, demanda_columnas):
                    if tipo == "fila" and demanda_filas[indice_max_demanda] >= barco:
                        marcar_barco_y_actualizar_demandas(tablero, barco, posicion, demanda_filas, demanda_columnas)
                        barcos.remove(barco)
                        indice_barco += 1
                        flag_marcado = True
                        break
                    elif tipo == "columna" and demanda_columnas[indice_max_demanda] >= barco:
                        marcar_barco_y_actualizar_demandas(tablero, barco, posicion, demanda_filas, demanda_columnas)
                        barcos.remove(barco)
                        indice_barco += 1
                        flag_marcado = True
                        break
            
            if flag_marcado:
                break  # Si pudimos colocar un barco, volvemos a calcular demandas
        
        # Si no pudimos colocar ningun barco en ninguna fila/columna, terminamos
        if not flag_marcado:
            break
    
    return tablero, max(0, sum(demanda_filas) + sum(demanda_columnas))


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


if __name__ == "__main__":
    demanda_filas = [1,0,1,0,1,0,0,1,1,1]
    demanda_columnas = [1,4,3]
    barcos = [3,3,4]
    ap(demanda_filas, demanda_columnas, barcos)

    