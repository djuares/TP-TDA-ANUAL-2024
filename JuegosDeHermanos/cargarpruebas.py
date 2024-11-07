import os

def pruebas(nombre_archivo, carpeta):
    ruta_prueba = os.path.join(carpeta, nombre_archivo)
    try:
        with open(ruta_prueba, 'r') as archivo:
            contenido = archivo.read()
            valores = [int(valor) for valor in contenido.split(';')[1:]]  # Divide y limpia espacios
            return valores
            
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo {nombre_archivo} no fue encontrado en la carpeta '{carpeta}'.")
