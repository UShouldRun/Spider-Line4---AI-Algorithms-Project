from random import randint
from algs.mdpfunctions import visualize_ab, visualize_negamax, visualize_montecarlo
from algs.minimax import AlphaBeta
from algs.negamax import Negamax
from algs.montecarlo import MCTS
import threading

class Bot0:
    def __init__(self, board, name: str) -> None: self.board, self.name = board, name
    def get_name(self) -> str: return self.name
    def play(self, piece: str, moves_func) -> None: self.board.place_piece(piece,moves_func()[randint(0,len(moves_func()) - 1)])

class Bot1(Negamax):
    def __init__(self, board, name: str, depth: int, mdp) -> None:
        super().__init__(board, 1, depth, mdp)
        self.board, self.name = board, name

    def get_name(self) -> str: return self.name
    
    def play(self, piece: str) -> None:
        print(f"{self.get_name()} evaluating...")

        self.root_state = self.board
        opponent = "2" if piece == "1" else "1"
        self.root_sign = -1 if opponent == "1" else 1

        self.mdp.action_type, self.mdp.action_type_opponent = piece, opponent

        root = self.negamax(opponent)
        if root == None: return
        best_nodes = [child for child in root.get_children() if child.get_reward() == self.root_sign * root.get_reward()]
        visualize_negamax(root.get_children(), self.root_sign, self.board.matrix.shape[0])

        move = best_nodes[randint(0, len(best_nodes) - 1)].get_action()[1]
        self.board.place_piece(piece, move)

class Bot2(AlphaBeta):
    def __init__(self, board, name: str, depth: int, mdp) -> None:
        super().__init__(board, depth, mdp)
        self.board, self.name = board, name

    def get_name(self) -> str: return self.name
    
    def play(self, piece: str) -> None:
        print(f"{self.get_name()} evaluating...")
        self.nodes_depth = 0
        self.root_state = self.board

        opponent = "2" if piece == "1" else "1"
        self.mdp.action_type, self.mdp.action_type_opponent  = piece, opponent 

        root = self.minimax(opponent)
        if root == None: return

        best_nodes = [child for child in root.get_children() if child.get_reward() == root.get_reward()]
        visualize_ab(root.get_children(), self.board.matrix.shape[0])

        move = best_nodes[randint(0,len(best_nodes) - 1)].get_action()[1]
        self.board.place_piece(piece, move)

class Bot3(MCTS):
    def __init__(self, board, name: str, max_time: int, max_mem: int, depth: int, uct_const: int, mdp) -> None:
        super().__init__(board, max_time, max_mem, depth, uct_const, mdp)
        self.board = self.root_state
        self.name = name

    def get_name(self) -> str: return self.name
    def play(self, piece: str) -> None:
        print(f"{self.get_name()} evaluating...")

        self.root_state = self.board
        opponent = "2" if piece == "1" else "1"

        self.mdp.action_type, self.mdp.action_type_opponent = piece, opponent
        root = self.mcts(opponent)
        if root == None: return
        move = self.uct_select(root).get_action()[1]

        visualize_montecarlo(root.get_children(), self.get_uct_const(), self.board.matrix.shape[0])
        self.board.place_piece(piece, move)
        self.reset()
