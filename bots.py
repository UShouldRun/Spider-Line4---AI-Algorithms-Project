from random import randint
from copy import deepcopy
from montecarlo import MCTS

class Bot0:
    def __init__(self, board, name: str) -> None: self.board, self.name = board, name
    def get_name(self) -> str: return self.name
    def play(self, piece: str, moves_func) -> None: self.board.place_piece(piece,moves_func()[randint(0,len(moves_func()) - 1)])

class Bot1:
    def __init__(self, board, name) -> None: self.board, self.name = board, name
    def get_name(self) -> str: return self.name
    def play(self, piece: str, moves_func) -> None: self.board.place_piece(piece,moves_func()[randint(0,len(moves_func()) - 1)])

class Bot2:
    def __init__(self, board, name) -> None: self.board, self.name = board, name
    def get_name(self) -> str: return self.name
    def play(self, piece: str, moves_func) -> None: self.board.place_piece(piece,moves_func()[randint(0,len(moves_func()) - 1)])

class Bot3(MCTS):
    def __init__(self, board, name, max_time, max_mem, mdp) -> None:
        super().__init__(board, max_time, max_mem, mdp)
        self.board = self.root_state
        self.name = name
    def get_name(self) -> str: return self.name
    def play(self, piece) -> None:
        self.mdp.action_type = piece
        move = self.uct_select(self.mcts()).get_action()[1]
        self.board.place_piece(piece, move)
        self.reset()


