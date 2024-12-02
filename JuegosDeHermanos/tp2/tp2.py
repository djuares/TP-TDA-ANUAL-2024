def pd2(monedas):
    #guardar los valor maximos para cada sublista
    #ganancia=[]
    #for i in range(len(monedas)+1):
     #   ganancia+=[float('-inf')]

    n= len(monedas)
    ganancia = [[-1] * (n+1) for _ in range(n+1)]
    return pd_aux(monedas, 0, len(monedas)-1, len(monedas),ganancia )



def pd3(monedas):
    n = len(monedas)
    # Crear tabla bidimensional para memoización
    ganancia = [[-1] * n for _ in range(n)]
    
    # Calcular la ganancia máxima
    max_ganancia = pd_aux(monedas, 0, n - 1, ganancia)
    return max_ganancia

def pd(monedas):
    n = len(monedas)
    # Crear tabla bidimensional para almacenar los resultados
    dp = [[0] * n for _ in range(n)]

    # Llenar la tabla base: casos con una sola moneda
    for i in range(n):
        dp[i][i] = monedas[i]

    # Llenar la tabla para rangos crecientes de tamaño
    for longitud in range(2, n + 1):  # Tamaño del subarreglo 
        for inicio in range(n - longitud + 1):  # Inicio del rango
            fin = inicio + longitud - 1  # Fin del rango   
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
     

    # El resultado está en dp[0][n-1], considerando todas las monedas
    return print(dp [0][n-1])


def pd_aux3(monedas, inicio, fin, ganancia):
    # Caso base: Si ya no hay monedas
    if inicio > fin:
        return 0

    # Si ya se calculó este rango, devolver el resultado almacenado
    if ganancia[inicio][fin] != -1:
        return ganancia[inicio][fin]

    # Elegir la moneda del inicio o la del final
    elegir_inicio = monedas[inicio] + min(
        pd_aux(monedas, inicio + 2, fin, ganancia),  # Oponente elige inicio
        pd_aux(monedas, inicio + 1, fin - 1, ganancia)  # Oponente elige fin
    )
    
    elegir_fin = monedas[fin] + min(
        pd_aux(monedas, inicio + 1, fin - 1, ganancia),  # Oponente elige inicio
        pd_aux(monedas, inicio, fin - 2, ganancia)  # Oponente elige fin
    )

    # Almacenar el resultado en la tabla
    ganancia[inicio][fin] = max(elegir_inicio, elegir_fin)
    return ganancia[inicio][fin]

def pd_aux2(monedas,inicio, final,  n, ganancia):
    #Ganancia para esta longitud ya esta calculada?
    if ganancia[inicio][final]>=0:
        return ganancia[inicio][final]
    
    if n==0:
        q=0
    elif n==1:
        q=0

    else:
        q= float('-inf')
        if n>= 2 and n<len(ganancia)-1:
            if monedas[inicio]>monedas[final]:
                inicio+=1
            else:
                final-=1
            n-=1
        q= max(q, monedas[inicio]+ pd_aux(monedas, inicio+1, final, n-1, ganancia), monedas[final]+ pd_aux(monedas,inicio, final-1 ,n-1, ganancia))
    ganancia[inicio][final]=q
    return q


def pd_4(monedas):
    n= len(monedas)
    # Crear tabla bidimensional para almacenar los resultados
    dp = [[0] * (n+1) for _ in range(n)]

    for j in range(len(monedas),-1):
        q= float('-inf')
        for i in range(len):

            if n>= 2 and n<len(monedas)-1:
                if monedas[i]>monedas[j]:
                    i+=1
                    n-=1
            else:
                    j-=1
                    n-=1
            n-=1
            q= max(q, monedas[i]+ dp[i+1][j], monedas[j]+dp[i][j-1])
        dp[i][j]= q
    return print(dp)

