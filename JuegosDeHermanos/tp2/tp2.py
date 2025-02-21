def pd(monedas):
    n = len(monedas)
    # Crear tabla bidimensional para almacenar los resultados
    dp = [[0] * n for _ in range(n)]

    # Llenar la tabla base: casos con una sola moneda
    for i in range(n):
        dp[i][i] = monedas[i]

    # Llenar la tabla para rangos crecientes de tamaño
    for longitud in range(2, n + 1):            # Tamaño del subarreglo 
        for inicio in range(n - longitud + 1):  # Inicio del rango
            fin = inicio + longitud - 1         # Fin del rango   

            # Calcular la mejor elección para el rango [inicio, fin]

            #Opcion inicio
            if inicio +1 <= fin:
                #Considero las opciones de Mateo
                if monedas[inicio + 1] >= monedas[fin]:
                    if inicio + 2 <= fin:
                        elegir_inicio = monedas[inicio] + dp[inicio + 2][fin]
                    else:
                        elegir_inicio= monedas[inicio]
                else:
                    if inicio + 1 <= fin - 1 :
                        elegir_inicio = monedas[inicio] + dp[inicio + 1][fin - 1]
                    else:
                        elegir_inicio= monedas[inicio]     
            else:
                elegir_inicio= monedas[inicio] 
            
            #Opcion Final
            if inicio <= fin - 1:
                #Considero las opciones de Mateo
                if monedas[inicio] >= monedas[fin - 1]:
                    if inicio + 1 <= fin - 1:
                        elegir_fin = monedas[fin] + dp[inicio + 1][fin - 1]  
                    else:
                        elegir_fin= monedas[fin]
                else:
                    if inicio <= fin - 2:
                        elegir_fin = monedas[fin] + dp[inicio][fin - 2]  
                    else:
                       elegir_fin= monedas[fin]
            else:
                elegir_fin = monedas[fin]


            dp[inicio][fin] = max(elegir_inicio,  elegir_fin )

    # El resultado está en dp[0][n-1], considerando todas las monedas
    
    print(f"Ganancia Sofia: {dp[0][n-1]} \nGanancia Mateo: {sum(monedas)-dp[0][n-1]}")






