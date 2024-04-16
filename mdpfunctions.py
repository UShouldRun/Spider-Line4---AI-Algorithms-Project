from objects import Node, Board
from copy import deepcopy
from math import sqrt, log, pow, e

def game_state(node: Node, checkWin, checkDraw) -> int:
    if node.is_root(): return False
    directions = [(-1,-1),(-1,0),(0,1),(1,1),(1,0),(0,-1),(1,-1),(-1,1)]
    for vector in directions:
        if checkWin(node.get_state().get_matrix(), vector, node.get_action()[0]): return 1
        if checkDraw(node.get_state().get_matrix()): return 2
    return 0

def state_analysis(node: Node, checkWin, checkDraw) -> bool:
    node.set_terminal(game_state(node, checkWin, checkDraw) != 0)
    return node.is_terminal()

def get_actions(node: Node, get_legal_moves) -> list[tuple[str, tuple[int, int]]]:
    piece = "1" if node.get_action()[0] == "2" else "2"
    actions = []
    for move in get_legal_moves(node.get_state()): actions.append((piece, move))
    return actions

def execute(node: Node, action) -> Node:
    new_state = deepcopy(node.get_state())
    Board.place(new_state, action[0], action[1])
    return Node(new_state, node, action)

def qfunction(node: Node, opponent: str, player: str, checkWin, checkDraw) -> float:
    if node.is_terminal():
        if game_state(node, checkWin, checkDraw) == 2: return 0.5
        return 0 if node.get_action()[0] == opponent else 1
    return softmax(qfunction3(node, opponent, player))

def softmax(x: float) -> float:
    if x == -float("inf"): return 0
    if x == float("inf"): return 1
    return 1/(1 + pow(e, -x))

def qfunction1(node: Node) -> float: return heuristic(node.get_state().get_matrix(), "1" if node.get_action()[0] == "2" else "2")
def qfunction3(node: Node, opponent: str, player: str) -> int: return heuristic1(node.get_state().get_matrix(), opponent if node.get_action()[0] == player else player, opponent)
def qfunction4(node: Node, opponent: str, player: str) -> int: return heuristic2(node.get_state().get_matrix(), opponent if node.get_action()[0] == player else player, opponent)

def heuristic(matrix, piece: str, n: int, m: int):
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # direções

    for i in range(n):
        for j in range(m):
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

def heuristic1(matrix, piece: str, opponent: str, weight: float = 0.5, player1_weight: float = 1.05, player1_offset: float = .1, neighbourhood_weight: float = 5, center_weight: float = .5, player_prox_weight: float = 1) -> float: 
    rows, cols = len(matrix), len(matrix[0])

    def center_prox(i: int, j: int) -> float: return center_weight * sqrt((rows/2)**2 + (cols/2)**2) - sqrt((rows/2 - i)**2 + (cols/2 - j)**2)
    def player_prox(i: int, j: int) -> float: 
        min_prox = float("inf")
        count = 0
        for u, row in enumerate(matrix):
            for v, entry in enumerate(row):
                if entry != "0" and entry != piece:
                    count += 1
                    prox = abs(sqrt((i)**2 + (j)**2) - sqrt((i - u)**2 + (j - v)**2))
                    if prox < min_prox: min_prox = prox
        if count > 0: return player_prox_weight / (1 + min_prox) 
        return 0

    def neighbourhood(i: int, j: int) -> int:
        eval = 0
        directions = [(-1,-1),(-1,0),(0,1),(1,1),(1,0),(0,-1),(1,-1),(-1,1)]
        for vector in directions:
            temp_eval = 0
            count = 1
            for k in range(4):
                u = i + vector[0] * k
                v = j + vector[1] * k

                if -1 < u < rows and -1 < v < cols:
                    if matrix[u][v] == matrix[i][j]:
                        temp_eval += count
                        count += 1
                    elif matrix[u][v] != "0":
                        temp_eval = 0
                        break
            eval += temp_eval
        return neighbourhood_weight * eval

    heuristic_eval = 0
    for i, row in enumerate(matrix):
        for j, entry in enumerate(row):
            if entry != "0":
                heuristic_eval += (-1 if entry == opponent else 1) * (neighbourhood(i,j) + center_prox(i,j) + player_prox(i,j))

    if piece == "1": return round(player1_weight * weight * heuristic_eval + player1_offset, 3)
    return round(weight * heuristic_eval / 10, 3)

