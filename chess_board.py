import piece
from tile import Tile
from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King, SupportivePiece
import copy
class ChessBoard:
    def __init__(self):
        self.player = True
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

        self.tiles = tiles
        self.kings_positions = [(0,4), (7,4)]
        self.update_board_info_1()
        self.update_board_info_2()



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

    def get_tile(self, coord):
        x,y = coord
        return self.tiles[x][y]


    #checks in a predefined array
    def is_move_legal(self, origin_coord, destination_coord):
        x, y = origin_coord
        return destination_coord in self.legal_moves[x][y]


    #doesn't care about legality
    def change_position(self, origin_coord, destination_coord):
        moved_piece = self.get_tile(origin_coord).piece
        moved_piece.has_moved = True
        self.get_tile(origin_coord).piece = None
        self.get_tile(destination_coord).piece = moved_piece


    ##
    ##
    ## TRUDNA SPRAWA
    ##
    ##
    def change_position_pawn(self, origin_coord, destination_coord):
        x, y = origin_coord
        z, w = destination_coord
        moved_piece = self.get_tile(origin_coord).piece
        moved_piece.has_moved = True
        ## adding virtual pawn if it is double move
        if y == w and abs(x-z)==2:
            self.tiles[int((x+z)/2)][y].piece = SupportivePiece(moved_piece.player)
        xdestr, ydestr = self.tiles[z][w].destruction_vector()
        #removing virtual (or any other piece or not piece to be exact) pawn upon capture
        self.tiles[xdestr+z][ydestr+w].piece = None
        self.tiles[x][y].piece = None
        self.tiles[z][w].piece = moved_piece



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
        origin_piece = self.get_tile(origin_coord).piece
        if origin_piece:
            possible_vectors = origin_piece.possibly_controlled_tiles()
            for vector in possible_vectors:
                z, w = vector
                newx = x+z
                newy = y+w
                if newx>=0 and newx<8 and newy>=0 and newy<8:
                    possibly_controlled.append((newx, newy))
        return possibly_controlled
    #extends function above with shadowing mechanism
    def list_controlled_coordinates(self, origin_coord):
        controlled = []
        possibly_controlled = self.list_possibly_controlled_coordinates(origin_coord)

        for possibility in possibly_controlled:
            intermediates = self.list_intermediate_coordinates(origin_coord, possibility)
            no_obstacle_flag = True
            #Knight moves don't have intermediates so it will act as jumping over pieces
            for intermediate in intermediates:
                intemediate_tile = self.get_tile(intermediate)
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
                controlling_piece = self.get_tile((i,j)).piece
                if controlling_piece:
                    player = controlling_piece.player
                    controlled_coords = self.list_controlled_coordinates((i,j))
                    for coord in controlled_coords:
                        tile = self.get_tile(coord)
                        tile.zocs[player] = True


    #without player and legal moves
    def update_board_info_1(self):
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
                piece = self.get_tile((i,j)).piece
                if type(piece) == King:
                    self.kings_positions[piece.player] = (i,j)


    # checks if the player on the move is in check
    def check(self):
        king_pos = self.kings_positions[self.player]
        king_tile = self.get_tile(king_pos)
        if king_tile.zocs[not self.player]:
            return True
        return False
    ###
    ###
    ###
    ###CIENSZKI OSZEH
    ###
    ###
    #extends controlled coordinates by not allowing entering controlled tile with our own piece and separate logic for pawn
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

    #deals with dual logic for pawn doesn't need to check for existance of piece at origin_coord
    def apply_move(self, origin_coord, destination_coord):
        if type(self.get_tile(origin_coord).piece) == Pawn:
            self.change_position_pawn(origin_coord, destination_coord)
        else:
            self.change_position(origin_coord, destination_coord)


    ##extends above function byt checking whether position after applying proposed move is valid
    def list_legal_coordinates(self, origin_coord):
        if not self.get_tile(origin_coord).piece or type (self.get_tile(origin_coord).piece) == SupportivePiece or self.get_tile(origin_coord).piece.player != self.player:
            return []
        legals = []
        accessibles = self.list_accessible_coordinates(origin_coord)
        for accessible in accessibles:
            board_copy = copy.deepcopy(self)
            board_copy.apply_move(origin_coord, accessible)
            board_copy.update_board_info_1()
            if not board_copy.check():
                legals.append(accessible)
        return legals



    def update_legal_moves(self):
        for i in range(8):
            for j in range(8):
                    self.legal_moves[i][j] = self.list_legal_coordinates((i,j))




    #checks if proposed castling is possible
    def if_castle(self, short):
        if self.check():
            return False
        x, y = self.kings_positions[self.player]
        if type(self.tiles[x][y].piece) != King or self.tiles[x][y].piece.player != self.player or self.tiles[x][y].piece.has_moved:
            return False
        if type(self.tiles[x][short*7].piece) != Rook or self.tiles[x][short*7].piece.player != self.player or self.tiles[x][short*7].piece.has_moved:
            return False
        y+= -(-1)**short
        if self.tiles[x][y].piece or self.tiles[x][y].zocs[not self.player]:
            return False
        y+= -(-1)**short
        if self.tiles[x][y].piece or self.tiles[x][y].zocs[not self.player]:
            return False
        return True



    def apply_castle(self, short):
        xk = self.player*7
        yk=4
        king = self.tiles[xk][yk].piece
        king.has_moved = True
        yr = short*7
        rook = self.tiles[xk][yr].piece
        rook.has_moved = True
        newyk = yk - 2*(-1)**short
        newyr = newyk + (-1)**short
        self.tiles[xk][yk].piece = None
        self.tiles[xk][yr].piece = None
        self.tiles[xk][newyk].piece = king
        self.tiles[xk][newyr].piece = rook



    def update_board_info_2(self):
        self.player = not self.player
        self.update_legal_moves()



    def does_not_have_legal_moves(self):
        for i in range(8):
            for j in range(8):
                if self.legal_moves[i][j] != []:
                    return False
        return True
    # tries to apply proposed move returns True and changes the board accordingly if successful, returns False otherwise
    def move(self, coord_origin, coord_destination):
        #separate logic for castling
        if self.if_castle(False):
            if coord_origin == (7*int(self.player), 4) and coord_destination == (7*int(self.player), 2):
                self.apply_castle(False)
                self.update_board_info_1()
                self.update_board_info_2()
                return True
        if self.if_castle(True):
            if coord_origin == (7*int(self.player), 4) and coord_destination == (7*int(self.player), 6):
                self.apply_castle(True)
                self.update_board_info_1()
                self.update_board_info_2()
                return True
        x, y = coord_origin
        if coord_destination in self.legal_moves[x][y]:
            self.apply_move(coord_origin, coord_destination)
            self.update_board_info_1()
            self.update_board_info_2()
            return True
        return False









