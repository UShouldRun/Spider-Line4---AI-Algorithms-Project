class Player:
    def __init__(self, board, piece: str) -> None:
        self.board = board
        self.piece = piece

    def setPiece(self, piece: str) -> None: self.piece = piece
    def getPiece(self) -> str: return self.piece

    def play(self, move) -> None: self.board.place_piece(self.piece, move)
