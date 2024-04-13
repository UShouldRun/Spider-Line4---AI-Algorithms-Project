from objects import Node, Board
from copy import deepcopy

def game_state(node: Node, checkWin, checkDraw) -> int:
    if node.is_root(): return False
    directions = [(-1,-1),(-1,0),(0,1),(1,1),(1,0),(0,-1),(1,-1),(-1,1)]
    for vector in directions:
        if checkWin(node.get_state().get_matrix(), vector, node.get_action()[0]): return 1
        if checkDraw(node.get_state().get_matrix()): return 2
    return 0

def state_analysis(node: Node, checkWin, checkDraw) -> bool: return game_state(node, checkWin, checkDraw) != 0

def get_actions(node: Node, start_piece: str, get_legal_moves) -> list[tuple[str, tuple[int, int]]]:
    if node.is_root(): piece = start_piece
    else: piece = "1" if node.get_action()[0] == "2" else "2"
    actions = []
    for move in get_legal_moves(node.get_state()): actions.append((piece, move))
    return actions

def execute(node: Node, action) -> Node:
    new_state = deepcopy(node.get_state())
    Board.place(new_state, action[0], action[1])
    return Node(new_state, node, action)

def qfunction(node: Node, checkWin, checkDraw) -> int:
    if game_state(node, checkWin, checkDraw) == 2: return 0.5
    return 0 if node.get_action()[0] == "1" else 1

def qfunction3(node: Node) -> int: return heuristic1(node.get_state().get_matrix())
def qfunction1(node: Node) -> float: return heuristic(node.get_state().get_matrix(), node.get_action()[0])

def heuristic(matrix, piece: str):
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # direções

    for i in range(8):
        for j in range(8):
            for dx, dy in directions:
                line = [matrix[i + k * dx][j + k * dy] if 0 <= i + k * dx < 8 and 0 <= j + k * dy < 8 else None for k in range(4)]
                player_count = line.count(piece)
                none_count = line.count(None)
                if player_count + none_count == 4:
                    if player_count == 3 and none_count == 1:
                        score += 100
                    elif player_count == 2 and none_count == 2:
                        score += 10
                    elif player_count == 1 and none_count == 3:
                        score += 1
                    elif player_count == 0 and none_count == 4:
                        score += 0.1

    return score

def heuristic1(matrix) -> int: 
    rows, cols = len(matrix), len(matrix[0])
    def neiborhood(i: int, j: int) -> int:
        count, eval = 1, 0
        directions = [(-1,-1),(-1,0),(0,1),(1,1),(1,0),(0,-1),(1,-1),(-1,1)]

        for vector in directions:
            temp_heuristic_sum = 0
            count = 1
            for k in range(4):
                u = i + vector[0] * k
                v = j + vector[1] * k

                if -1 < u < rows and -1 < v < cols:
                    if matrix[u][v] == matrix[i][j]:
                        temp_heuristic_sum += count
                        count += 1
                    elif matrix[u][v] != "0":
                        temp_heuristic_sum = 0
                        break

                if matrix[i][j] == "1": eval -= temp_heuristic_sum
                if matrix[i][j] == "2": eval += temp_heuristic_sum

        return eval

    heuristic_sum = 0
    for i, row in enumerate(matrix):
        for j, entry in enumerate(row):
            if matrix[i][j] != "0":
                heuristic_sum += neiborhood(i, j)

    return heuristic_sum


