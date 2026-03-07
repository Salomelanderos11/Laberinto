from utils import Moves, heuristic

def ejecutar(tablero, inicio, meta, movimientos):
    rows, cols = len(tablero), len(tablero[0])
    stack = [(inicio, [inicio])]
    visited = {inicio}
    while stack:
        current, path = stack.pop()
        if current == meta: return True, path
        next_moves = []
        for k in movimientos:
            dr, dc = Moves[k]
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and tablero[nr][nc] == 0 and (nr, nc) not in visited:
                next_moves.append(((nr, nc), heuristic((nr, nc), meta)))
        next_moves.sort(key=lambda x: x[1], reverse=True)
        for move in next_moves:
            visited.add(move[0])
            stack.append((move[0], path + [move[0]]))
    return False, []