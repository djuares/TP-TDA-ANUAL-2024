import copy
import time

def mostrar_tablero(tablero):
    for fila in tablero:
        print(" ".join(map(str, map(int, fila))))

def calcular_demanda_incumplida(demanda_fila, demanda_columna):
    return sum(demanda_fila) + sum(demanda_columna)

def marcar_barco_en_tablero(tablero, nro_barco, tamaño_barco, posicion):
    if posicion == None:
        return tablero
    
    copia_tablero = [fila[:] for fila in tablero]
    
    x, y = posicion[0]
    orientacion = posicion[1]
    if orientacion == "horizontal":
        for j in range(y, y + tamaño_barco):
            copia_tablero[x][j] = nro_barco
    elif orientacion == "vertical":
        for i in range(x, x + tamaño_barco):
            copia_tablero[i][y] = nro_barco

    return copia_tablero

def supera_demanda_permitida(tablero, posicion, tamaño_barco, demanda_fila, demanda_columna):
    if posicion == None:
        return False
    
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
    if posicion == None:
        return True
    
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

def calcular_posibles_posiciones(tablero, n, m, tamaño_barco, demanda_fila, demanda_columna):
    posiciones = []
    
    for i in range(n):
        if demanda_fila[i] < tamaño_barco:
            continue

        for j in range(m - tamaño_barco + 1):
            if demanda_columna[j] < 1:
                continue
            posicion = ((i, j), 'horizontal')
            if not supera_demanda_permitida(tablero, posicion, tamaño_barco, demanda_fila, demanda_columna) and es_posicion_valida(tablero, tamaño_barco, posicion, n, m):
                posiciones.append(posicion)

    if tamaño_barco == 1:
        posiciones.append(None)
        return posiciones
    
    for i in range(n - tamaño_barco + 1):
        if demanda_fila[i] < 1:
            continue
        for j in range(m):
            if demanda_columna[j] < tamaño_barco:
                continue
            posicion = ((i, j), 'vertical')
            if not supera_demanda_permitida(tablero, posicion, tamaño_barco, demanda_fila, demanda_columna) and es_posicion_valida(tablero, tamaño_barco, posicion, n, m):
                posiciones.append(posicion)

    posiciones.append(None)
    return posiciones

def actualizar_demandas(demanda_fila, demanda_columna, tamaño_barco, posicion):
    if posicion == None:
        return demanda_fila, demanda_columna
    
    x, y = posicion[0]
    orientacion = posicion[1]
    nueva_demanda_fila = demanda_fila.copy()
    nueva_demanda_columna = demanda_columna.copy()

    if orientacion == 'horizontal':
        for j in range(y, y + tamaño_barco): 
            nueva_demanda_fila[x] -= 1
            nueva_demanda_columna[j] -= 1
    elif orientacion == 'vertical':
        for i in range(x, x + tamaño_barco):
            nueva_demanda_fila[i] -= 1
            nueva_demanda_columna[y] -= 1

    return nueva_demanda_fila, nueva_demanda_columna


def crear_tablero_vacio(n, m):
    return [[0] * m for _ in range(n)]

def filtrar_barcos_por_demanda(barcos, demanda_fila, demanda_columna):
    max_demanda = max(max(demanda_fila), max(demanda_columna))
    return [barco for barco in barcos if barco <= max_demanda]

def obtener_indice_prox_barco(barcos):
    i = 0
    for i in range(len(barcos)):
        if barcos[i] != barcos[0]:
            return i
    return 1

def batalla_naval_bt(tablero, barcos, demanda_fila, demanda_columna, mejor_demanda_inc, demanda_inc, indice, mejor_tablero):
    if mejor_demanda_inc == 0:
        return mejor_tablero, mejor_demanda_inc

    if not barcos:
        demanda_inc = calcular_demanda_incumplida(demanda_fila, demanda_columna)
        if demanda_inc < mejor_demanda_inc:
            mejor_demanda_inc = demanda_inc
            mejor_tablero = copy.deepcopy(tablero)
        return mejor_tablero, mejor_demanda_inc
    
    barcos_filtrados = filtrar_barcos_por_demanda(barcos, demanda_fila, demanda_columna)
    if not barcos_filtrados:
        return mejor_tablero, mejor_demanda_inc

    # Si con los barcos que me quedan no puedo mejorar la mejor demanda incumplida, corto la rama
    if calcular_demanda_incumplida(demanda_fila, demanda_columna) - sum(barcos_filtrados)*2 >= mejor_demanda_inc:
        return mejor_tablero, mejor_demanda_inc
    
    posiciones = calcular_posibles_posiciones(tablero, len(tablero), len(tablero[0]), barcos_filtrados[0], demanda_fila, demanda_columna)

    mejor_tablero_actual = mejor_tablero 

    for posicion in posiciones:    

        if calcular_demanda_incumplida(demanda_fila, demanda_columna) - sum(barcos_filtrados)*2 >= mejor_demanda_inc:
            return mejor_tablero, mejor_demanda_inc
        
        nuevo_tablero = marcar_barco_en_tablero(tablero, indice, barcos_filtrados[0], posicion)

        nueva_demanda_fila, nueva_demanda_columna = actualizar_demandas(demanda_fila, demanda_columna, barcos_filtrados[0], posicion)

        # Si el barco actual no se puede ubicar, todos los barcos con igual tamaño tampoco, obtengo el primero distinto
        if posicion == None:
            i_prox_barco =  obtener_indice_prox_barco(barcos_filtrados)
        else:
            i_prox_barco = 1

        nuevo_tablero, nuevo_demanda_inc = batalla_naval_bt(nuevo_tablero, barcos_filtrados[i_prox_barco:], nueva_demanda_fila, nueva_demanda_columna, mejor_demanda_inc, demanda_inc, indice+1, mejor_tablero_actual)
        
        if nuevo_demanda_inc < mejor_demanda_inc:
            mejor_demanda_inc = nuevo_demanda_inc
            mejor_tablero = nuevo_tablero
    
    return mejor_tablero, mejor_demanda_inc


def es_posible_colocar_barco(n, m, tamaño_barco, demanda_fila, demanda_columna):
    # Horizontal
    for i in range(n):
        for j in range(m - tamaño_barco + 1):
            if all(demanda_columna[k] >= 1 for k in range(j, j + tamaño_barco)) and demanda_fila[i] >= tamaño_barco:
                return True

    # Vertical
    for j in range(m):
        for i in range(n - tamaño_barco + 1):
            if all(demanda_fila[k] >= 1 for k in range(i, i + tamaño_barco)) and demanda_columna[j] >= tamaño_barco:
                return True

    return False

def sacar_barcos_muy_grandes(n, m, barcos, demanda_fila, demanda_columna):
    max_demanda = max(max(demanda_fila), max(demanda_columna))

    for idx, barco in enumerate(barcos):
        if barco > max_demanda:
            continue
        if es_posible_colocar_barco(n, m, barco, demanda_fila, demanda_columna):
            return barcos[idx:]

    return []

def bt(demanda_fila, demanda_columna, barcos):
    tablero = crear_tablero_vacio(len(demanda_fila), len(demanda_columna))
    t1 = time.time()
    barcos = sacar_barcos_muy_grandes(len(tablero), len(tablero[0]), barcos, demanda_fila, demanda_columna)
    barcos.sort(reverse=True)
    mejor_tablero, mejor_demanda_inc = batalla_naval_bt(tablero, barcos, demanda_fila, demanda_columna, float('inf'), 0, 1, tablero)
    t2 = time.time()
    print(f"Tiempo de ejecución: {t2 - t1}")
    return mejor_tablero, mejor_demanda_inc