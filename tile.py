from piece import Piece, SupportivePiece, Pawn


class Tile:
    def __init__(self, pos, piece):
        self.pos = pos
        self.piece = piece
        #WB
        self.zocs = [False, False]
    def __str__(self):
        if self.piece:
            return self.piece.__str__()
        else:
            return " "
    def is_empty(self):
        if self.piece:
            return False
        return True
    #this type of field can be 'captured' by en_passant eligible pieces
    def is_hollow_but_not_empty(self):
        if type(self.piece) == SupportivePiece:
            return True
        return False
    def en_passant_elegible(self):
        if self.piece:
            if type(self.piece) == Pawn:
                return True
            return False
        return False

