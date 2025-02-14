from abc import ABC, abstractmethod
class Piece(ABC):
    @abstractmethod
    def __init__(self, player):
        #white=false, black=true
        self.player = player
        self.has_moved = False
        self.ttl = -1
    #returns relative position of piece that should be taken of the board upon capture (is not always (0,0) because of en passant mechanism)

    @abstractmethod
    def destruction_vector(self):
        pass

    #returns list of vectors pointing to tiles that may be controlled by our piece
    @abstractmethod
    def possibly_controlled_tiles(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
    def update_ttl(self):
        self.ttl -= 1



class SupportivePiece(Piece):
    def __init__(self, player):
        super().__init__(player)
        #will go through zero
        self.ttl=1

    def destruction_vector(self):
        return ((-1)**self.player, 0)

    def possibly_controlled_tiles(self):
        return []

    def __str__(self):
        return " "



class MovingPiece(Piece, ABC):  
    def __init__(self, player):
        super().__init__(player)

    def destruction_vector(self):
        return (0,0)

    @abstractmethod
    def possibly_controlled_tiles(self):
        pass

    @abstractmethod
    def __str__(self):
        pass



class Pawn(MovingPiece):
    def __init__(self, player):
        super().__init__(player)

    def __str__(self):
        return chr(80+32*self.player)

    def possibly_controlled_tiles(self):
        return [((-1)**self.player,-1), ((-1)**self.player,1)]



class Rook(MovingPiece):
    def __init__(self, player):
        super().__init__(player)

    def __str__(self):
        return chr(82+32*self.player)

    # 4 dirs max displacement is 7
    def possibly_controlled_tiles(self):
        tiles = []
        for i in range(1,8):
            tiles.append((i,0))
            tiles.append((-i,0))
            tiles.append((0,i))
            tiles.append((0,-i))
        return tiles




class Knight(MovingPiece):
    def __init__(self, player):
        super().__init__(player)

    def __str__(self):
        return chr(78+32*self.player)

    def possibly_controlled_tiles(self):
        tiles = []
        xinc = [-2, -1, 1, 2]
        yinc = [-2, -1, 1, 2]
        for i in xinc:
            for j in yinc:
                if abs(i)!=abs(j):
                    tiles.append((i,j))
        return tiles





class Bishop(MovingPiece):
    def __init__(self, player):
        super().__init__(player)

    def __str__(self):
        return chr(66 + 32 * self.player)

    # similar to rook, this time directions are diagonal
    def possibly_controlled_tiles(self):
        tiles = []
        for i in range(1, 8):
            tiles.append((i, i))
            tiles.append((-i, i))
            tiles.append((i, -i))
            tiles.append((-i, -i))
        return tiles







class Queen(MovingPiece):
    def __init__(self, player):
        super().__init__( player)

    def __str__(self):
        return chr(81+32*self.player)

    # combining rook and bishop
    def possibly_controlled_tiles(self):
        tiles = []
        for i in range(1, 8):
            tiles.append((i, 0))
            tiles.append((-i, 0))
            tiles.append((0, i))
            tiles.append((0, -i))
            tiles.append((i, i))
            tiles.append((-i, i))
            tiles.append((i, -i))
            tiles.append((-i, -i))
        return tiles






class King(MovingPiece):
    def __init__(self, player):
        super().__init__(player)

    def __str__(self):
        return chr(75+32*self.player)

    def possibly_controlled_tiles(self):
        tiles = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not (i == 0 and j == 0):
                    tiles.append((i, j))
        return tiles






