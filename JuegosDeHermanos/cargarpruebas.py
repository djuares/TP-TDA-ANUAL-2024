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

def pruebas_tp3(nombre_archivo, carpeta):
    ruta_prueba = os.path.join(carpeta, nombre_archivo)

    try:
        with open(ruta_prueba, 'r') as file:
            secciones = []
            seccion_actual = []
            
            for linea in file:
                # Ignorar líneas en blanco y líneas que comienzan con '#'
                linea = linea.strip()
                if linea.startswith('#'):
                    continue
                
                # Si encontramos una línea en blanco después de una sección, guardamos la sección
                if linea == "":
                    if seccion_actual:
                        secciones.append(seccion_actual)
                        seccion_actual = []
                else:
                    seccion_actual.append(int(linea))
            
            # Agregar la última sección, si existe
            if seccion_actual:
                secciones.append(seccion_actual)
            
            # Separar cada sección en variables correspondientes
            demanda_fila = secciones[0]
            demanda_columna = secciones[1]
            largos_barcos = secciones[2]

            return demanda_fila, demanda_columna, largos_barcos
        
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo {nombre_archivo} no fue encontrado en la carpeta '{carpeta}'.")