class Tile:
    def __init__(self, pos, piece):
        self.pos = pos
        self.piece = piece
        self.in_white_zoc = False
        self.in_black_zoc = False
        self.en_passant = False
    def __str__(self):
        if self.piece:
            return self.piece.__str__()
        else:
            return " "
