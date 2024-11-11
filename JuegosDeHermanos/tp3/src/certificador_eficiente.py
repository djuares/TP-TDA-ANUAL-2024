def chequeo_barcos_diagonales(tablero):
    n = len(tablero)
    m = len(tablero[0])

    for i in range(n):
        for j in range(m):

            if tablero[i][j] == 1:

                # Superior izq
                if i > 0 and j > 0 and tablero[i-1][j-1] == 1:
                    return False
                
                # Superior der
                if i > 0 and j < m-1 and tablero[i-1][j+1] == 1:
                    return False

                # Inferior izq
                if i < n-1 and j > 0 and tablero[i+1][j-1] == 1:
                    return False
                
                if i < n-1 and j < m-1 and tablero[i+1][j+1] == 1:
                    return False
    
    return True

def chequear_barcos(tablero, barcos):
    n = len(tablero)
    m = len(tablero[0])

    for i in range(n):
        for j in range(m):

            if len(barcos) == 0:
                break

            if tablero[i][j] == 1:
                largo_barco = 1
                tablero[i][j] = 0
                # Barco horizontal
                if j < m-1 and tablero[i][j+1] == 1:
                    while j < m-1:
                        if tablero[i][j+1] == 1:
                            largo_barco += 1
                            tablero[i][j+1] = 0
                            j += 1 
                        else:
                            break
                
                # Barco vertical
                elif i < n-1 and tablero[i+1][j] == 1:
                    while i < n-1:
                        if tablero[i+1][j] == 1:
                            largo_barco += 1
                            tablero[i+1][j] = 0
                            i += 1
                        else:
                            break
                
                if barcos.count(largo_barco) > 0:
                    barcos.remove(largo_barco)
                else:
                    # No existe un barco con esa longitud
                    return False
    
    # Quedaron barcos sin asignar al tablero
    if len(barcos) != 0:
        return False

    return True

def certificador_eficiente(tablero, barcos, requisitos_fil, requisitos_col):
    
    # Chequeo barcos diagonales -> O(nxm)
    if chequeo_barcos_diagonales(tablero) == False:
        return False

    # Chequeo requisitos de fila -> O(nxm)
    for i in range(len(tablero)):
        if tablero[i].count(1) != requisitos_fil[i]:
            return False
        
    # Chequeo requisitos de columna -> O(nxm)
    for j in range(len(tablero[0])):
        sum_j = sum(fila[j] for fila in tablero)
        if (sum_j != requisitos_col[j]):
            return False
    
    # Chequeo barcos asignados correctamente -> O(nxm)
    if chequear_barcos(tablero, barcos) == False:
        return False

    return True


def crear_tablero_fijo():
    tablero = [
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    ]
    return tablero

if __name__ == "__main__":

    tamaños_barcos = [4, 3, 3, 3, 3, 1, 1]

    tablero = crear_tablero_fijo()
   
    requisitos_fil = [1,5,1,0,4,1,1,3,0,2]
    requisitos_col = [2,1,2,4,2,0,1,4,1,1]

    print(certificador_eficiente(tablero, tamaños_barcos, requisitos_fil, requisitos_col))
