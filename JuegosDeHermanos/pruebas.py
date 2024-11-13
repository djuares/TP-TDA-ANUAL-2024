import sys
import cargarpruebas
from tp1.tp1 import greedy
from tp2.tp2 import pd
from tp3.src.backtracking import bt

def mostrar_tablero(tablero):
    for i in range(len(tablero)):
        fila = []
        for j in range(len(tablero[0])):
            valor = tablero[i][j]
            fila.append(str(int(valor)))
        print(" ".join(fila))


if len(sys.argv) <2:
    print("Uso: python pruebas.py <metodo> <prueba>")
    print("Metodos disponibles: greedy, pd, bt")
    sys.exit(1)

#Ejecutar una prueba especifica
nombre_funcion = sys.argv[1]
nombre_archivo = sys.argv[2]

try:
    # Selecciona la función y carpeta de prueba basada en el argumento
    if nombre_funcion == "greedy":

        valores = cargarpruebas.pruebas(nombre_archivo, "pruebas1")

        greedy(valores)

    elif nombre_funcion == "pd":
        valores = cargarpruebas.pruebas(nombre_archivo, "pruebas2")
        pd(valores)

    elif nombre_funcion == "bt":
        campos = cargarpruebas.pruebas_tp3(nombre_archivo, "pruebas3")
        res = bt(campos[0], campos[1], campos[2])
        mostrar_tablero(res[0])
        print(f"Demanda cumplida: {sum(campos[0]) + sum(campos[1]) - res[1]}")
        print(f"Demanda total: {sum(campos[0]) + sum(campos[1])}")

    else:
        print("Función no reconocida. Las opciones son: greedy, pd, bt")

except FileNotFoundError as e:
    print(e)
