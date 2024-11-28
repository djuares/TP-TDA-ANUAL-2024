from pulp import LpProblem, LpVariable, LpBinary, lpSum, LpMinimize, value, LpInteger, PULP_CBC_CMD

def guardar_resultados(n, m, x, u, v, barcos):
    resultado = {"tablero": None, "incumplida_filas": 0, "incumplida_columnas": 0}

    tablero = [[0 for _ in range(m)] for _ in range(n)]
    for b in range(len(barcos)):
        for i in range(n):
            for j in range(m):
                for o in [0, 1]:
                    if (i, j, b, o) in x and value(x[i, j, b, o]) > 0:
                        if o == 0:  # Horizontal
                            for l in range(barcos[b]):
                                if j + l < m:
                                    tablero[i][j + l] = b + 1
                        elif o == 1:  # Vertical
                            for l in range(barcos[b]):
                                if i + l < n:
                                    tablero[i + l][j] = b + 1
    resultado["tablero"] = tablero
    resultado["incumplida_filas"] = {i: u[i].varValue for i in range(n)}
    resultado["incumplida_columnas"] = {j: v[j].varValue for j in range(m)}

    return resultado

def es_posicion_valida(barcos, i, j, b, o, demandas_filas, demandas_columnas, n, m):
    if (o == 0 and j + barcos[b] > m) or (o == 1 and i + barcos[b] > n):
        return False
    
    if (o == 0 and barcos[b] > demandas_filas[i]) or (o == 1 and barcos[b] > demandas_columnas[j]):
        return False
    
    if o == 0:
        for y in range(j, j + barcos[b]):
            if demandas_columnas[y] == 0:
                return False
    else:
        for x in range(i, i + barcos[b]):
            if demandas_filas[x] == 0:
                return False
    
    return True

def batalla_naval_individual_pl(n, m, k, barcos, demandas_filas, demandas_columnas):

    # Crear el problema
    problema = LpProblem("Minimizar_demanda_incumplida", LpMinimize)

    # Variables de decision
    # x -> Barco b en la posición (i, j) y orientación o
    # u -> Demanda incumplida en fila i
    # v -> Demanda incumplida en columna j
    x = LpVariable.dicts(
    "x",
    (
        (i, j, b, o)
        for i in range(n)
        for j in range(m)
        for b in range(k)
        for o in [0, 1]
        if es_posicion_valida(barcos, i, j, b, o, demandas_filas, demandas_columnas, n, m)
    ),
    cat=LpBinary)
    u = LpVariable.dicts("u", (i for i in range(n)), lowBound=0, cat=LpInteger)
    v = LpVariable.dicts("v", (j for j in range(m)), lowBound=0, cat=LpInteger)

    # Funcion objetivo: Minimizar demanda incumplida
    problema += (
        lpSum(u[i] for i in range(n)) + 
        lpSum(v[j] for j in range(m))
    ), "Minimizar_Demanda_Incumplida"

    # Restricciones de demanda en filas
    for i in range(n):
        problema += (
            lpSum(
                x[i, j, b, 0] * barcos[b] for j in range(m) for b in range(k) if (i,j,b,0) in x if j + barcos[b] <= m
            ) +
            lpSum(
                x[i - l, j, b, 1] for j in range(m) for b in range(k) for l in range(barcos[b]) if (i-l,j,b,1) in x if 0 <= i - l < n
            ) +
            u[i] == demandas_filas[i]
        )

    # Restricciones de demanda en columnas
    for j in range(m):
        problema += (
            lpSum(
                x[i, j, b, 1] * barcos[b] for i in range(n) for b in range(k) if (i,j,b,1) in x if i + barcos[b] <= n
            ) +
            lpSum(
                x[i, j - l, b, 0] for i in range(n) for b in range(k) for l in range(barcos[b]) if (i,j-l,b,0) in x if 0 <= j - l < m
            ) +
            v[j] == demandas_columnas[j]
        )


    # Restricciones de unicidad de los barcos
    for b in range(k):
        problema += (
            lpSum(x[i, j, b, o] for i in range(n) for j in range(m) for o in [0, 1] if (i,j,b,o) in x) <= 1
        )

    # Restricciones de no solapamiento
    for i in range(n):
        for j in range(m):
            problema += (
                lpSum(
                    x[i, j, b, o] for b in range(k) for o in [0, 1] if (i,j,b,o) in x
                ) <= 1
            ), f"No_Solapamiento_{i}_{j}"

    # Restricciones para evitar barcos contiguos y diagonales
    for (i, j, b, o) in x:
        if o == 0 and j + barcos[b] <= m:  # Barco horizontal
            for l in range(barcos[b]):
                for di, dj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    ni, nj = i + di, j + l + dj
                    if 0 <= ni < n and 0 <= nj < m:
                        problema += (
                            lpSum(x[ni, nj, b2, o2] for (ni2, nj2, b2, o2) in x if ni2 == ni and nj2 == nj and b2 != b) <= 1 - x[i, j, b, o]
                        )
        elif o == 1 and i + barcos[b] <= n:  # Barco vertical
            for l in range(barcos[b]):
                for di, dj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    ni, nj = i + l + di, j + dj
                    if 0 <= ni < n and 0 <= nj < m:
                        problema += (
                            lpSum(x[ni, nj, b2, o2] for (ni2, nj2, b2, o2) in x if ni2 == ni and nj2 == nj and b2 != b) <= 1 - x[i, j, b, o]
                        )


    # Resolver el modelo
    problema.solve(PULP_CBC_CMD())

    # Resultados
    resultado = guardar_resultados(n, m, x, u, v, barcos)
    return resultado["tablero"], sum(resultado['incumplida_filas'].values()) + sum(resultado['incumplida_columnas'].values())


def pl(demanda_filas, demanda_columnas, barcos):
    n = len(demanda_filas)
    m = len(demanda_columnas)
    k = len(barcos)

    return batalla_naval_individual_pl(n, m, k, barcos, demanda_filas, demanda_columnas)