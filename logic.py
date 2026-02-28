import random

SIZE = 4

def start_game():
    return [[0]*SIZE for _ in range(SIZE)]

def add_new_tile(mat):
    empty = [(i, j) for i in range(SIZE) for j in range(SIZE) if mat[i][j] == 0]
    if empty:
        i, j = random.choice(empty)
        mat[i][j] = 2

def compress(mat):
    changed = False
    new_mat = [[0]*SIZE for _ in range(SIZE)]
    for i in range(SIZE):
        pos = 0
        for j in range(SIZE):
            if mat[i][j] != 0:
                new_mat[i][pos] = mat[i][j]
                if j != pos:
                    changed = True
                pos += 1
    return new_mat, changed

def merge(mat):
    changed = False
    score = 0
    for i in range(SIZE):
        for j in range(SIZE-1):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                score += mat[i][j]
                mat[i][j+1] = 0
                changed = True
    return mat, changed, score

def reverse(mat):
    return [row[::-1] for row in mat]

def transpose(mat):
    return [list(row) for row in zip(*mat)]

def move_left(grid):
    grid, c1 = compress(grid)
    grid, c2, score = merge(grid)
    grid, _ = compress(grid)
    return grid, c1 or c2, score

def move_right(grid):
    grid = reverse(grid)
    grid, changed, score = move_left(grid)
    return reverse(grid), changed, score

def move_up(grid):
    grid = transpose(grid)
    grid, changed, score = move_left(grid)
    return transpose(grid), changed, score

def move_down(grid):
    grid = transpose(grid)
    grid, changed, score = move_right(grid)
    return transpose(grid), changed, score

def get_game_state(mat):
    for row in mat:
        if 2048 in row:
            return "WON"
    if any(0 in row for row in mat):
        return "PLAYING"
    for i in range(SIZE):
        for j in range(SIZE-1):
            if mat[i][j] == mat[i][j+1] or mat[j][i] == mat[j+1][i]:
                return "PLAYING"
    return "LOST"