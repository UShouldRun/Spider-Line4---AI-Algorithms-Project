class Player:
    def __init__(self, board, piece: str, name: str) -> None:
        self.board = board
        self.piece = piece
        self.name = name

    def setPiece(self, piece: str) -> None: self.piece = piece
    def getPiece(self) -> str: return self.piece
    def get_name(self) -> str: return self.name

    def play(self, move) -> None: self.board.place_piece(self.piece, move)
