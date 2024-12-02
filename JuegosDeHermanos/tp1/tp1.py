def greedy(monedas):
    gananciaS= 0
    gananciaM= 0

    acciones = []

    turno = 0 # 0: Sophia, 1: Mateo    
    while len(monedas) > 0:
        
        if turno == 0:
            if monedas[0] > monedas[-1]:
                gananciaS += monedas.pop(0)
                acciones.append("Primera moneda para Sophia")
            else:
                gananciaS += monedas.pop(-1)
                acciones.append("Ultima moneda para Sophia")
        else:
            if monedas[0] > monedas[-1]:
                gananciaM += monedas.pop(-1)
                acciones.append("Ultima moneda para Mateo")
            else:
                gananciaM += monedas.pop(0)
                acciones.append("Primera moneda para Mateo")
        
        turno = 1 - turno
             
    print(acciones)
    print(f"Ganancia Sofia: {gananciaS} - Ganancia Mateo: {gananciaM}")
