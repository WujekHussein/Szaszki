import piece
from tile import Tile
from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King, SupportivePiece
import copy
class ChessBoard:
    def __init__(self):
        self.player = False
        self.legal_moves = [[[] for i in range(8)] for j in range(8)]
        tiles = [[Tile((i, j), None) for j in range(8)] for i in range(8)]
        #PAWNS
        for i in range(8):
            tiles[1][i].piece = Pawn(False)
            tiles[6][i].piece = Pawn(True)

        #rooks
        tiles[0][0].piece = Rook(False)
        tiles[0][7].piece = Rook(False)
        tiles[7][0].piece = Rook(True)
        tiles[7][7].piece = Rook(True)

        #knights
        tiles[0][1].piece = Knight(False)
        tiles[0][6].piece = Knight(False)
        tiles[7][1].piece = Knight(True)
        tiles[7][6].piece = Knight(True)

        #bishops
        tiles[0][2].piece = Bishop(False)
        tiles[0][5].piece = Bishop(False)
        tiles[7][2].piece = Bishop(True)
        tiles[7][5].piece = Bishop(True)

        #queen
        tiles[0][3].piece = Queen(False)
        tiles[7][3].piece = Queen(True)

        #king
        tiles[0][4].piece = King(False)
        tiles[7][4].piece = King(True)
        tiles[2][1].piece = Knight(True)

        self.tiles = tiles
        self.kings_positions = [(0,4), (7,4)]
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



    #checks in a predefined array
    def is_move_legal(self, origin_coord, destination_coord):
        x, y = origin_coord
        return destination_coord in self.legal_moves[x][y]


    #doesn't care about legality
    def change_position(self, origin_coord, destination_coord):
        x, y = origin_coord
        z, w = destination_coord
        moved_piece = self.tiles[x][y].piece
        moved_piece.has_moved = True
        self.tiles[x][y].piece = None
        self.tiles[z][w].piece = moved_piece



    #tries to apply proposed move returns True and changes the board accordingly if successful, returns False otherwise
    def move(self, origin_coord, destination_coord):
        if self.is_move_legal(origin_coord, destination_coord):
            self.change_position(origin_coord, destination_coord)
            #Update_board_info_tu będzie wywołane
            return True
        return False


    #omits origin coord and destination coord works only for vertical horizontal and strictly diagonal lines
    def list_intermediate_coordinates(self, origin_coord, destination_coord):
        intermediates = []
        x, y = origin_coord
        z, w = destination_coord
        dx = z-x
        dy = w-y
        if x==z or y==w or x-y==z-w or x+y==z+w:
            sgndx = (dx > 0 ) - (dx < 0)
            sgndy = (dy > 0 ) - (dy < 0)
            dynx = x
            dyny = y
            for i in range(max(abs(dx), abs(dy))-1):
                dynx += sgndx
                dyny += sgndy
                intermediates.append((dynx, dyny))

        return intermediates


    #just adds origin_coord to piece possibly_controlled_tiles coordinatewise and checks if the result fits on the board
    def list_possibly_controlled_coordinates(self, origin_coord):
        possibly_controlled = []
        x, y = origin_coord
        origin_piece = self.tiles[x][y].piece
        if origin_piece:
            possible_vectors = origin_piece.possibly_controlled_tiles()
            for vector in possible_vectors:
                z, w = vector
                newx = x+z
                newy = y+w
                if newx>=0 and newx<8 and newy>=0 and newy<8:
                    possibly_controlled.append((newx, newy))
        return possibly_controlled

    def list_controlled_coordinates(self, origin_coord):
        controlled = []
        possibly_controlled = self.list_possibly_controlled_coordinates(origin_coord)

        for possibility in possibly_controlled:
            intermediates = self.list_intermediate_coordinates(origin_coord, possibility)
            no_obstacle_flag = True
            #Knight moves don't have intermediates so it will act as jumping over pieces
            for intermediate in intermediates:
                x, y = intermediate
                intemediate_tile = self.tiles[x][y]
                if not (intemediate_tile.is_empty() or intemediate_tile.is_hollow_but_not_empty()):
                    no_obstacle_flag = False
                    break
            if no_obstacle_flag:
                controlled.append(possibility)
        return controlled



    def update_zoc(self):
        #clearing
        for i in range(8):
            for j in range(8):
                self.tiles[i][j].zocs = [False, False]
        for i in range(8):
            for j in range(8):
                controlling_piece = self.tiles[i][j].piece
                if controlling_piece:
                    player = controlling_piece.player
                    controlled_coords = self.list_controlled_coordinates((i,j))
                    for coord in controlled_coords:
                        x, y = coord
                        tile = self.tiles[x][y]
                        tile.zocs[player] = True



    def update_board_info(self):
        self.update_zoc()
        self.update_ttl_and_possibly_remove()
        self.update_kings_positions()



    def update_ttl_and_possibly_remove(self):
        for i in range(8):
            for j in range(8):
                piece = self.tiles[i][j].piece
                if piece:
                    piece.ttl -= 1
                    #will remove only en passant guys who will be added after executing this function so they will last on enemy's turn
                    if piece.ttl == 0:
                        self.tiles[i][j].piece = None



    def update_kings_positions(self):
        for i in range(8):
            for j in range(8):
                piece = self.tiles[i][j].piece
                if type(piece) == King:
                    self.kings_positions[piece.player] = (i,j)
    # checks if the player on the move is in check
    def check(self):
        king_pos = self.kings_positions[self.player]
        x, y = king_pos
        king_tile = self.tiles[x][y]
        if king_tile.zocs[not self.player]:
            return True
        return False


    def list_accessible_coordinates(self, origin_coord):
        x, y = origin_coord
        piece = self.tiles[x][y].piece
        if not piece:
            return []
        accessible = []
        if type(piece) != Pawn:
            #logic for not letting capturing own pieces
            controlled_tiles = self.list_controlled_coordinates(origin_coord)
            for tile in controlled_tiles:
                x, y = tile
                controlled_piece = self.tiles[x][y].piece
                if not controlled_piece or (controlled_piece and controlled_piece.player != self.player):
                    accessible.append(tile)
            return accessible
        pawn_controlled = self.list_controlled_coordinates(origin_coord)
        for coord in pawn_controlled:
            z, w = coord
            controlled_piece = self.tiles[z][w].piece
            if controlled_piece and controlled_piece.player != piece.player:
                accessible.append(coord)
        forward_x = x + (-1)**(piece.player)
        if forward_x >= 0 and forward_x < 8 and not self.tiles[forward_x][y].piece:
            accessible.append((forward_x, y))
            forward_x += (-1)**(piece.player)
            if (not piece.has_moved) and (forward_x >= 0) and (forward_x < 8) and (not self.tiles[forward_x][y].piece):
                accessible.append((forward_x,y))
        return accessible



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
    #             zoc = self.tiles[i][j].zocs
    #             if zoc == [True, True]:
    #                 zoc_char = "3"
    #             elif zoc == [False, True]:
    #                 zoc_char = "2"
    #             elif zoc == [True, False]:
    #                 zoc_char = "1"
    #             else:
    #                 zoc_char = "0"
    #             row += zoc_char
    #         suffix = f" | {i + 1}\n"
    #         row += suffix
    #         disp = row + disp
    #     disp = letter_line + disp
    #     return disp

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
    # def list_controlled_tiles(self, coords):
    #     x, y = coords
    #     tile = self.tiles[x][y]
    #     piece = tile.piece
    #     if piece:
    #         moves = piece.list_zoc_tiles()
    #         controlled_tiles = []
    #         for move in moves:
    #             xinc, yinc = move
    #             #coords of piece after move
    #             newx = x + xinc
    #             newy = y + yinc
    #             #
    #             if newx >= 0 and newy >= 0 and newx < 8 and newy < 8:  # checking for possibility of move taking us outside the board
    #                 #knight can jump
    #                 if type(piece) == Knight:
    #                     controlled_tiles.append((newx, newy))
    #                 else:
    #                     supportive_var = True
    #                     # list of intermediate tiles for checking if there's a piece on the way
    #                     intermediates = []
    #                     xsgn = (xinc > 0 ) - (xinc < 0)
    #                     ysgn = (yinc > 0 ) - (yinc < 0)
    #                     #works for horizontal, vertical and diagonal moves
    #                     for i in range(1, max(abs(xinc), abs(yinc))):
    #                         interx = x + i*xsgn
    #                         intery = y + i*ysgn
    #                         intermediates.append((interx, intery))
    #                     for intermediate in intermediates:
    #                         a, b = intermediate
    #                         if self.tiles[a][b].piece:
    #                             supportive_var = False
    #                             break
    #                     if supportive_var:
    #                         controlled_tiles.append((newx, newy))
    #         return controlled_tiles
    #     #if tile has no piece
    #     return []
    # def list_achievable_tiles(self, coords):
    #     x, y = coords
    #     tile = self.tiles[x][y]
    #     piece = tile.piece
    #     if piece:
    #         moves = piece.list_moves()
    #         achievable_tiles = []
    #         for move in moves:
    #             xinc, yinc = move
    #             # coords of piece after move
    #             newx = x + xinc
    #             newy = y + yinc
    #             #
    #             if newx >= 0 and newy >= 0 and newx < 8 and newy < 8:  # checking for possibility of move taking us outside the board
    #                 # knight can jump
    #                 if type(piece) == Knight:
    #                     achievable_tiles.append((newx, newy))
    #                 else:
    #                     supportive_var = True
    #                     # list of intermediate tiles for checking if there's a piece on the way
    #                     intermediates = []
    #                     xsgn = (xinc > 0) - (xinc < 0)
    #                     ysgn = (yinc > 0) - (yinc < 0)
    #                     # works for horizontal, vertical and diagonal moves
    #                     for i in range(1, max(abs(xinc), abs(yinc))):
    #                         interx = x + i * xsgn
    #                         intery = y + i * ysgn
    #                         intermediates.append((interx, intery))
    #                     for intermediate in intermediates:
    #                         a, b = intermediate
    #                         if self.tiles[a][b].piece:
    #                             supportive_var = False
    #                             break
    #                     if supportive_var:
    #                         achievable_tiles.append((newx, newy))
    #         return achievable_tiles
    #     # if tile has no piece
    #     return []
    # #sets up correct zocs for tiles and kings' postitions
    # def update_board_info(self):
    #     #clearing up old zones
    #     for i in range(8):
    #         for j in range(8):
    #             self.tiles[i][j].in_white_zoc = False
    #             self.tiles[i][j].in_black_zoc = False
    #     for i in range(8):
    #         for j in range(8):
    #             controlled_tiles = self.list_controlled_tiles((i, j))
    #             if self.tiles[i][j].piece:
    #                 color = self.tiles[i][j].piece.color
    #             for controlled_tile in controlled_tiles:
    #                 x, y = controlled_tile
    #                 if color:
    #                     self.tiles[x][y].in_white_zoc = True
    #                 else:
    #                     self.tiles[x][y].in_black_zoc = True
    #             if type(self.tiles[i][j].piece) == King:
    #                 if color:
    #                     self.white_king_pos = (i, j)
    #                 else:
    #                     self.black_king_pos = (i, j)
    # #checks whether provided player is in check
    # def check(self, player):
    #     if player:
    #         x,y = self.white_king_pos
    #         if self.tiles[x][y].in_black_zoc:
    #             return True
    #         return False
    #     else:
    #         x,y = self.black_king_pos
    #         if self.tiles[x][y].in_white_zoc:
    #             return True
    #         return False
    # #cheks whether board position with provided player on move is valid
    # def is_valid(self, player):
    #     if self.check(not player):
    #         return False
    #     return True
    #
    # def list_legal_tiles(self, coord, player):
    #     legal_tiles = []
    #     x, y = coord
    #     tile_origin = self.tiles[x][y]
    #     achievable_tiles = self.list_achievable_tiles(coord)
    #     #legal tiles are subset of controlled tiles
    #     for controlled_tile in achievable_tiles:
    #         z, w = controlled_tile
    #         tile_destination = self.tiles[z][w]
    #         if ((not tile_destination.piece) or (tile_destination.piece.color != player)) and (tile_origin.piece.color == player):
    #             board_copy = copy.deepcopy(self)
    #             piece = board_copy.tiles[x][y].piece
    #             board_copy.tiles[x][y].piece = None
    #             piece.has_moved = True
    #             board_copy.tiles[z][w].piece = piece
    #             board_copy.update_board_info()
    #             if board_copy.is_valid(not player):
    #                 legal_tiles.append((z, w))
    #     return legal_tiles
    #
    #
    #
    # # applies proposed move if possible
    # def move(self, coordStart, coordEnd, player):
    #     x, y = coordStart
    #     legal_tiles = self.list_legal_tiles(coordStart, player)
    #     if coordEnd in legal_tiles:
    #         z, w = coordEnd
    #         moved_piece = self.tiles[x][y].piece
    #         self.tiles[x][y].piece = None
    #         moved_piece.has_moved = True
    #         self.tiles[z][w].piece = moved_piece
    #         self.update_board_info()
    #         return True
    #     return False
    # # def print_zone_of_control(self):
    # #     letter_line = "    A   B   C   D   E   F   G   H    \n"
    # #     sep_line = "  +---+---+---+---+---+---+---+---+  \n"
    # #     disp = ""  # this variable will be appended until done
    # #     disp = letter_line + disp
    # #     disp = sep_line + disp
    # #     for i in range(8):
    # #         row = sep_line
    # #         row += f"{i + 1}"
    # #         for j in range(8):
    # #             row += " | "
    # #             piece = self.tiles[i][j]
    # #             if True in piece.zoc and False in piece.zoc:
    # #                 zoc_char = "3"
    # #             elif False in piece.zoc:
    # #                 zoc_char = "2"
    # #             elif True in piece.zoc:
    # #                 zoc_char = "1"
    # #             else:
    # #                 zoc_char = "0"
    # #             row += zoc_char
    # #         suffix = f" | {i + 1}\n"
    # #         row += suffix
    # #         disp = row + disp
    # #     disp = letter_line + disp
    # #     return disp
    # #checks whether there are legal moves or not
    # def does_not_have_legal_moves(self, player):
    #     for i in range(8):
    #         for j in range(8):
    #             if self.tiles[i][j].piece and self.tiles[i][j].piece.color == player:
    #                 legal_moves = self.list_legal_tiles((i, j), player)
    #                 if legal_moves:
    #                     return False
    #     return True
    # #function assumes player is castling his own pieces
    # def castle(self, long, player):
    #     kocol = 4
    #     if player:
    #         row = 0
    #     else:
    #         row = 7
    #     if long:
    #         rcol = 0
    #         kdcol = 2
    #         rdcol=3
    #     else:
    #         rcol = 7
    #         kdcol = 6
    #         rdcol = 5
    #     king_tile = self.tiles[row][kocol]
    #     king = king_tile.piece
    #     rook = self.tiles[row][rcol].piece
    #     dest_tile = self.tiles[row][kdcol]
    #     #sanity check
    #     if rook.has_moved or king.has_moved:
    #         return False
    #     rightwards = kdcol-kocol > 0
    #     oneorminusone = -1 + 2*rightwards
    #     #checking for free passage
    #     for i in range(kocol, kdcol+oneorminusone, oneorminusone):
    #         if (i!=kocol and self.tiles[row][i].piece):
    #             return False
    #         if player:
    #             if self.tiles[row][i].in_black_zoc:
    #                 return False
    #         else:
    #             if self.tiles[row][i].in_white_zoc:
    #                 return False
    #     #checks done
    #
    #     self.tiles[row][kocol].piece = None
    #     king.has_moved = True
    #     self.tiles[row][kdcol].piece = king
    #     self.tiles[row][rcol].piece = None
    #     rook.has_moved = True
    #     self.tiles[row][rdcol].piece = rook
    #     self.update_board_info()
    #     return True







