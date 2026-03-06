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

# ===================== VORAZ =====================

def voraz(tablero, inicio, meta, movimientos):
    rows = len(tablero)
    cols = len(tablero[0])
    
    def heuristic(pos):
        return abs(pos[0] - meta[0]) + abs(pos[1] - meta[1])

    stack = [(inicio, [inicio])]
    visited = set([inicio])

    while stack:
        current, path = stack.pop()

        if current == meta:
            return True, path
        
        # Ordena los movimientos por la heurística
        next_moves = []
        for k in movimientos:
            dr, dc = Moves[k]
            nr, nc = current[0] + dr, current[1] + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if tablero[nr][nc] == 0 and (nr, nc) not in visited:
                    next_moves.append(((nr, nc), heuristic((nr, nc))))

        next_moves.sort(key=lambda x: x[1]) # Ordena por heurística

        for move in next_moves:
            pos = move[0]
            visited.add(pos)
            stack.append((pos, path + [pos]))

    return False, []

# ===================== A STAR =====================

def a_star(tablero, inicio, meta, movimientos):
    rows = len(tablero)
    cols = len(tablero[0])
    
    def heuristic(pos):
        return abs(pos[0] - meta[0]) + abs(pos[1] - meta[1])

    # El open_set es una lista de tuplas (f_score, posición, camino) ordenada por f_score
    open_set = [(heuristic(inicio), inicio, [inicio])]
    visited = set([inicio])

    while open_set:
        _, current, path = open_set.pop(0)

        if current == meta:
            return True, path
        
        for k in movimientos:
            dr, dc = Moves[k]
            nr, nc = current[0] + dr, current[1] + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if tablero[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    open_set.append((heuristic((nr, nc)), (nr, nc), path + [(nr, nc)]))
                    open_set.sort(key=lambda x: x[0]) # Ordena por heurística

    return False, []

# ===================== BUSQUEDA TABU =====================

def tabu(tablero, inicio, meta, movimientos, tabu_size):
    rows = len(tablero)
    cols = len(tablero[0])
    
    def heuristic(pos):
        return abs(pos[0] - meta[0]) + abs(pos[1] - meta[1])

    current = inicio
    path = [inicio]
    tabu_list = set()

    while current != meta:
        next_moves = []
        for k in movimientos:
            dr, dc = Moves[k]
            nr, nc = current[0] + dr, current[1] + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if tablero[nr][nc] == 0 and (nr, nc) not in tabu_list:
                    next_moves.append(((nr, nc), heuristic((nr, nc))))

        if not next_moves:
            return False, [] # No hay movimientos disponibles

        next_moves.sort(key=lambda x: x[1]) # Ordena por heurística
        next_pos = next_moves[0][0]

        tabu_list.add(current)
        if len(tabu_list) > tabu_size:
            tabu_list.pop() # Elimina el elemento más antiguo

        current = next_pos
        path.append(current)

    return True, path

# ===================== RECOCIDO SIMULADO =====================

def recocido_simulado(tablero, inicio, meta, movimientos, initial_temp, cooling_rate):
    rows = len(tablero)
    cols = len(tablero[0])
    
    def heuristic(pos):
        return abs(pos[0] - meta[0]) + abs(pos[1] - meta[1])

    current = inicio
    path = [inicio]
    temp = initial_temp

    while current != meta and temp > 0:
        next_moves = []
        for k in movimientos:
            dr, dc = Moves[k]
            nr, nc = current[0] + dr, current[1] + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if tablero[nr][nc] == 0:
                    next_moves.append(((nr, nc), heuristic((nr, nc))))

        if not next_moves:
            return False, [] # No hay movimientos disponibles

        next_moves.sort(key=lambda x: x[1]) # Ordena por heurística
        next_pos = next_moves[0][0]

        if heuristic(next_pos) < heuristic(current) or random.random() < temp / initial_temp:
            current = next_pos
            path.append(current)

        temp *= cooling_rate # Enfría la temperatura

    return current == meta, path

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
    print("4 - Voraz")
    print("5 - A*")
    print("6 - Tabu")
    print("7 - Recocido Simulado")
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
    if model_option == 4:
        success, path = voraz(tablero, inicio, meta, movimientos)
    if model_option == 5:
        success, path = a_star(tablero, inicio, meta, movimientos)
    if model_option == 6:
        tabu_size = read_int("Ingrese el tamaño de la lista tabu: ", 1)
        success, path = tabu(tablero, inicio, meta, movimientos, tabu_size)
    if model_option == 7:
        initial_temp = read_int("Ingrese la temperatura inicial: ", 1)
        cooling_rate = float(input("Ingrese la tasa de enfriamiento (0 < rate < 1): "))
        success, path = recocido_simulado(tablero, inicio, meta, movimientos, initial_temp, cooling_rate)

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
