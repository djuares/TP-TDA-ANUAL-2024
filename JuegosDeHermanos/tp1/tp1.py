def greedy(monedas):
    gananciaS= 0
    gananciaM= 0
    
    inicio= 0
    fin= len(monedas)-1

    while inicio<=fin:
        
        if fin-inicio >=2:
            if monedas[inicio]> monedas[fin]:
                gananciaS+= monedas[inicio]
                gananciaM+= monedas[fin]
            else:
                gananciaS+= monedas[fin]
                gananciaM+= monedas[inicio]

            inicio+=1
            fin-=1
        else:
            #numero de monedas impar (como empieza sofia y termina ella)
            gananciaS+= monedas[inicio]
            inicio+=1
            fin-=1
             
    print("Ganancia Sofia: {}\nGanancia Mateo: {}".format(gananciaS, gananciaM))





