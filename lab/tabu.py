from collections import deque
from utils import Moves, heuristic

def ejecutar(tablero, inicio, meta, movimientos, tabu_size):
    rows, cols = len(tablero), len(tablero[0])
    current = inicio
    path = [inicio]
    tabu_list = deque()
    
    # Límite de pasos para evitar bucles infinitos en tabú si no hay solución
    for _ in range(rows * cols * 2):
        if current == meta: return True, path
        next_moves = []
        for k in movimientos:
            dr, dc = Moves[k]
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and tablero[nr][nc] == 0 and (nr, nc) not in tabu_list:
                next_moves.append(((nr, nc), heuristic((nr, nc), meta)))
        
        if not next_moves: return False, []
        
        next_moves.sort(key=lambda x: x[1])
        next_pos = next_moves[0][0]
        
        tabu_list.append(current)
        if len(tabu_list) > tabu_size: tabu_list.popleft()
        
        current = next_pos
        path.append(current)
    return False, []