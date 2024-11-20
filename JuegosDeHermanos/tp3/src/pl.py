from pulp import LpProblem, LpVariable, LpBinary, LpInteger, lpSum, LpMinimize, value

def solve_ship_placement(n, m, k, barcos, demandas_filas, demandas_columnas):
    """   
    n: numero de filas.
    m: numero de columnas.
    k: numero de barcos.
    barcos: longitudes de cada barco.
    demandas_filas: demandas de las filas.
    demandas_columnas: demandas de las columnas.
    """
    # Crear el problema
    problema = LpProblem("Batalla naval individual", LpMinimize)

    # Variables de decisión
    x = LpVariable.dicts("x", ((i, j, b, o) for i in range(n) for j in range(m) for b in range(k) for o in [0, 1]), cat=LpBinary)
    u = LpVariable.dicts("u", (i for i in range(n)), lowBound=0, cat=LpInteger)  # demanda incumplida en filas
    v = LpVariable.dicts("v", (j for j in range(m)), lowBound=0, cat=LpInteger)  # demanda incumplida en columnas

    # Funcion objetivo: minimizar demanda incumplida
    problema += lpSum(u[i] for i in range(n)) + lpSum(v[j] for j in range(m)), "Minimizar_Demanda_Incumplida"

    # Restricciones de demanda en filas
    for i in range(n):
        problema += (
            lpSum(
                x[i, j, b, 0] * barcos[b] for j in range(m) for b in range(k) if j + barcos[b] <= m
            ) +
            lpSum(
                x[i - l, j, b, 1] for j in range(m) for b in range(k) for l in range(barcos[b]) if 0 <= i - l < n
            ) +
            u[i] == demandas_filas[i]
        ), f"Demanda_Fila_{i}"

    # Restricciones de demanda en columnas
    for j in range(m):
        problema += (
            lpSum(
                x[i, j, b, 1] * barcos[b] for i in range(n) for b in range(k) if i + barcos[b] <= n
            ) +
            lpSum(
                x[i, j - l, b, 0] for i in range(n) for b in range(k) for l in range(barcos[b]) if 0 <= j - l < m
            ) +
            v[j] == demandas_columnas[j]
        ), f"Demanda_Columna_{j}"

    # Restriccion: los barcos no pueden ser ubicados en una posicion donde puedan superar los limites del tablero
    for b in range(k):
        for i in range(n):
            for j in range(m):
                if j + barcos[b] > m:
                    problema += x[i, j, b, 0] == 0, f"Límite_Horizontal_{i}_{j}_{b}"
                if i + barcos[b] > n:
                    problema += x[i, j, b, 1] == 0, f"Límite_Vertical_{i}_{j}_{b}"

    # Restriccion: cada barco solo puede ser ubicado en una posicion con una orientacion
    for b in range(k):
        problema += (
            lpSum(x[i, j, b, o] for i in range(n) for j in range(m) for o in [0, 1]) <= 1
        ), f"Unicidad_Barco_{b}"

    # Restriccio: evitar ubicar barcos contiguos y en diagonal
    for i in range(n):
        for j in range(m):
            for b in range(k):
                for o in [0, 1]:
                    if o == 0:  # Barco horizontal
                        if j + barcos[b] <= m:
                            for l in range(barcos[b]):
                                for di, dj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                                    ni, nj = i + di, j + l + dj
                                    if 0 <= ni < n and 0 <= nj < m:
                                        problema += x[i, j, b, o] + lpSum(x[ni, nj, b2, o2] for b2 in range(k) for o2 in [0, 1]) <= 1
                    elif o == 1:  # Barco vertical
                        if i + barcos[b] <= n:
                            for l in range(barcos[b]):
                                for di, dj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                                    ni, nj = i + l + di, j + dj
                                    if 0 <= ni < n and 0 <= nj < m:
                                        problema += x[i, j, b, o] + lpSum(x[ni, nj, b2, o2] for b2 in range(k) for o2 in [0, 1]) <= 1

    # Resolver el modelo
    problema.solve()

    # Resultados
    resultado = {
        "status": problema.status,
        "barcos": [],
        "incumplida_filas": {i: u[i].varValue for i in range(n)},
        "incumplida_columnas": {j: v[j].varValue for j in range(m)},
    }

    # Crear tablero
    tablero = [[0 for _ in range(m)] for _ in range(n)]
    for b in range(k):
        for i in range(n):
            for j in range(m):
                for o in [0, 1]:
                    if value(x[i, j, b, o]) > 0:
                        resultado["barcos"].append((i, j, b, "horizontal" if o == 0 else "vertical"))
                        if o == 0:  # Horizontal
                            for l in range(barcos[b]):
                                if j + l < m:  # Validar límite horizontal
                                    tablero[i][j + l] = b + 1
                        elif o == 1:  # Vertical
                            for l in range(barcos[b]):
                                if i + l < n:  # Validar límite vertical
                                    tablero[i + l][j] = b + 1
    resultado["tablero"] = tablero
    return resultado

barcos = [1, 2, 2, 2, 2, 1]
demandas_filas = [3, 3, 0, 1, 1]
demandas_columnas = [3, 1, 0, 3, 3]

resultado = solve_ship_placement(len(demandas_filas), len(demandas_columnas), len(barcos), barcos, demandas_filas, demandas_columnas)
print("Tablero final:")
for fila in resultado["tablero"]:
    print(" ".join(map(str, fila)))
print("\nResultado completo:")
print(resultado)
