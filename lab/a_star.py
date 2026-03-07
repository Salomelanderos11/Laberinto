from utils import Moves, heuristic

def ejecutar(tablero, inicio, meta, movimientos):
    rows, cols = len(tablero), len(tablero[0])
    open_set = [(heuristic(inicio, meta), inicio, [inicio])]
    visited = {inicio}
    while open_set:
        _, current, path = open_set.pop(0)
        if current == meta: return True, path
        for k in movimientos:
            dr, dc = Moves[k]
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and tablero[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                open_set.append((heuristic((nr, nc), meta), (nr, nc), path + [(nr, nc)]))
                open_set.sort(key=lambda x: x[0])
    return False, []