from abc import ABC, abstractmethod
class Piece(ABC):
    @abstractmethod
    def __init__(self, coords, color):
        self.coords = coords
        self.color = color
        self.zoc = set()
        self.has_moved = False
    #returns list of possible relative changes in pos, doesn't care about piece position
    @abstractmethod
    def list_moves(self):
        pass
    @abstractmethod
    def update_zone_of_control(self, board):
        pass
    @abstractmethod
    def __str__(self):
        pass
class EmptyField(Piece):
    def __init__(self, coords, color):
        super().__init__(coords, color)
    def list_moves(self):
        return []
    def update_zone_of_control(self, board):
        pass
    def __str__(self):
        return " "
class Pawn(Piece):
    def __init__(self, coords, color):
        super().__init__(coords, color)
    def list_moves(self):
        if self.has_moved:
            return [(-(-1)**self.color,0)]
        return [(-(-1)**self.color,0), (-2*(-1)**self.color,0)]
    #fuck en passant
    def update_zone_of_control(self, board):
        x, y = self.coords
        next_row = x - (-1)**(self.color)
        if next_row < len(board.pieces) and next_row >= 0:
            if y>0:
                board.pieces[next_row][y-1].zoc.add(self.color)
            if y<len(board.pieces)-1:
                board.pieces[next_row][y+1].zoc.add(self.color)

    def __str__(self):
        return chr(112-32*self.color)
class Rook(Piece):
    def __init__(self, coords, color):
        super().__init__(coords, color)
    def list_moves(self):
        #4 dirs max displacement is 7
        moves = []
        for i in range(1,8):
            moves.append((i,0))
            moves.append((-i,0))
            moves.append((0,i))
            moves.append((0,-i))
        return moves
    def update_zone_of_control(self, board):
        x, y = self.coords

        #4 loops 4 directions
        #north
        it = x+1
        while(it<8):
            board.pieces[it][y].zoc.add(self.color)
            if type(board.pieces[it][y]) != EmptyField:
                break
            it+=1
        #east
        it = y+1
        while(it<8):
            board.pieces[x][it].zoc.add(self.color)
            if type(board.pieces[x][it]) != EmptyField:
                break
            it+=1
        #south
        it = x - 1
        while (it >= 0):
            board.pieces[it][y].zoc.add(self.color)
            if type(board.pieces[it][y]) != EmptyField:
                break
            it -= 1
        #west
        it = y - 1
        while (it >= 0):
            board.pieces[x][it].zoc.add(self.color)
            if type(board.pieces[x][it]) != EmptyField:
                break
            it -= 1

    def __str__(self):
        return chr(114-32*self.color)
class Knight(Piece):
    def __init__(self, coords, color):
        super().__init__(coords, color)
    def list_moves(self):
        moves = []
        xinc = [-2, -1, 1, 2]
        yinc = [-2, -1, 1, 2]
        for i in xinc:
            for j in yinc:
                if abs(i)!=abs(j):
                    moves.append((i,j))
        return moves

    def update_zone_of_control(self, board):
        x, y = self.coords
        xinc = [-2, -1, 1, 2]
        yinc = [-2, -1, 1, 2]
        for i in xinc:
            for j in yinc:
                if abs(i)!=abs(j):
                    x_new = x + i
                    y_new = y + j
                    if(x_new>=0 and x_new<8 and y_new>=0 and y_new<8):
                        board.pieces[x_new][y_new].zoc.add(self.color)
    def __str__(self):
        return chr(110-32*self.color)
