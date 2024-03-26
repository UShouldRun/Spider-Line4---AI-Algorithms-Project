from random import randint

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

class Bot3:
    def __init__(self, board, name) -> None: self.board, self.name = board, name
    def get_name(self) -> str: return self.name
    def play(self, piece: str, moves_func) -> None: self.board.place_piece(piece,moves_func()[randint(0,len(moves_func()) - 1)])
