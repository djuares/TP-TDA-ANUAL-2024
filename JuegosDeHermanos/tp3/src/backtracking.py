import copy

def mostrar_tablero(tablero):
    for i in range(len(tablero)):
        fila = []
        for j in range(len(tablero[0])):
            valor = tablero[i][j]
            fila.append(str(int(valor)))
        print(" ".join(fila))

def calcular_demanda_incumplida(tablero, demanda_fila, demanda_columna):
    n = len(tablero)
    m = len(tablero[0])

    demanda_incumplida = 0
    for i in range(n):
        ocupadas = sum(1 for j in range(m) if tablero[i][j] != 0)
        demanda_incumplida += max(0, demanda_fila[i] - ocupadas)
    
    for j in range(m):
        ocupadas = sum(1 for i in range(n) if tablero[i][j] != 0)
        demanda_incumplida += max(0, demanda_columna[j] - ocupadas)
    
    return demanda_incumplida


def supera_demanda_permitida(tablero, posicion, tamaño_barco, demanda_fila, demanda_columna):
    n = len(tablero)
    m = len(tablero[0])
    i = posicion[0][0]
    j = posicion[0][1]
    orientacion = posicion[1]

    # Verificación de demanda en fila o columna según la orientación del barco
    if orientacion == 'horizontal':
        # Checar si sumar el barco excede la demanda en la fila
        if sum(tablero[i][k] != 0 for k in range(m)) + tamaño_barco > demanda_fila[i]:
            return True
        
        # Checar en cada columna donde estará el barco que no exceda la demanda de esa columna
        for y in range(j, j + tamaño_barco):
            if sum(tablero[k][y] != 0 for k in range(n)) + 1 > demanda_columna[y]:
                return True 

    else:  # Orientación vertical
        # Checar si sumar el barco excede la demanda en la columna
        if sum(tablero[k][j] != 0 for k in range(n)) + tamaño_barco > demanda_columna[j]:
            return True
        
        # Checar en cada fila donde estará el barco que no exceda la demanda de esa fila
        for x in range(i, i + tamaño_barco):
            if sum(tablero[x][k] != 0 for k in range(m)) + 1 > demanda_fila[x]:
                return True

    return False

def calcular_posibles_posiciones(tablero, tamaño_barco, demanda_fila, demanda_columna):
    n = len(tablero)
    m = len(tablero[0])
    posiciones = []

    # Verificar posiciones horizontales
    for i in range(n):
        for j in range(m - tamaño_barco + 1):
            # Verifica si las celdas horizontales están libres
            if all(tablero[i][j + k] == 0 for k in range(tamaño_barco)):
                # Comprobar que al ubicar el barco no se excedan las demandas de fila y columnas
                if (sum(tablero[i][k] != 0 for k in range(m)) + tamaño_barco <= demanda_fila[i] and
                    all(sum(tablero[r][j + k] != 0 for r in range(n)) + 1 <= demanda_columna[j + k] for k in range(tamaño_barco))):
                    posiciones.append(((i, j), 'horizontal'))

    # Verificar posiciones verticales
    for i in range(n - tamaño_barco + 1):
        for j in range(m):
            # Verifica si las celdas verticales están libres
            if all(tablero[i + k][j] == 0 for k in range(tamaño_barco)):
                # Comprobar que al ubicar el barco no se excedan las demandas de fila y columnas
                if (sum(tablero[k][j] != 0 for k in range(n)) + tamaño_barco <= demanda_columna[j] and
                    all(sum(tablero[i + k][c] != 0 for c in range(m)) + 1 <= demanda_fila[i + k] for k in range(tamaño_barco))):
                    posiciones.append(((i, j), 'vertical'))

    return posiciones


def marcar_barco_en_tablero(tablero, nro_barco, largo_barco, posicion):
    if posicion == None:
        return tablero

    x, y = posicion[0]
    orientacion = posicion[1]
    nuevo_tablero = copy.deepcopy(tablero)

    if orientacion == "horizontal":
        for j in range(y, y + largo_barco):
            nuevo_tablero[x][j] = nro_barco
    
    elif orientacion == "vertical":
        for i in range(x, x + largo_barco):
            nuevo_tablero[i][y] = nro_barco

    return nuevo_tablero


