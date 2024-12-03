def pd(monedas):
    n = len(monedas)
    # Crear tabla bidimensional para almacenar los resultados
    dp = [[0] * n for _ in range(n)]
    decisiones = [[None] * n for _ in range(n)]  # Para guardar las decisiones tomadas

    # Llenar la tabla base: casos con una sola moneda
    for i in range(n):
        dp[i][i] = monedas[i]

    # Llenar la tabla para rangos crecientes de tamaño
    for longitud in range(2, n + 1):            # Tamaño del subarreglo 
        for inicio in range(n - longitud + 1):  # Inicio del rango
            fin = inicio + longitud - 1         # Fin del rango   

            # Calcular la mejor elección para el rango [inicio, fin]
            elegir_inicio = monedas[inicio] + max(
                dp[inicio + 2][fin] if (inicio + 2 <= fin) and (monedas[inicio+1]>monedas[fin]) else 0,
                dp[inicio + 1][fin - 1] if (inicio ++ 1 <= fin - 1) and (monedas[inicio+1]<monedas[fin])else 0,
            )
            elegir_fin = monedas[fin] + max(
                dp[inicio][fin - 2] if (inicio <= fin - 2) and (monedas[inicio]< monedas[fin-1])  else 0,
                dp[inicio + 1][fin - 1] if (inicio + 1) <= fin - 1 and (monedas[inicio]>monedas[fin-1]) else 0,
            )
            dp[inicio][fin] = max(elegir_inicio,  elegir_fin )

             # Guardar la mejor opción y la decisión tomada
            if elegir_inicio > elegir_fin:
                dp[inicio][fin] = elegir_inicio
                decisiones[inicio][fin] = 'inicio'  # Elegir la moneda del inicio
            else:
                dp[inicio][fin] = elegir_fin
                decisiones[inicio][fin] = 'fin'  # Elegir la moneda del final

    # El resultado está en dp[0][n-1], considerando todas las monedas
    
    print(f"Ganancia Sofia: {dp[0][n-1]} \nGanancia Mateo: {sum(monedas)-dp[0][n-1]}")







