import random 
import os
import time
from collections import deque

def clear():
    os.system('cls' if os.name == "nt" else 'clear')

Moves = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
    'UL': (-1, -1),
    'UR': (-1, 1),
    'DL': (1, -1),
    'DR': (1, 1)
}

def read_int(prompt, minv=0):
    while True:
        try:
            v = int(input(prompt))
            if v < minv:
                print(f"Ingrese un número >= {minv}")
                continue
            return v
        except ValueError:
            print("Entrada Inválida.")

def preguntar_posicion(prompt, rows, cols):
    while True:
        try:
            # Se pide al usuario que ingrese los movimientos permitidos en el formato "U,D,L,R,UL,UR,DL,DR"
            text = input(prompt + " (fila,col): ")
            r, c = map(int, text.split(","))
            # Se valida que la posición ingresada esté dentro de los límites del tablero
            if 0 <= r < rows and 0 <= c < cols:
                return(r, c)
        except:
            pass
        print("Posicion invalida.")

def calcular_porcentaje_obstaculos(rows, cols):
    size = rows * cols
    pct = size / 2.5
    # se añade el porcentaje de obstáculos de manera automatica y 
    # evalua que no sea mayor a 60% para evitar laberintos imposibles de resolver.
    return min(pct, 60) 

def generar_tablero(rows, cols, obstaculos_pct, inicio, meta):
    # Calcula el tamaño del tablero
    total = rows * cols
    # Calcula la cantidad de obstáculos en el tablero
    obstaculos_cantidad = int(total * obstaculos_pct / 100)

    tablero = [[0 for _ in range(cols)] for _ in range(rows)]

    posiciones = [(r, c) for r in range(rows) for c in range(cols)
                  if (r, c) != inicio and (r, c) != meta]
    
    random.shuffle(posiciones)

    for i in range(min(obstaculos_cantidad, len(posiciones))):
        r, c = posiciones[i]
        # Coloca un obstáculo 
        tablero[r][c] = 1 

    return tablero

def imprimir_tablero(tablero, inicio, meta, posicion_actual= None, path=None):
    path = path or []
    rows = len(tablero)
    cols = len(tablero[0])

    for r in range(rows):
        linea = ""
        for c in range(cols):
            if (r, c) == posicion_actual:
                linea += "A "
            elif(r, c) == inicio:
                linea += "I "
            elif(r, c) == meta:
                linea += "M "
            elif(r, c) in path:
                linea += "- "
            elif tablero[r][c] == 1:
                linea += "X "
            else:
                linea += ". "
        print(linea)

# ===================== BFS =====================
def bfs(tablero, inicio, meta, movimientos):
    rows = len(tablero)
    cols = len(tablero[0])

    queue = deque()
    queue.append((inicio, [inicio]))

    visitados = set([inicio])

    while queue:
        posicion_actual, path = queue.popleft()

        if posicion_actual == meta:
            return True, path
        
        for k in movimientos:
            dr, dc = Moves[k]
            nr, nc = posicion_actual[0] + dr, posicion_actual[1] + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if tablero[nr][nc] == 0 and (nr, nc) not in visitados:
                    visitados.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))

    return False, []

# ===================== DFS =====================

def dfs(tablero, inicio, meta, movimientos):
    rows = len(tablero)
    cols = len(tablero[0])
    
    stack = [(inicio, [inicio])]
    stack.append((inicio, [inicio]))

    visited = set([inicio])

    while stack:
        current, path = stack.pop() # Estructura LIFO

        if current == meta:
            return True, path
        
        for k in movimientos:
            dr, dc = Moves[k]
            nr, nc = current[0] + dr, current[1] + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if tablero[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append(((nr, nc), path + [(nr, nc)]))

    return False, []

# ===================== LDFS =====================

def ldfs(tablero, inicio, meta, movimientos, limit):
    rows = len(tablero)
    cols = len(tablero[0])
    
    stack = [(inicio, [inicio], 0)] # Estructura LIFO con profundidad
    visited = set([inicio])

    while stack:
        current, path, depth = stack.pop()

        if current == meta:
            return True, path
        
        if depth < limit:
            for k in movimientos:
                dr, dc = Moves[k]
                nr, nc = current[0] + dr, current[1] + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    if tablero[nr][nc] == 0 and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        stack.append(((nr, nc), path + [(nr, nc)], depth + 1))

    return False, []

# ===================== Animación =====================

def animate_path(tablero, inicio, meta, path):
    visitados = []
    for posicion in path:
        clear()
        visitados.append(posicion)
        imprimir_tablero(tablero, inicio, meta, posicion_actual=posicion, path=visitados)
        input("Presione Enter para el siguiente paso")

# ===================== MAIN =====================

def main():
    print("--- Laberinto con BFS, DFS y LDFS ---")

    print("Elija un modelo")
    print("1 - BFS Anchura")
    print("2 - DFS Profundidad")
    print("3 - LDFS Profundidad Limitada")
    model_option = read_int("Seleccione una opcion: ", 1)

    # Se pide el tamaño del tablero al usuario
    rows = read_int("Ingrese el numero de filas: ", 1)
    cols = read_int("Ingrese el numero de columnas: ", 1)

    inicio = preguntar_posicion("Posicion de inicio(4, 5)", rows, cols)
    meta = preguntar_posicion("Posicion de meta(7, 8)", rows, cols)

    while meta == inicio:
        print("La meta no puede ser igual a la posicion de inicio")
        meta = preguntar_posicion("Posicion de meta(7, 8)", rows, cols)

    print("\nTipo de movimientos permitidos:")
    print("1 - solo arriba, abajo, izquierda y derecha (U,D,L,R)")
    print("2 - movimientos diagonales incluidos (U,D,L,R,UL,UR,DL,DR)")

    opcion = read_int("Seleccione una opcion: ", 1)

    if opcion == 1:
        movimientos = ['U', 'D', 'L', 'R']
    else:
        movimientos = ['U', 'D', 'L', 'R', 'UL', 'UR', 'DL', 'DR']

    obstaculos_pct = calcular_porcentaje_obstaculos(rows, cols)
    print(f"Se generará un laberinto con aproximadamente {obstaculos_pct:.2f}% de obstáculos.")
    
    tablero = generar_tablero(rows, cols, obstaculos_pct, inicio, meta)

    if model_option == 1:
        success, path = bfs(tablero, inicio, meta, movimientos)
    if model_option == 2:
        success, path = dfs(tablero, inicio, meta, movimientos)
    if model_option == 3:
        limit = read_int("Ingrese el limite de profundidad para LDFS: ", 1)
        success, path = ldfs(tablero, inicio, meta, movimientos, limit)

    if success:
        print("\nCamino encontrado: ")
        time.sleep(1)
        animate_path(tablero, inicio, meta, path)
        print("\nSolucion completada en ", len(path) - 1, "pasos.")
    else:
        clear()
        imprimir_tablero(tablero, inicio, meta, path)
        print("\nNo se encontro una solucion para este laberinto.")

if __name__ == "__main__":
    main()
