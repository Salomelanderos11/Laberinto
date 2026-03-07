import os
import time
import random

# Importación de utilidades y algoritmos
import utils
import bfs, dfs, ldfs, voraz, a_star, tabu, recocido

def clear():
    os.system('cls' if os.name == "nt" else 'clear')

def read_int(prompt, minv=0):
    while True:
        try:
            v = int(input(prompt))
            if v >= minv: return v
            print(f"Error: Ingrese un número mayor o igual a {minv}")
        except ValueError:
            print("Error: Entrada no válida.")

def preguntar_posicion(prompt, rows, cols):
    while True:
        try:
            text = input(prompt + " (formato fila,col): ")
            r, c = map(int, text.split(","))
            if 0 <= r < rows and 0 <= c < cols:
                return (r, c)
        except:
            pass
        print(f"Posición fuera de rango. El tablero es de {rows}x{cols}.")

def generar_tablero(rows, cols, inicio, meta):
    # Calcula porcentaje automático (máximo 60% para que sea posible resolver)
    pct_val = min((rows * cols) / 2.5, 60)
    print(f"\nGenerando laberinto con {pct_val:.2f}% de obstáculos...")
    
    tablero = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Lista de todas las celdas excepto inicio y meta
    posiciones = [(r, c) for r in range(rows) for c in range(cols) 
                  if (r, c) != inicio and (r, c) != meta]
    
    random.shuffle(posiciones)
    num_obstaculos = int((rows * cols) * pct_val / 100)
    
    for i in range(min(num_obstaculos, len(posiciones))):
        r, c = posiciones[i]
        tablero[r][c] = 1 # 1 representa un muro (X)
        
    return tablero

def imprimir_tablero(tablero, inicio, meta, pos_actual=None, path=None):
    path = path or []
    for r in range(len(tablero)):
        linea = ""
        for c in range(len(tablero[0])):
            if (r, c) == pos_actual: linea += "A " # Agente actual
            elif (r, c) == inicio:   linea += "I " # Inicio
            elif (r, c) == meta:     linea += "M " # Meta
            elif (r, c) in path:     linea += "- " # Camino recorrido
            elif tablero[r][c] == 1: linea += "X " # Obstáculo
            else:                    linea += ". " # Espacio vacío
        print(linea)

def animar_solucion(tablero, inicio, meta, path):
    if not path:
        return
    print("\n--- Iniciando Animación ---")
    recorrido = []
    for paso in path:
        clear()
        recorrido.append(paso)
        imprimir_tablero(tablero, inicio, meta, pos_actual=paso, path=recorrido)
        time.sleep(0.2) # Velocidad de la animación
    print(f"\n¡Llegamos! Solución encontrada en {len(path)-1} movimientos.")

def main():
    clear()
    print("========================================")
    print("   SIMULADOR DE BUSQUEDA EN LABERINTOS  ")
    print("========================================\n")

    # 1. Configuración del Tablero
    rows = read_int("Número de filas: ", 2)
    cols = read_int("Número de columnas: ", 2)
    
    inicio = preguntar_posicion("Punto de INICIO", rows, cols)
    meta = preguntar_posicion("Punto de META", rows, cols)
    
    while inicio == meta:
        print("El inicio y la meta no pueden ser iguales.")
        meta = preguntar_posicion("Punto de META", rows, cols)

    # 2. Selección de Movimientos
    print("\n¿Qué movimientos permite?")
    print("1 - Ortogonales (Arriba, Abajo, Izq, Der)")
    print("2 - Incluir Diagonales (8 direcciones)")
    mov_op = read_int("Opción: ", 1)
    
    if mov_op == 1:
        movimientos_permitidos = ['U', 'D', 'L', 'R']
    else:
        movimientos_permitidos = list(utils.Moves.keys())

    # 3. Generación del Laberinto
    tablero = generar_tablero(rows, cols, inicio, meta)
    
    # 4. Selección del Algoritmo
    print("\nSeleccione el Algoritmo de Búsqueda:")
    print("1. BFS (Anchura)")
    print("2. DFS (Profundidad)")
    print("3. LDFS (Profundidad Limitada)")
    print("4. Voraz (Greedy)")
    print("5. A* (Estrella)")
    print("6. Búsqueda Tabú")
    print("7. Recocido Simulado")
    
    alg_op = read_int("Opción: ", 1)
    
    success, path = False, []

    # Ejecución según opción
    if alg_op == 1:
        success, path = bfs.ejecutar(tablero, inicio, meta, movimientos_permitidos)
    elif alg_op == 2:
        success, path = dfs.ejecutar(tablero, inicio, meta, movimientos_permitidos)
    elif alg_op == 3:
        limite = read_int("Ingrese el límite de profundidad: ", 1)
        success, path = ldfs.ejecutar(tablero, inicio, meta, movimientos_permitidos, limite)
    elif alg_op == 4:
        success, path = voraz.ejecutar(tablero, inicio, meta, movimientos_permitidos)
    elif alg_op == 5:
        success, path = a_star.ejecutar(tablero, inicio, meta, movimientos_permitidos)
    elif alg_op == 6:
        t_size = read_int("Tamaño de la lista Tabú: ", 1)
        success, path = tabu.ejecutar(tablero, inicio, meta, movimientos_permitidos, t_size)
    elif alg_op == 7:
        temp = read_int("Temperatura inicial (ej. 100): ", 1)
        cooling = float(input("Tasa de enfriamiento (0.1 a 0.99): "))
        success, path = recocido.ejecutar(tablero, inicio, meta, movimientos_permitidos, temp, cooling)

    # 5. Resultado
    if success:
        input("\n¡Camino encontrado! Presione Enter para ver la animación...")
        animar_solucion(tablero, inicio, meta, path)
    else:
        clear()
        imprimir_tablero(tablero, inicio, meta)
        print("\nNo se encontró una ruta posible con el algoritmo seleccionado.")

if __name__ == "__main__":
    main()