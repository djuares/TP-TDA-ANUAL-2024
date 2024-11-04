import sys
import cargarpruebas
from tp1.tp1 import greedy
#from tp2.tp2 import pd


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

##    elif nombre_funcion == "pd":
##        valores = cargar_datos(nombre_archivo, pruebas2)
##        pd(valores)

##    elif nombre_funcion == "bt":
##        valores = cargar_datos(nombre_archivo, pruebas3)
##        bt(valores) 
    
    else:
        print("Función no reconocida. Las opciones son: greedy, pd, bt")

except FileNotFoundError as e:
    print(e)