def heuristic2(matrix, piece: str, opponent: str, weight: float = .5, player1_weight: float = 1.05, player1_offset: float = .1, neighbourhood_weight: float = 2, center_weight: float = 0.5, player_prox_weight: float = 1) -> float: 
    rows, cols = len(matrix), len(matrix[0])

    def center_prox(i: int, j: int) -> float: return center_weight * sqrt((rows/2)**2 + (cols/2)**2) - sqrt((rows/2 - i)**2 + (cols/2 - j)**2)
    def player_prox(i: int, j: int) -> float: 
        min_prox = float("inf")
        count = 0
        for u, row in enumerate(matrix):
            for v, entry in enumerate(row):
                if entry != "0" and entry != piece:
                    count += 1
                    prox = abs(sqrt((i)**2 + (j)**2) - sqrt((i - u)**2 + (j - v)**2))
                    if prox < min_prox: min_prox = prox
        if count > 0: return player_prox_weight / (1 + min_prox) 
        return 0

    def neighborhood(i: int, j: int) -> int:
        eval = 0
        directions = [(-1,-1),(-1,0),(0,1),(1,1),(1,0),(0,-1),(1,-1),(-1,1)]
        for vector in directions:
            temp_eval = 0
            count = 1
            for k in range(4):
                u = i + vector[0] * k
                v = j + vector[1] * k

                if -1 < u < rows and -1 < v < cols:
                    if matrix[u][v] == matrix[i][j]:
                        temp_eval += count
                        count += 1
                    elif matrix[u][v] != "0":
                        temp_eval = 0
                        break
            eval += temp_eval
        return neighbourhood_weight * eval

    heuristic_eval = 0
    for i, row in enumerate(matrix):
        for j, entry in enumerate(row):
            if entry != "0":
                heuristic_eval += (-1 if entry == opponent else 1) * (neighborhood(i,j) + center_prox(i,j) + player_prox(i,j))

    if piece == "1": return round(abs(player1_weight * weight * heuristic_eval)/10, 3)
    return round(abs(weight * heuristic_eval)/10, 3)


def visualize_ab(nodes, size: int) -> None:
    rows = []
    for i in range(size):
        cols = []
        for j in range(size):
            got_it = False
            for node in nodes:
                if node.get_action()[1] == (i,j):
                    reward = str(node.get_reward())
                    c = len(reward)
                    if c < 7: reward = " "*(7 - c) + reward
                    cols.append(reward)
                    got_it = True
                    break
            if not got_it: cols.append("-------")
        rows.append(cols)
    for row in rows: print(row)

def visualize_negamax(nodes, sign: int, size: int) -> None:
    rows = []
    for i in range(size):
        cols = []
        for j in range(size):
            got_it = False
            for node in nodes:
                if node.get_action()[1] == (i,j):
                    reward = str(sign * node.get_reward())
                    c = len(reward)
                    if c < 7: reward = " "*(7 - c) + reward
                    cols.append(reward)
                    got_it = True
                    break
            if not got_it: cols.append("-------")
        rows.append(cols)
    for row in rows: print(row)


def visualize_montecarlo(nodes, uct_const: int, size: int) -> None:
    def uct(node) -> float:
        if node.get_parent().get_visits() == 0: raise ValueError("Parent node has 0 visits")

        n_parent = node.get_parent().get_visits()
        n_i = node.get_visits()

        if n_i == 0: return float("inf")
        v_i = node.get_reward()/n_i

        if uct_const > 0:
            if n_i > 1: return v_i + uct_const * sqrt(log(n_parent)/log(n_i))
            else: return float("inf")
        return v_i

    rows = []
    for i in range(size):
        cols = []
        for j in range(size):
            got_it = False
            for node in nodes:
                if node.get_action()[1] == (i,j):
                    eval = str(round(softmax(uct(node)), 3)) + f"/{round(node.get_reward()/node.get_visits(), 3)}/{node.get_visits()}" 
                    c = len(eval)
                    if c < 15: eval = " "*(15 - c) + eval
                    cols.append(eval)
                    got_it = True
                    break
            if not got_it: cols.append("---------------")
        rows.append(cols)
    for row in rows: print(row)