def es_tablero_valido(tablero):
    n = len(tablero)
    m = len(tablero[0])

    # Comprobar que no haya barcos en posiciones diagonales
    for i in range(n):
        for j in range(m):
            if tablero[i][j] != 0:
                # Comprobar las diagonales
                if (i > 0 and j > 0 and tablero[i-1][j-1] != 0) or \
                   (i > 0 and j < m-1 and tablero[i-1][j+1] != 0) or \
                   (i < n-1 and j > 0 and tablero[i+1][j-1] != 0) or \
                   (i < n-1 and j < m-1 and tablero[i+1][j+1] != 0):
                    return False

    # Comprobar que no haya barcos contiguos
    for i in range(n):
        for j in range(m):
            if tablero[i][j] != 0:
                # Comprobar en las celdas adyacentes si hay 2 barcos distintos
                if (i > 0 and tablero[i-1][j] > 0 and tablero[i-1][j] != tablero[i][j]) or \
                   (i < n-1 and tablero[i+1][j] > 0 and tablero[i+1][j] != tablero[i][j]) or \
                   (j > 0 and tablero[i][j-1] > 0 and tablero[i][j-1] != tablero[i][j]) or \
                   (j < m-1 and tablero[i][j+1] > 0 and tablero[i][j+1] != tablero[i][j]):
                    return False

    return True

def batalla_naval_bt(tablero, barcos, demanda_fila, demanda_columna, mejor_demanda_inc, indice, mejor_tablero):
    # Caso base: si hemos intentado colocar todos los barcos
    if indice >= len(barcos):
        # Calcular la demanda incumplida para esta configuración
        demanda_inc_actual = calcular_demanda_incumplida(tablero, demanda_fila, demanda_columna)
        if demanda_inc_actual < mejor_demanda_inc:
            mejor_demanda_inc = demanda_inc_actual
            mejor_tablero[:] = [fila[:] for fila in tablero]  # Copia profunda del tablero actual
        return mejor_tablero, mejor_demanda_inc

    # Caso recursivo: intentamos todas las posiciones válidas para el barco actual
    barco_actual = barcos[indice]

    for posicion in calcular_posibles_posiciones(tablero, barco_actual, demanda_fila, demanda_columna):
        # Copiamos el tablero antes de realizar cambios
        tablero_temporal = [fila[:] for fila in tablero]
        # Colocamos el barco en la posición actual
        tablero_temporal = marcar_barco_en_tablero(tablero_temporal, indice + 1, barco_actual, posicion)

        # Si el tablero es válido, continuamos con el siguiente barco
        if es_tablero_valido(tablero_temporal):
            # Llamada recursiva para el siguiente barco
            mejor_tablero, mejor_demanda_inc = batalla_naval_bt(
                tablero_temporal, barcos, demanda_fila, demanda_columna, mejor_demanda_inc, indice + 1, mejor_tablero
            )

    # Opción de no colocar el barco actual (es decir, omitirlo)
    mejor_tablero, mejor_demanda_inc = batalla_naval_bt(
        tablero, barcos, demanda_fila, demanda_columna, mejor_demanda_inc, indice + 1, mejor_tablero
    )

    return mejor_tablero, mejor_demanda_inc


def bt(demanda_fila, demanda_columna, barcos):
    tablero = crear_tablero_vacio(len(demanda_fila), len(demanda_columna))
    return batalla_naval_bt(tablero, barcos, demanda_fila, demanda_columna, 10000, 0, tablero)


def crear_tablero_vacio(n, m):
    tablero = []
    for i in range(n):
        fila = [0] * m 
        tablero.append(fila)

    return tablero

if __name__ == "__main__":

    barcos = [1,2,2,2,2,1]

    tablero = crear_tablero_vacio(5,5)

    demanda_fila = [3,3,0,1,1]
    demanda_columna = [3,1,0,3,3]

    info = batalla_naval_bt(tablero, barcos, demanda_fila, demanda_columna, 100000, 0, tablero)
    mostrar_tablero(info[0])
    print(f"Demanda incumplida: {info[1]}")
    