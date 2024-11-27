import sys
import cargarpruebas
from tp1.tp1 import greedy
from tp2.tp2 import pd
from tp3.src.backtracking import bt
from tp3.src.pl import pl
from tp3.src.approx import ap

def mostrar_tablero(tablero):
    for i in range(len(tablero)):
        fila = []
        for j in range(len(tablero[0])):
            valor = tablero[i][j]
            fila.append(str(int(valor)))
        print(" ".join(fila))


if len(sys.argv) <2:
    print("Uso: python pruebas.py <metodo> <ruta_archivo>")
    print("Metodos disponibles: greedy, pd, bt, pl, ap")
    sys.exit(1)

#Ejecutar una prueba especifica
nombre_funcion = sys.argv[1]
ruta_archivo_pruebas = sys.argv[2]

try:
    # Selecciona la función y carpeta de prueba basada en el argumento
    if nombre_funcion == "greedy":

        valores = cargarpruebas.pruebas(ruta_archivo_pruebas)

        greedy(valores)

    elif nombre_funcion == "pd":
        valores = cargarpruebas.pruebas(ruta_archivo_pruebas)
        pd(valores)

    elif nombre_funcion == "bt":
        campos = cargarpruebas.pruebas_tp3(ruta_archivo_pruebas)
        res = bt(campos[0], campos[1], campos[2])
        mostrar_tablero(res[0])
        print(f"Demanda cumplida: {sum(campos[0]) + sum(campos[1]) - res[1]}")
        print(f"Demanda total: {sum(campos[0]) + sum(campos[1])}")

    elif nombre_funcion == "pl":
        campos = cargarpruebas.pruebas_tp3(ruta_archivo_pruebas)
        res = pl(campos[0], campos[1], campos[2])
        mostrar_tablero(res[0])
        print(f"Demanda cumplida: {sum(campos[0]) + sum(campos[1]) - res[1]}")
        print(f"Demanda total: {sum(campos[0]) + sum(campos[1])}")
    
    elif nombre_funcion == "ap":
        campos = cargarpruebas.pruebas_tp3(ruta_archivo_pruebas)
        res = ap(campos[0], campos[1], campos[2])
        mostrar_tablero(res[0])
        print(f"Demanda cumplida: {sum(campos[0]) + sum(campos[1]) - res[1]}")
        print(f"Demanda total: {sum(campos[0]) + sum(campos[1])}")

    else:
        print("Función no reconocida. Las opciones son: greedy, pd, bt, pl, ap")

except FileNotFoundError as e:
    print(e)
