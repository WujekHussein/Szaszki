import piece
from piece import EmptyField, Pawn, Rook, Knight, Bishop, Queen, King
import copy
class ChessBoard:
    def __init__(self):
        pieces = [[EmptyField((i, j), bool((i + j) % 2)) for j in range(8)] for i in range(8)]
        #PAWNS
        for i in range(8):
            pieces[1][i] = Pawn((1, i), True)
            pieces[6][i] = Pawn((6, i), False)
        #WHITE
        #rooks
        pieces[0][0] = Rook((0, 0),  True)
        pieces[0][7] = Rook((0, 7),  True)
        #knights
        pieces[0][1] = Knight((0, 1),  True)
        pieces[0][6] = Knight((0, 6),  True)
        # #bishops
        pieces[0][2] = Bishop((0, 2),  True)
        pieces[0][5] = Bishop((0, 5),  True)
        # #queen
        pieces[0][3] = Queen((0, 3),  True)
        # #king
        pieces[0][4] = King((0, 4),  True)
        #BLACK
        # rooks
        pieces[7][0] = Rook((7, 0),  False)
        pieces[7][7] = Rook((7, 7),  False)
        # # knights
        pieces[7][1] = Knight((7, 1),  False)
        pieces[7][6] = Knight((7, 6),  False)
        # # bishops
        pieces[7][2] = Bishop((7, 2),  False)
        pieces[7][5] = Bishop((7, 5),  False)
        # # queen
        pieces[7][3] = Queen((7, 3),  False)
        # # king
        pieces[7][4] = King((7, 4),  False)
        self.pieces = pieces
        self.white_king_pos = (0,4)
        self.black_king_pos = (7,4)
        self.update_zone_of_control()
    def __str__(self):
        letter_line = "    A   B   C   D   E   F   G   H    \n"
        sep_line = "  +---+---+---+---+---+---+---+---+  \n"
        disp = "" #this variable will be appended until done
        disp = letter_line + disp
        disp = sep_line + disp
        for i in range(8):
            row=sep_line
            row+=f"{i+1}"
            for j in range(8):
                row+=" | "
                row+= str(self.pieces[i][j])
            suffix = f" | {i+1}\n"
            row+=suffix
            disp = row + disp
        disp = letter_line + disp
        return disp
    def str_black(self):
        letter_line = "    H   G   F   E   D   C   B   A    \n"
        sep_line = "  +---+---+---+---+---+---+---+---+  \n"
        disp = ""  # this variable will be appended until done
        disp = letter_line + disp
        disp = sep_line + disp
        for i in range(8):
            row=sep_line
            row+=f"{8-i}"
            for j in range(8):
                row+=" | "
                row+= str(self.pieces[7-i][7-j])
            suffix = f" | {8-i}\n"
            row+=suffix
            disp = row + disp
        disp = letter_line + disp
        return disp
    def list_achievable_tiles(self, coords): #used in both update_zone_of_control and move functions, doesn't take checking mechanism into account piece overlap (so it can be used in calculating zoc), but does take into account piece shadowing separate logic will need to be implemented for Pawn
        x, y = coords
        piece = self.pieces[x][y]
        moves = piece.list_moves()
        achievable_tiles = []
        for move in moves:
            xinc, yinc = move
            newx = x + xinc
            newy = y + yinc
            if newx >= 0 and newy >= 0 and newx < 8 and newy < 8:  # checking for possibility of move taking us outside the board or capturing our own piece
                if type(piece) == Knight:
                    achievable_tiles.append((newx, newy))
                else:
                    supportive_var = True
                    intermediates = []# list of intermediate tiles for checking if there's a piece on the way
                    xsgn = (xinc > 0 ) - (xinc < 0)
                    ysgn = (yinc > 0 ) - (yinc < 0)
                    for i in range(1, max(abs(xinc), abs(yinc))):
                        interx = x + i*xsgn
                        intery = y + i*ysgn
                        intermediates.append((interx, intery))
                    for intermediate in intermediates:
                        a, b = intermediate
                        if type(self.pieces[a][b]) != EmptyField:
                            supportive_var = False
                            break
                    if supportive_var:
                        achievable_tiles.append((newx, newy))
        return achievable_tiles
    def update_zone_of_control(self):
        for i in range(8):
            for j in range(8):
                self.pieces[i][j].zoc = set() #clearing previous zocs
        for i in range(8):
            for j in range(8):
                achievable_tiles = self.list_achievable_tiles((i, j))
                for achievable_tile in achievable_tiles:
                    x, y = achievable_tile
                    self.pieces[x][y].zoc.add(self.pieces[i][j].color)

    #checks whether proposed move is possible, if so it applies the move and returns True, otherwise it returns False
    def move(self, coordStart, coordEnd, player_color):
        x, y = coordStart
        z, w = coordEnd
        piece = self.pieces[x][y]
        piece_end = self.pieces[z][w]
        if type(piece) == EmptyField or piece.color != player_color or (piece_end.color == piece.color and type(piece_end) != EmptyField):
            return False
        tiles = self.list_achievable_tiles(coordStart)
        for tile in tiles:
            if tile == coordEnd:
                board_copy = copy.deepcopy(self)
                piece_copy = copy.deepcopy(piece)
                board_copy.pieces[x][y] = EmptyField((x, y), bool((x + y) % 2))
                piece_copy.coords = tile
                newx, newy = tile
                board_copy.pieces[newx][newy] = piece_copy
                board_copy.update_zone_of_control()
                if type(piece) == King:
                    if piece.color:
                        board_copy.white_king_pos = (newx, newy)
                    else:
                        board_copy.black_king_pos = (newx, newy)

                if board_copy.is_valid(player_color):
                    piece.has_moved = True
                    self.pieces[newx][newy] = piece
                    self.pieces[x][y] = EmptyField((x, y), bool((x + y) % 2))
                    self.update_zone_of_control()
                    #updating King's position needed for check function
                    if type(piece) == King:
                        if piece.color:
                            self.white_king_pos = (newx, newy)
                        else:
                            self.black_king_pos = (newx, newy)
                    return True
                else:
                    return False
        return False
    #returns a set of colors that are being in check
    def check(self):
        check_set = set()
        wx, wy = self.white_king_pos
        bx, by = self.black_king_pos
        if False in self.pieces[wx][wy].zoc:
            check_set.add(True)
        if True in self.pieces[bx][by].zoc:
            check_set.add(False)
        return check_set
    #checking for whether the player that just moved isn't in check (that would be silly)
    def is_valid(self, player_color):
        if player_color in self.check():
            return False
        return True
    def print_zone_of_control(self):
        letter_line = "    A   B   C   D   E   F   G   H    \n"
        sep_line = "  +---+---+---+---+---+---+---+---+  \n"
        disp = ""  # this variable will be appended until done
        disp = letter_line + disp
        disp = sep_line + disp
        for i in range(8):
            row = sep_line
            row += f"{i + 1}"
            for j in range(8):
                row += " | "
                piece = self.pieces[i][j]
                if True in piece.zoc and False in piece.zoc:
                    zoc_char = "3"
                elif False in piece.zoc:
                    zoc_char = "2"
                elif True in piece.zoc:
                    zoc_char = "1"
                else:
                    zoc_char = "0"
                row += zoc_char
            suffix = f" | {i + 1}\n"
            row += suffix
            disp = row + disp
        disp = letter_line + disp
        return disp
    #checks whether there's mate or not
    def does_not_have_legal_moves(self, player):
    #we go through all the pieces (it is necessarily possible to do it simpler)
        for i in range(8):
            for j in range(8):
                if self.pieces[i][j].color == player:
                    achievable_tiles = self.list_achievable_tiles((i, j))
                    for achievable_tile in achievable_tiles:
                        x, y = achievable_tile
                        if type(self.pieces[x][y]) == EmptyField or self.pieces[x][y].color != player:
                            board_copy = copy.deepcopy(self)
                            piecec = board_copy.pieces[i][j]
                            piecec.coords = achievable_tile
                            board_copy.pieces[i][j] = EmptyField((i, j), bool((i + j) % 2))
                            board_copy.pieces[x][y] = piecec
                            board_copy.update_zone_of_control()
                            if type(piecec) == King:
                                if piecec.color:
                                    board_copy.white_king_pos = (x, y)
                                else:
                                    board_copy.black_king_pos = (x, y)
                            if board_copy.is_valid(player):
                                # print(board_copy)
                                # print((i,j))
                                # print((x,y))
                                return False


        return True
    #checks whether there's a tie or not
    def tie(self, player):
        return False