class Bishop(Piece):
    def __init__(self, coords, color):
        super().__init__(coords, color)
    def list_moves(self):
        #similar to rook, this time directions are diagonal
        moves = []
        for i in range(1, 8):
            moves.append((i, i))
            moves.append((-i, i))
            moves.append((i, -i))
            moves.append((-i, -i))
        return moves
    def update_zone_of_control(self, board):
        x ,y = self.coords
        #again 4 directions
        #NE
        itx = x+1
        ity = y+1
        while(itx<8 and ity<8):
            board.pieces[itx][ity].zoc.add(self.color)
            if type(board.pieces[itx][ity]) != EmptyField:
                break
            itx+=1
            ity+=1
        #SE
        itx = x-1
        ity = y+1
        while(itx>=0 and ity<8):
            board.pieces[itx][ity].zoc.add(self.color)
            if type(board.pieces[itx][ity]) != EmptyField:
                break
            itx -= 1
            ity += 1
        #SW
        itx = x-1
        ity = y-1
        while(itx>=0 and ity>=0):
            board.pieces[itx][ity].zoc.add(self.color)
            if type(board.pieces[itx][ity]) != EmptyField:
                break
            itx -= 1
            ity -= 1
        #NW
        itx = x+1
        ity = y-1
        while(itx<8 and ity>=0):
            board.pieces[itx][ity].zoc.add(self.color)
            if type(board.pieces[itx][ity]) != EmptyField:
                break
            itx += 1
            ity -= 1
    def __str__(self):
        return chr(98-32*self.color)
class Queen(Piece):
    def __init__(self, coords, color):
        super().__init__(coords, color)
    def list_moves(self):
        #combining rook and bishop
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
    def update_zone_of_control(self, board):
        #implements logic of rook and bishop simultaneously
        x, y = self.coords

        # 4 loops 4 directions
        # north
        it = x + 1
        while (it < 8):
            board.pieces[it][y].zoc.add(self.color)
            if type(board.pieces[it][y]) != EmptyField:
                break
            it += 1
        # east
        it = y + 1
        while (it < 8):
            board.pieces[x][it].zoc.add(self.color)
            if type(board.pieces[x][it]) != EmptyField:
                break
            it += 1
        # south
        it = x - 1
        while (it >= 0):
            board.pieces[it][y].zoc.add(self.color)
            if type(board.pieces[it][y]) != EmptyField:
                break
            it -= 1
        # west
        it = y - 1
        while (it >= 0):
            board.pieces[x][it].zoc.add(self.color)
            if type(board.pieces[x][it]) != EmptyField:
                break
            it -= 1
        # NE
        itx = x + 1
        ity = y + 1
        while (itx < 8 and ity < 8):
            board.pieces[itx][ity].zoc.add(self.color)
            if type(board.pieces[itx][ity]) != EmptyField:
                break
            itx += 1
            ity += 1
        # SE
        itx = x - 1
        ity = y + 1
        while (itx >= 0 and ity < 8):
            board.pieces[itx][ity].zoc.add(self.color)
            if type(board.pieces[itx][ity]) != EmptyField:
                break
            itx -= 1
            ity += 1
        # SW
        itx = x - 1
        ity = y - 1
        while (itx >= 0 and ity >= 0):
            board.pieces[itx][ity].zoc.add(self.color)
            if type(board.pieces[itx][ity]) != EmptyField:
                break
            itx -= 1
            ity -= 1
        # NW
        itx = x + 1
        ity = y - 1
        while (itx < 8 and ity >= 0):
            board.pieces[itx][ity].zoc.add(self.color)
            if type(board.pieces[itx][ity]) != EmptyField:
                break
            itx += 1
            ity -= 1
    def __str__(self):
        return chr(113-32*self.color)
class King(Piece):
    def __init__(self, coords, color):
        super().__init__(coords, color)
    def list_moves(self):
        moves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not (i == 0 and j == 0):
                    moves.append((i, j))
        return moves

    def update_zone_of_control(self, board):
        x, y = self.coords
        xinc = [-1, 0, 1]
        yinc = [-1, 0, 1]
        for i in xinc:
            for j in yinc:
                if x!=0 or y!=0:
                    new_x = x + i
                    new_y = y + j
                    if new_x<8 and new_x>=0 and new_y<8 and new_y>=0:
                        board.pieces[new_x][new_y].zoc.add(self.color)
    def __str__(self):
        return chr(107-32*self.color)



