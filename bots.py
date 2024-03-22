from random import randint

class Bot0:
    def __init__(self, board) -> None: self.board = board
    def play(self, piece: str, moves_func) -> None: self.board.place_piece(piece,moves_func()[randint(0,len(moves_func()) - 1)])

class Bot1:
    def __init__(self, board) -> None: self.board = board

    def play(self) -> None: pass

class Bot2:
    def __init__(self, board) -> None: self.board = board

    def play(self) -> None: pass

class Bot3:
    def __init__(self, board) -> None: self.board = board

    def play(self) -> None: pass
