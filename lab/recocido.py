import random
import math
from utils import Moves, heuristic

def ejecutar(tablero, inicio, meta, movimientos, initial_temp, cooling_rate):
    rows, cols = len(tablero), len(tablero[0])
    current = inicio
    path = [inicio]
    temp = initial_temp
    
    while current != meta and temp > 0.01:
        next_moves = []
        for k in movimientos:
            dr, dc = Moves[k]
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and tablero[nr][nc] == 0:
                next_moves.append((nr, nc))
        
        if not next_moves: return False, []
        
        next_pos = random.choice(next_moves)
        delta = heuristic(next_pos, meta) - heuristic(current, meta)
        
        if delta < 0 or random.random() < math.exp(-delta / temp if temp > 0 else 1):
            current = next_pos
            path.append(current)
            
        temp *= cooling_rate
    return current == meta, path