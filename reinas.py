import random 
import os
import time
from collections import deque
from turtle import pos

from lab.utils import Moves

def clear():
    os.system('cls' if os.name == "nt" else 'clear')


def read_int(prompt, minv=4):
    while True:
        try:
            v = int(input(prompt))
            if v < minv:
                print(f"Ingrese un número >= {minv}")
                continue
            return v
        except ValueError:
            print("Entrada Inválida.")





def cant_Q(tablero):
    cant=0
    posiciones = set()
    atacados= set()
    
    for i in range(len(tablero)):
        if  "Q" in tablero[i]:
            cant+=1
            posiciones.add((i,tablero.index("Q")))
            atacados.add((i,tablero.index("Q")))
    return cant,posiciones,atacados
# ===================== BFS =====================
def bfs(tablero,inicio):
    rows = len(tablero)
    cols = len(tablero[0])
    reinas= set (inicio)
    queue = deque()
    queue.append((tablero, reinas))
    atacados = set()

    while queue:
        tab, reinas_tab = queue.popleft()
        #cantidad_q,posiciones_reinas, atacados= cant_Q(tab)
                    
        if reinas_tab == len(tab):
            return True
        
        rows = len(tablero)
        cols = len(tablero[0])
        #r, f = inicio  # Fila y columna de la Reina
        
        


        for n in range(rows):
            barrido= 0
            for c in range(cols):
                # 1. Posición de la Reina
                if (n,c) in reinas_tab:
                    visitados.add((n,c))
                # 2. Misma fila o misma columna
                elif n == r or c == f:
                    linea += "[-]"
                    visitados.add((n,c))
                # 3. Misma diagonal (La magia de las matemáticas)
                elif abs(n - r) == abs(c - f):
                    linea += "[-]"
                    visitados.add((n,c))
                # 4. Espacio vacío
                else:
                    linea += "[ ]"
            print(linea)

    return False, []

from collections import deque

def es_seguro(reinas_actuales, nueva_reina):
    """
    Comprueba si la nueva_reina es atacada por las reinas que ya están en el tablero.
    """
    r_nueva, c_nueva = nueva_reina
    for r, c in reinas_actuales:
        # Misma columna o misma diagonal
        if c == c_nueva or abs(r - r_nueva) == abs(c - c_nueva):
            return False
    return True

def resolver_n_reinas_bfs(n, pos_inicial=None):
    queue = deque()
    if pos_inicial:
        # Si hay una reina fija, empezamos con ella
        queue.append([pos_inicial])
        filas_ocupadas = {pos_inicial[0]}
    else:
        # Si no hay fija, empezamos con un tablero vacío
        queue.append([])
        filas_ocupadas = set()

    soluciones = []

    while queue:
        tablero_actual = queue.popleft()
        
        # Condición de victoria: si tenemos N reinas, es una solución
        if len(tablero_actual) == n:
            soluciones.append(tablero_actual)
            continue # Buscamos más soluciones en la cola

        # Determinamos qué fila toca llenar
        # Buscamos la primera fila que no esté en el tablero_actual
        filas_en_este_tablero = {r for r, c in tablero_actual}
        fila_objetivo = 0
        while fila_objetivo in filas_en_este_tablero:
            fila_objetivo += 1
            
        # Intentamos colocar una reina en cada columna de la fila_objetivo
        for col in range(n):
            nueva_pos = (fila_objetivo, col)
            if es_seguro(tablero_actual, nueva_pos):
                # Importante: Creamos una copia del camino actual + la nueva reina
                nuevo_tablero = tablero_actual + [nueva_pos]
                queue.append(nuevo_tablero)

    return filas_en_este_tablero

# Ejemplo: Tablero de 4x4 con reina fija en (2,0)
n = 4
pos_fija = (2, 0)
resultados = resolver_n_reinas_bfs(n, pos_fija)

print(f"Soluciones encontradas: {len(resultados)}")
for i, sol in enumerate(resultados):
    print(f"Solución {i+1}: {sol}")


def generar_tablero(rows,inicio=None):

    tablero = [[0 for _ in range(rows)] for _ in range(rows)]
    if inicio:
        tablero[inicio[0]][inicio[1]]= " Q "
    return tablero

def imprimir_tablero(tablero):
    #path = path or []
    rows = len(tablero)
    cols = len(tablero[0])

    for r in range(rows):
        fila=""
        for c in range(cols):    
            fila +=tablero[r][c]
            
        print(fila)




def bfs_mi(tablero):
    queue = deque()
    queue.append(tablero)

    while queue:
        tablero_actual = queue.popleft()

        if contar_r(tablero_actual)[1] == len(tablero_actual):
            return True, tablero
        
        fila_inicio=0
        for pos in contar_r(tablero_actual)[2]:
            if fila_inicio==pos[0]:
                fila_inicio+=1

        for c in range(len(tablero_actual)):
            fila_inicio+=1
            nuevo = [fila[:] for fila in tablero_actual]
            if es_seguro(contar_r(tablero_actual)[2],(fila_inicio,c)):
                nuevo[fila_inicio][c] = " Q "
                queue.append(nuevo)
            imprimir_tablero(nuevo)    




    return False, "no se encontro solucion"


def es_seguro(reinas,new_reina):
    r, c = new_reina
    for i in reinas:
        if ((r, c) == i ) or (r == i[0] or c == i[1]) or (abs(r - i[0]) == abs(c - i[1])):
                    return False

    return True            


def contar_r(tablero):
    cant=0
    posiciones = set()
    atacados= set()
    
    for i in range(len(tablero)):
        if  " Q " in tablero[i]:
            cant+=1
            c=tablero[i].index(" Q ")
            posiciones.add((i,c))
            atacados.add((i,c))

    for f in posiciones:

        for n in range(len(tablero)):
            barrido= 0
            for c in range(len(tablero)):
                if (n,c)== f:
                    continue
                elif (n == f[0] or c == f[1]) or (abs(n - f[0]) == abs(c - f[1])):
                    atacados.add((n,c))
                    tablero[n][c]="[-]"
                else:
                    tablero[n][c]="[ ]"
    
    return [tablero,cant,posiciones,atacados]
            

# Ejemplo de uso con un tablero de 8x8

def main():
    print("--- Laberinto con BFS, DFS y LDFS ---")
    rows = read_int("Ingrese el numero de filas: ", 4)
    tablero = generar_tablero(rows,(0,0))
    print(bfs_mi(tablero))
    #success, path = bfs(tablero, inicio, meta, movimientos)
    
if __name__ == "__main__":
    main()    