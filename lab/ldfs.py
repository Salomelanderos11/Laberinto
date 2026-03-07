from utils import Moves

def ejecutar(tablero, inicio, meta, movimientos, limite):
    rows, cols = len(tablero), len(tablero[0])
    stack = [(inicio, [inicio], 0)]
    visited = {inicio}
    while stack:
        current, path, depth = stack.pop()
        if current == meta: return True, path
        if depth < limite:
            for k in movimientos:
                dr, dc = Moves[k]
                nr, nc = current[0] + dr, current[1] + dc
                if 0 <= nr < rows and 0 <= nc < cols and tablero[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append(((nr, nc), path + [(nr, nc)], depth + 1))
    return False, []