import os


def pruebas(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as archivo:
            contenido = archivo.read()
            
            # Dividir el contenido por ';' y filtrar comentarios
            valores = [int(valor.strip()) for valor in contenido.split(";") if not valor.strip().startswith("#")]
    
        return valores
            
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo {ruta_archivo} no fue encontrado.")


def pruebas_tp3(ruta_archivo):

    try:
        with open(ruta_archivo, 'r') as file:
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
        raise FileNotFoundError(f"El archivo {ruta_archivo} no fue encontrado.")