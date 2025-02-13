from abc import ABC, abstractmethod
class Piece(ABC):
    @abstractmethod
    def __init__(self, color):
        self.color = color
        self.has_moved = False
    #returns list of possible changes in position
    @abstractmethod
    def list_moves(self):
        pass
    @abstractmethod
    def list_zoc_tiles(self):
        pass
    @abstractmethod
    def __str__(self):
        pass



class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)

    def list_moves(self):
        if self.has_moved:
            return [(-(-1)**self.color,0)]
        return [(-(-1)**self.color,0), (-2*(-1)**self.color,0)]
    def list_zoc_tiles(self):
        return [(-(-1)**self.color, -1), (-(-1)**self.color, 1)]

    def __str__(self):
        return chr(112-32*self.color)



class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)

    # 4 dirs max displacement is 7
    def list_moves(self):

        moves = []
        for i in range(1,8):
            moves.append((i,0))
            moves.append((-i,0))
            moves.append((0,i))
            moves.append((0,-i))
        return moves
    def list_zoc_tiles(self):
        return self.list_moves()
    def __str__(self):
        return chr(114-32*self.color)



class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

    def list_moves(self):
        moves = []
        xinc = [-2, -1, 1, 2]
        yinc = [-2, -1, 1, 2]
        for i in xinc:
            for j in yinc:
                if abs(i)!=abs(j):
                    moves.append((i,j))
        return moves
    def list_zoc_tiles(self):
        return self.list_moves()
    def __str__(self):
        return chr(110-32*self.color)



class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    # similar to rook, this time directions are diagonal
    def list_moves(self):
        moves = []
        for i in range(1, 8):
            moves.append((i, i))
            moves.append((-i, i))
            moves.append((i, -i))
            moves.append((-i, -i))
        return moves

    def list_zoc_tiles(self):
        return self.list_moves()

    def __str__(self):
        return chr(98-32*self.color)



class Queen(Piece):
    def __init__(self, color):
        super().__init__( color)

    # combining rook and bishop
    def list_moves(self):
        moves = []
        for i in range(1, 8):
            moves.append((i, 0))
            moves.append((-i, 0))
            moves.append((0, i))
            moves.append((0, -i))
            moves.append((i, i))
            moves.append((-i, i))
            moves.append((i, -i))
            moves.append((-i, -i))
        return moves

    def list_zoc_tiles(self):
        return self.list_moves()

    def __str__(self):
        return chr(113-32*self.color)



class King(Piece):
    def __init__(self, color):
        super().__init__(color)

    def list_moves(self):
        moves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not (i == 0 and j == 0):
                    moves.append((i, j))
        return moves

    def list_zoc_tiles(self):
        return self.list_moves()

    def __str__(self):
        return chr(107-32*self.color)


