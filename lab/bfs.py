from collections import deque
from utils import Moves

def ejecutar(tablero, inicio, meta, movimientos):
    rows, cols = len(tablero), len(tablero[0])
    queue = deque([(inicio, [inicio])])
    visitados = {inicio}
    while queue:
        pos_actual, path = queue.popleft()
        if pos_actual == meta: return True, path
        for k in movimientos:
            dr, dc = Moves[k]
            nr, nc = pos_actual[0] + dr, pos_actual[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and tablero[nr][nc] == 0 and (nr, nc) not in visitados:
                visitados.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return False, []