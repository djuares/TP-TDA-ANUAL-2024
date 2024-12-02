def greedy(monedas):
    n= len(monedas)
    inicio= 0
    final=len(monedas)-1

    acciones = [[], []]

    turno = 0 # 0: Sophia, 1: Mateo    
    while n > 0:
        
        if turno == 0:
            if monedas[inicio] > monedas[final]:
                acciones[0].append(monedas[inicio])
                inicio+=1
            else:
                acciones[0].append(monedas[final])
                final-=1

        else:
            if monedas[inicio] > monedas[final]:
                acciones[1].append(monedas[final])
                final-=1
            else:
                acciones[1].append(monedas[inicio])
                inicio+=1
        n-=1
        
        turno = 1 - turno
             
    print(f"Ganancia Sofia: {sum(acciones[0])} - Monedas: {acciones[0]} \n")
    print(f"Ganancia Mateo: {sum(acciones[1])} - Monedas: {acciones[1]}")