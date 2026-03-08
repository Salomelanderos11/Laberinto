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


def generar_tablero(rows,inicio=None):

    tablero = [["[ ]" for _ in range(rows)] for _ in range(rows)]
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
            fila += tablero[r][c]
            
        print(fila)

def preguntar_posicion(prompt, rows):
    while True:
        try:
            text = input(prompt + " (fila,col): ")
            r, c = map(int, text.split(","))
            # Se valida que la posición ingresada esté dentro de los límites del tablero
            if 0 <= r < rows and 0 <= c < cols:
                return(r, c)
        except:
            pass
        print("Posicion invalida.")


def bfs_mi(tablero):
    queue = deque()
    queue.append((tablero,[tablero]))

    while queue:
        tablero_actual, path = queue.popleft()
        # Una sola llamada para obtener todo
        cant_actual, pos_actual= contar_reinas(tablero_actual)

        if cant_actual == len(tablero_actual):
            return True,path

        # Buscar la siguiente fila
        fila_objetivo = 0
        filas_ocupadas = {p[0] for p in pos_actual}
        while fila_objetivo in filas_ocupadas:
            fila_objetivo += 1

        if fila_objetivo < len(tablero_actual):
            for c in range(len(tablero_actual)):
                if es_seguro(pos_actual, (fila_objetivo, c)):
                    nuevo = [fila[:] for fila in tablero_actual]
                    nuevo[fila_objetivo][c] = " Q "
                    
                    # Verificamos victoria aquí para ahorrar memoria
                    nuevo_camino = path + [nuevo]
                    
                    if contar_reinas(nuevo)[1] == len(nuevo):
                        tab_fin = contar_reinas(nuevo)[0]
                        print("¡SOLUCIÓN FINAL ENCONTRADA!")

                        #imprimir_tablero(tab_fin)
                        return True, nuevo_camino
                    queue.append((nuevo, nuevo_camino))
                  
                    # ¡NO IMPRIMIR AQUÍ PARA N=10!
                       




    return False, "no se encontro solucion"


def dfs_mi(tablero_actual, camino):
    #queue = deque()
    #queue.append(tablero)


   # tablero_actual = queue.pop()
    # Una sola llamada para obtener todo
    cant_actual, pos_actual= contar_reinas(tablero_actual)
    camino.append(tablero_actual)

    if cant_actual == len(tablero_actual):
        print("¡SOLUCIÓN FINAL ENCONTRADA!")
        #imprimir_tablero(tablero_actual)
        return True, camino

    # Buscar la siguiente fila
    fila_objetivo = 0
    filas_ocupadas = {p[0] for p in pos_actual}
    while fila_objetivo in filas_ocupadas:
        fila_objetivo += 1

    #if fila_objetivo < len(tablero_actual):
    for c in range(len(tablero_actual)):
        if es_seguro(pos_actual, (fila_objetivo, c)):
            nuevo = [fila[:] for fila in tablero_actual]
            nuevo[fila_objetivo][c] = " Q "
            exito, resultado_final = dfs_mi(nuevo, list(camino))
            # Verificamos victoria aquí para ahorrar memoria
            if exito:
                return True, resultado_final

    return False, []




def ldfs_mi(tablero_actual, camino,limite):

    cant_actual, pos_actual = contar_reinas(tablero_actual)
    nuevo_camino = camino + [tablero_actual]

    if cant_actual == len(tablero_actual):
        print("¡SOLUCIÓN FINAL ENCONTRADA!")
        #imprimir_tablero(tablero_actual)
        return True, nuevo_camino
    
    if limite <= 0:
       return False, []        
       
    # Buscar la siguiente fila
    fila_objetivo = 0
    filas_ocupadas = {p[0] for p in pos_actual}
    while fila_objetivo in filas_ocupadas:
        fila_objetivo += 1

    
    #if fila_objetivo < len(tablero_actual):
    for c in range(len(tablero_actual)):
        if es_seguro(pos_actual, (fila_objetivo, c)):
            nuevo = [fila[:] for fila in tablero_actual]
            nuevo[fila_objetivo][c] = " Q "
            exito, resultado_final = ldfs_mi(nuevo, nuevo_camino,limite-1)
            # Verificamos victoria aquí para ahorrar memoria
            if exito:
                return True, resultado_final

    return False, []



def es_seguro(reinas,new_reina):
    r, c = new_reina
    for i in reinas:
        if ((r, c) == i ) or (r == i[0] or c == i[1]) or (abs(r - i[0]) == abs(c - i[1])):
                    return False

    return True            


def contar_reinas(tablero):
    posiciones = set()
    cant = 0
    for i in range(len(tablero)):
        for j in range(len(tablero)):
            if tablero[i][j] == " Q ":
                cant += 1
                posiciones.add((i, j))
    return [cant, posiciones]
            




def main():
    print("\n--- Solucionador de N-Reinas (BFS, DFS, LDFS) ---")
    print("1 - BFS (Anchura)\n2 - DFS (Profundidad)\n3 - LDFS (Profundidad Limitada)")
    model_option = read_int("Seleccione una opcion: ", 1)
    rows = read_int("Ingrese el numero de reinas (N): ", 4)
    
    print("\n¿Deseas fijar la posición de la primera reina?")
    resp = read_int("1: SI | 2: NO  -> ", 1)
    inicio = preguntar_posicion(f"Posición", rows) if resp == 1 else None

    tablero_inicial = generar_tablero(rows, inicio)
    success, path = False, []

    print(f"\nEjecutando búsqueda... Por favor espere.")
    start_time = time.time()

    if model_option == 1:
        success, path = bfs_mi(tablero_inicial)
    elif model_option == 2:
        success, path = dfs_mi(tablero_inicial, [])
    elif model_option == 3:
        limit = read_int(f"Ingrese el limite de profundidad (Sugerido: {rows}): ", 1)
        success, path = ldfs_mi(tablero_inicial, [], limit)

    end_time = time.time()

    if success:
        print(f"\n¡SOLUCIÓN ENCONTRADA en {end_time - start_time:.4f} segundos!")
        print(f"Pasos recorridos: {len(path)}")
        ver_pasos = read_int("¿Deseas ver la animación? (1: SI | 2: NO): ", 1)
        if ver_pasos == 1:
            for i, paso in enumerate(path):
                print(f"\n--- Paso {i+1} ---")
                imprimir_tablero(paso) # Corregido: imprimir el paso directamente
                time.sleep(0.3)
    else:
        print("\nNo se encontró una solución.")

if __name__ == "__main__":
    main()