Moves = {
    'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1),
    'UL': (-1, -1), 'UR': (-1, 1), 'DL': (1, -1), 'DR': (1, 1)
}

def heuristic(pos, meta):
    return abs(pos[0] - meta[0]) + abs(pos[1] - meta[1])