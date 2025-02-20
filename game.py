from chess_board import ChessBoard
from os.path import join
import pygame
from button import Button, TileButton

class Game:
    def __init__(self):
        self.player = False # White player starts
        self.board = ChessBoard()
        self.turn = 1
        self.pressed_button = None
        self.input_str =""
        self.mate = False
        self.draw = False
    def tileButtonAction(self, button):
        self.input_str = self.input_str + button.__str__()
    def newGameButtonAction(self, button):
        self.board = ChessBoard()
        self.turn = 1
        self.player = False
        self.input_str = ""
        self.mate = False
        self.draw = False
    def play(self):

        ## OKNO
        pygame.init()
        ##Ważne stałe
        WINDOW_WIDTH = 1920
        WINDOW_HEIGHT = 9 / 16 * WINDOW_WIDTH
        display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        TILE_SIZE = WINDOW_HEIGHT / 12
        LEFT_BUTTON_WIDTH = 3/16 * WINDOW_WIDTH
        LEFT_BUTTON_HEIGHT = WINDOW_HEIGHT / 6
        pygame.display.set_caption("Szaszki")
        font = pygame.font.Font(None, int(0.75 * TILE_SIZE))

        running = True
        # PIECES SURFACES
        white_pawn = pygame.image.load(join('images', 'pieces', 'white-pawn.png'))
        black_pawn = pygame.image.load(join('images', 'pieces', 'black-pawn.png'))
        white_rook = pygame.image.load(join('images', 'pieces', 'white-rook.png'))
        black_rook = pygame.image.load(join('images', 'pieces', 'black-rook.png'))
        white_knight = pygame.image.load(join('images', 'pieces', 'white-knight.png'))
        black_knight = pygame.image.load(join('images', 'pieces', 'black-knight.png'))
        white_bishop = pygame.image.load(join('images', 'pieces', 'white-bishop.png'))
        black_bishop = pygame.image.load(join('images', 'pieces', 'black-bishop.png'))
        white_queen = pygame.image.load(join('images', 'pieces', 'white-queen.png'))
        black_queen = pygame.image.load(join('images', 'pieces', 'black-queen.png'))
        white_king = pygame.image.load(join('images', 'pieces', 'white-king.png'))
        black_king = pygame.image.load(join('images', 'pieces', 'black-king.png'))
        piece_surfaces = [[None, white_pawn, white_rook, white_knight, white_bishop, white_queen, white_king],
                          [None, black_pawn, black_rook, black_knight, black_bishop, black_queen, black_king]]
        for i in range(2):
            for j in range(7):
                if piece_surfaces[i][j]:
                    piece_surfaces[i][j] = pygame.transform.scale(piece_surfaces[i][j], (TILE_SIZE, TILE_SIZE))


        BOARD_COARDX = 5 / 16 * WINDOW_WIDTH
        BOARD_COARDY = 1 / 6 * WINDOW_HEIGHT

        buttons = []
        markings = []
        for i in range(8):
            # TILES
            for j in range(8):
                tile_coords_x = BOARD_COARDX + j * TILE_SIZE
                tile_coords_y = BOARD_COARDY + i * TILE_SIZE
                ##displaying tile itself
                tile = TileButton(tile_coords_x, tile_coords_y, TILE_SIZE, TILE_SIZE, "", font, self.tileButtonAction, (7-i, j), 0,
                                  "beige" if (i + j) % 2 == 0 else (62, 29, 35))
                tile.draw(display_surface)
                buttons.append(tile)
            # COORDINATE MARKINGS
            # top letters
            text_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            text_rendered = font.render(chr(i + 65), True, "black")
            text_rect = text_rendered.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2))
            text_surface.blit(text_rendered, text_rect)
            markings.append((text_surface, (BOARD_COARDX + TILE_SIZE * i, BOARD_COARDY - TILE_SIZE) ))
            # bottop letters
            text_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            text_rendered = font.render(chr(i + 65), True, "black")
            text_rect = text_rendered.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2))
            text_surface.blit(text_rendered, text_rect)
            markings.append((text_surface, (BOARD_COARDX + TILE_SIZE * i, BOARD_COARDY + 8 * TILE_SIZE)))
            # left numbers
            text_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            text_rendered = font.render(chr(i + 49), True, "black")
            text_rect = text_rendered.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2))
            text_surface.blit(text_rendered, text_rect)
            markings.append((text_surface, (BOARD_COARDX - TILE_SIZE, BOARD_COARDY + (7 - i) * TILE_SIZE)))
            # right numbers
            text_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            text_rendered = font.render(chr(i + 49), True, "black")
            text_rect = text_rendered.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2))
            text_surface.blit(text_rendered, text_rect)
            markings.append((text_surface, (BOARD_COARDX + 8 * TILE_SIZE, BOARD_COARDY + (7 - i) * TILE_SIZE)))


        ng_button = Button(WINDOW_WIDTH // 16, WINDOW_HEIGHT // 6, LEFT_BUTTON_WIDTH, LEFT_BUTTON_HEIGHT, "New Game",
                           font, self.newGameButtonAction, WINDOW_WIDTH // 480)
        ng_button.draw(display_surface)
        buttons.append(ng_button)

        player_mark_surf = font.render("Player:", True, "black")
        player_mark_rect = player_mark_surf.get_rect(center = (13/16*WINDOW_WIDTH, 7/18*WINDOW_HEIGHT))

        CHECK = False
        #will be checked for having correct length
        while (running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for button in buttons:
                    if button.check_pushdown(event):
                        self.pressed_button = button
                    if button.check_release(event):
                        if button == self.pressed_button:
                            button.act()
                            print(self.input_str)
                        else:
                            self.pressed_button = None
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     if event.button == 1:
                #         for button in buttons:
                #             if type(button) == TileButton and button.is_hovered() and button.is_active():
                #                 self.pressed_button = button
                # elif event.type == pygame.MOUSEBUTTONUP:
                #     if event.button == 1 and self.pressed_button:
                #         for button in buttons:
                #             if type(button) == TileButton and button.is_hovered() and button.is_active():
                #                 if button == self.pressed_button:
                #                     INPUT_STR = INPUT_STR + self.pressed_button.__str__()
                #                     if len(INPUT_STR) == 4:
                #                         coord_origin, coord_destination = self.string_to_pair_of_pairs(INPUT_STR)
                #                         if self.board.move(coord_origin, coord_destination):
                #                             self.player = not self.player
                #                         INPUT_STR = ""
                #         self.pressed_button = None


            HIGHLIGHT_POSSIBLE_MOVES = False
            ##LOGIC
            if len(self.input_str) == 4:
                coord_origin, coord_destination = self.string_to_pair_of_pairs(self.input_str)
                if self.board.move(coord_origin, coord_destination):
                    if self.player:
                        self.turn+=1
                    self.player = not self.player
                    CHECK = self.board.check()
                    self.mate = self.board.mate()
                    self.draw = self.board.draw()
                    if self.mate:
                        print("MAT SKURWYSYNU")
                self.input_str = ""
            elif len(self.input_str) == 2:
                HIGHLIGHT_POSSIBLE_MOVES = True




            display_surface.fill('white')

            for button in buttons:
                button.draw(display_surface)
            hovering = False
            for button in buttons:
                if button.is_hovered() and button.is_active():
                    hovering = True
                    break
            if hovering:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            for marking in markings:
                surf, coords = marking
                display_surface.blit(surf, coords)


            for i in range(8):
                # TILES
                for j in range(8):
                    tile_coords_x = BOARD_COARDX + i * TILE_SIZE
                    tile_coords_y = BOARD_COARDY + j * TILE_SIZE
                    ##displaying piece
                    display_color, display_piece = self.board.tiles[7 - j][i].get_display_info()
                    if display_piece != 0:
                        display_surface.blit(piece_surfaces[display_color][display_piece], (tile_coords_x, tile_coords_y))





            #INFO
            display_surface.blit(player_mark_surf, player_mark_rect.topleft)

            outer_on_the_move_rect = pygame.Rect(0,0, int(1/9*WINDOW_HEIGHT)+10, int(1/9*WINDOW_HEIGHT)+10)
            outer_on_the_move_rect.center = (15/16*WINDOW_WIDTH, 7/18*WINDOW_HEIGHT)
            inner_on_the_move_rect = pygame.Rect(0,0, int(1/9*WINDOW_HEIGHT), int(1/9*WINDOW_HEIGHT))
            inner_on_the_move_rect.center = (15 / 16 * WINDOW_WIDTH, 7 / 18 * WINDOW_HEIGHT)
            pygame.draw.rect(display_surface, "black", outer_on_the_move_rect)
            player_color = "black" if self.player else "white"
            pygame.draw.rect(display_surface, player_color, inner_on_the_move_rect)

            turn_surf = font.render(f"Turn {self.turn}", True, "black")
            turn_rect = player_mark_surf.get_rect(center=(13 / 16 * WINDOW_WIDTH, 4 / 18 * WINDOW_HEIGHT))
            display_surface.blit(turn_surf, turn_rect.topleft)

            player_str = "Black" if self.player else "White"
            not_player_str = "White" if self.player else "Black"

            if CHECK:
                check_surf = font.render(f"{player_str} is in check", True, "black")
                check_rect = check_surf.get_rect(center=(14/16*WINDOW_WIDTH, 10/18*WINDOW_HEIGHT))
                display_surface.blit(check_surf, check_rect.topleft)

            if self.mate or self.draw:
                text = f"{self.player} has no legal moves\n but is not in check - draw" if self.draw else f"Checkmate - {not_player_str} won"
                end_info_surf = font.render(text, True, "black")
                end_info_rect = end_info_surf.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
                outer_bg_rect = end_info_rect.inflate(60,60)
                bg_rect = end_info_rect.inflate(50, 50)
                pygame.draw.rect(display_surface, "black", outer_bg_rect)
                pygame.draw.rect(display_surface, "white", bg_rect)
                display_surface.blit(end_info_surf, end_info_rect.topleft)

            pygame.display.update()
    pygame.quit()

        #turns will take place for infinite amount of time or will end upon mate or a tie
        # while(True):
        #     print(f"Turn {self.turn}")
        #     print(f"{self.player_text(self.player)} is on the move")
        #     print(self.board)
        #     #player will provide moves until they are correct or he can surrender by typing s
        #     while(True):
        #         proposed_move = input("Provide move: ")
        #
        #         move = self.string_to_pair_of_pairs(proposed_move)
        #         if move!=0:
        #             origin, destination = move
        #             if not (self.board.move(origin, destination)):
        #                 print("It's not a legal move")
        #             else:
        #                 break
        #         else:
        #             print("It's not a valid move notationwise.")
        #
        #     if self.board.check():
        #         if self.board.does_not_have_legal_moves():
        #             print(self.board)
        #             print(f"Checkmate {self.player_text(self.player)} won")
        #             break
        #         print(f"{self.player_text(not self.player)} is in check")
        #     elif self.board.does_not_have_legal_moves():
        #         print(f"{self.player_text(self.player)} has not left {self.player_text(not self.player)} any legal moves but also has not put him in check - a draw")
        #         break
        #     self.player = not self.player
        #
        #     if not self.player:
        #         self.turn += 1

    def string_to_pair_of_pairs(self, text):
        if (len(text) != 4):
            return 0
        y1 = ord(text[0])-97
        x1 = ord(text[1])-49
        y2 = ord(text[2])-97
        x2 = ord(text[3])-49
        if x1<0 or x1>7 or y1<0 or y1>7 or x2<0 or x2>7 or y2<0 or y2>7:
            return 0
        else:
            return ((x1,y1),(x2,y2))
    def controls(self):
        text = ("moves are input using {letter}{number}{letter}{number} format,\n first is the tile from which move is taking place and after it destination tile\n"
                "you can also surrender by typing 's'")
        return text
    def player_text(self, player):
        if player:
            return "Black"
        else:
            return "White"
    def chessboard_coord_to_window_coords(self, i, j):
        pass