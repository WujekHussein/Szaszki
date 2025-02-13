import piece
from tile import Tile
from piece import Pawn, Rook, Knight, Bishop, Queen, King
import copy
class ChessBoard:
    def __init__(self):
        tiles = [[Tile((i, j), None) for j in range(8)] for i in range(8)]
        #PAWNS
        for i in range(8):
            tiles[1][i].piece = Pawn(True)
            tiles[6][i].piece = Pawn(False)

        #rooks
        tiles[0][0].piece = Rook(True)
        tiles[0][7].piece = Rook(True)
        tiles[7][0].piece = Rook(False)
        tiles[7][7].piece = Rook(False)

        #knights
        tiles[0][1].piece = Knight(True)
        tiles[0][6].piece = Knight(True)
        tiles[7][1].piece = Knight(False)
        tiles[7][6].piece = Knight(False)

        #bishops
        tiles[0][2].piece = Bishop(True)
        tiles[0][5].piece = Bishop(True)
        tiles[7][2].piece = Bishop(False)
        tiles[7][5].piece = Bishop(False)

        #queen
        tiles[0][3].piece = Queen(True)
        tiles[7][3].piece = Queen(False)

        #king
        tiles[0][4].piece = King(True)
        tiles[7][4].piece = King(False)


        self.tiles = tiles
        self.update_board_info()
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
                row+= str(self.tiles[i][j])
            suffix = f" | {i+1}\n"
            row+=suffix
            disp = row + disp
        disp = letter_line + disp
        return disp
    # def str_black(self):
    #     letter_line = "    H   G   F   E   D   C   B   A    \n"
    #     sep_line = "  +---+---+---+---+---+---+---+---+  \n"
    #     disp = ""  # this variable will be appended until done
    #     disp = letter_line + disp
    #     disp = sep_line + disp
    #     for i in range(8):
    #         row=sep_line
    #         row+=f"{8-i}"
    #         for j in range(8):
    #             row+=" | "
    #             row+= str(self.tiles[7-i][7-j])
    #         suffix = f" | {8-i}\n"
    #         row+=suffix
    #         disp = row + disp
    #     disp = letter_line + disp
    #     return disp

    # used in both update_zone_of_control and move functions, doesn't take checking mechanism  and piece overlap into account  (so it can be used in calculating zoc), but does take into account piece shadowing separate logic will need to be implemented for Pawn
    def list_controlled_tiles(self, coords):
        x, y = coords
        tile = self.tiles[x][y]
        piece = tile.piece
        if piece:
            moves = piece.list_zoc_tiles()
            controlled_tiles = []
            for move in moves:
                xinc, yinc = move
                #coords of piece after move
                newx = x + xinc
                newy = y + yinc
                #
                if newx >= 0 and newy >= 0 and newx < 8 and newy < 8:  # checking for possibility of move taking us outside the board
                    #knight can jump
                    if type(piece) == Knight:
                        controlled_tiles.append((newx, newy))
                    else:
                        supportive_var = True
                        # list of intermediate tiles for checking if there's a piece on the way
                        intermediates = []
                        xsgn = (xinc > 0 ) - (xinc < 0)
                        ysgn = (yinc > 0 ) - (yinc < 0)
                        #works for horizontal, vertical and diagonal moves
                        for i in range(1, max(abs(xinc), abs(yinc))):
                            interx = x + i*xsgn
                            intery = y + i*ysgn
                            intermediates.append((interx, intery))
                        for intermediate in intermediates:
                            a, b = intermediate
                            if self.tiles[a][b].piece:
                                supportive_var = False
                                break
                        if supportive_var:
                            controlled_tiles.append((newx, newy))
            return controlled_tiles
        #if tile has no piece
        return []
    def list_achievable_tiles(self, coords):
        x, y = coords
        tile = self.tiles[x][y]
        piece = tile.piece
        if piece:
            moves = piece.list_moves()
            achievable_tiles = []
            for move in moves:
                xinc, yinc = move
                # coords of piece after move
                newx = x + xinc
                newy = y + yinc
                #
                if newx >= 0 and newy >= 0 and newx < 8 and newy < 8:  # checking for possibility of move taking us outside the board
                    # knight can jump
                    if type(piece) == Knight:
                        achievable_tiles.append((newx, newy))
                    else:
                        supportive_var = True
                        # list of intermediate tiles for checking if there's a piece on the way
                        intermediates = []
                        xsgn = (xinc > 0) - (xinc < 0)
                        ysgn = (yinc > 0) - (yinc < 0)
                        # works for horizontal, vertical and diagonal moves
                        for i in range(1, max(abs(xinc), abs(yinc))):
                            interx = x + i * xsgn
                            intery = y + i * ysgn
                            intermediates.append((interx, intery))
                        for intermediate in intermediates:
                            a, b = intermediate
                            if self.tiles[a][b].piece:
                                supportive_var = False
                                break
                        if supportive_var:
                            achievable_tiles.append((newx, newy))
            return achievable_tiles
        # if tile has no piece
        return []
    #sets up correct zocs for tiles and kings' postitions
    def update_board_info(self):
        #clearing up old zones
        for i in range(8):
            for j in range(8):
                self.tiles[i][j].in_white_zoc = False
                self.tiles[i][j].in_black_zoc = False
        for i in range(8):
            for j in range(8):
                controlled_tiles = self.list_controlled_tiles((i, j))
                if self.tiles[i][j].piece:
                    color = self.tiles[i][j].piece.color
                for controlled_tile in controlled_tiles:
                    x, y = controlled_tile
                    if color:
                        self.tiles[x][y].in_white_zoc = True
                    else:
                        self.tiles[x][y].in_black_zoc = True
                if type(self.tiles[i][j].piece) == King:
                    if color:
                        self.white_king_pos = (i, j)
                    else:
                        self.black_king_pos = (i, j)
    #checks whether provided player is in check
    def check(self, player):
        if player:
            x,y = self.white_king_pos
            if self.tiles[x][y].in_black_zoc:
                return True
            return False
        else:
            x,y = self.black_king_pos
            if self.tiles[x][y].in_white_zoc:
                return True
            return False
    #cheks whether board position with provided player on move is valid
    def is_valid(self, player):
        if self.check(not player):
            return False
        return True

    def list_legal_tiles(self, coord, player):
        legal_tiles = []
        x, y = coord
        tile_origin = self.tiles[x][y]
        achievable_tiles = self.list_achievable_tiles(coord)
        #legal tiles are subset of controlled tiles
        for controlled_tile in achievable_tiles:
            z, w = controlled_tile
            tile_destination = self.tiles[z][w]
            if ((not tile_destination.piece) or (tile_destination.piece.color != player)) and (tile_origin.piece.color == player):
                board_copy = copy.deepcopy(self)
                piece = board_copy.tiles[x][y].piece
                board_copy.tiles[x][y].piece = None
                piece.has_moved = True
                board_copy.tiles[z][w].piece = piece
                board_copy.update_board_info()
                if board_copy.is_valid(not player):
                    legal_tiles.append((z, w))
        return legal_tiles



    # applies proposed move if possible
    def move(self, coordStart, coordEnd, player):
        x, y = coordStart
        legal_tiles = self.list_legal_tiles(coordStart, player)
        if coordEnd in legal_tiles:
            z, w = coordEnd
            moved_piece = self.tiles[x][y].piece
            self.tiles[x][y].piece = None
            moved_piece.has_moved = True
            self.tiles[z][w].piece = moved_piece
            self.update_board_info()
            return True
        return False
    # def print_zone_of_control(self):
    #     letter_line = "    A   B   C   D   E   F   G   H    \n"
    #     sep_line = "  +---+---+---+---+---+---+---+---+  \n"
    #     disp = ""  # this variable will be appended until done
    #     disp = letter_line + disp
    #     disp = sep_line + disp
    #     for i in range(8):
    #         row = sep_line
    #         row += f"{i + 1}"
    #         for j in range(8):
    #             row += " | "
    #             piece = self.tiles[i][j]
    #             if True in piece.zoc and False in piece.zoc:
    #                 zoc_char = "3"
    #             elif False in piece.zoc:
    #                 zoc_char = "2"
    #             elif True in piece.zoc:
    #                 zoc_char = "1"
    #             else:
    #                 zoc_char = "0"
    #             row += zoc_char
    #         suffix = f" | {i + 1}\n"
    #         row += suffix
    #         disp = row + disp
    #     disp = letter_line + disp
    #     return disp
    #checks whether there are legal moves or not
    def does_not_have_legal_moves(self, player):
        for i in range(8):
            for j in range(8):
                if self.tiles[i][j].piece and self.tiles[i][j].piece.color == player:
                    legal_moves = self.list_legal_tiles((i, j), player)
                    if legal_moves:
                        return False
        return True
    #function assumes player is castling his own pieces
    def castle(self, long, player):
        kocol = 4
        if player:
            row = 0
        else:
            row = 7
        if long:
            rcol = 0
            kdcol = 2
            rdcol=3
        else:
            rcol = 7
            kdcol = 6
            rdcol = 5
        king_tile = self.tiles[row][kocol]
        king = king_tile.piece
        rook = self.tiles[row][rcol].piece
        dest_tile = self.tiles[row][kdcol]
        #sanity check
        if rook.has_moved or king.has_moved:
            return False
        rightwards = kdcol-kocol > 0
        oneorminusone = -1 + 2*rightwards
        #checking for free passage
        for i in range(kocol, kdcol+oneorminusone, oneorminusone):
            if (i!=kocol and self.tiles[row][i].piece):
                return False
            if player:
                if self.tiles[row][i].in_black_zoc:
                    return False
            else:
                if self.tiles[row][i].in_white_zoc:
                    return False
        #checks done

        self.tiles[row][kocol].piece = None
        king.has_moved = True
        self.tiles[row][kdcol].piece = king
        self.tiles[row][rcol].piece = None
        rook.has_moved = True
        self.tiles[row][rdcol].piece = rook
        self.update_board_info()
        return True







