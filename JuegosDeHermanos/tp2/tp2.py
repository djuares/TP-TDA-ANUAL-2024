def pd(monedas):
    n = len(monedas)
    dp = [[0] * n for _ in range(n)]
    
    # Llenamos la tabla `dp` de abajo hacia arriba
    for length in range(1, n + 1):       #longitud del intervalo
        for i in range(n - length + 1):  #inicio del intervalo
            j = i + length - 1           #final del intervalo
            
            if i == j:                   #caso base, una sola moneda
                dp[i][j] = monedas[i]
            else:
                # Maximizar ganancia al elegir la primera o la última moneda
                elegir_primera = monedas[i] + min(dp[i + 2][j] if i + 2 <= j else 0,
                                                  dp[i + 1][j - 1] if i + 1 <= j - 1 else 0)
                elegir_ultima = monedas[j] + min(dp[i + 1][j - 1] if i + 1 <= j - 1 else 0,
                                                 dp[i][j - 2] if i <= j - 2 else 0)
                dp[i][j] = max(elegir_primera, elegir_ultima)

    # La ganancia de Sofía está en dp[0][n-1]
    gananciaS = dp[0][n - 1]
    gananciaM = sum(monedas) - gananciaS

    print("Ganancia Sofía: {}\nGanancia Mateo: {}".format(gananciaS, gananciaM))



