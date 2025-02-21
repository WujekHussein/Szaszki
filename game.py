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
        self.chosen_tile = None
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

        #possible tile surface
        red_circle = pygame.image.load(join('images', 'other', 'Red-Circle-Transparent.png'))
        red_circle = pygame.transform.scale(red_circle, (TILE_SIZE*0.75, TILE_SIZE*0.75))

        BOARD_COARDX = 5 / 16 * WINDOW_WIDTH
        BOARD_COARDY = 1 / 6 * WINDOW_HEIGHT

        # tile_buttons = []
        markings = []
        tile_buttons = [[TileButton(BOARD_COARDX + j * TILE_SIZE, BOARD_COARDY + i * TILE_SIZE, TILE_SIZE, TILE_SIZE,
                                    "", font, self.tileButtonAction, (7 - i, j), 0,
                                    "beige" if (i + j) % 2 == 0 else (62, 29, 35)) for j in range(8)] for i in range(8)]
        for i in range(8):
        #     # TILES
        #         tile_coords_x = BOARD_COARDX + j * TILE_SIZE
        #         tile_coords_y = BOARD_COARDY + i * TILE_SIZE
        #         ##displaying tile itself
        #         tile = TileButton(tile_coords_x, tile_coords_y, TILE_SIZE, TILE_SIZE, "", font, self.tileButtonAction, (7-i, j), 0,
        #                           "beige" if (i + j) % 2 == 0 else (62, 29, 35))
        #         tile.draw(display_surface)
        #         tile_buttons.append(tile)



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
        tile_buttons_list = [tile for row in tile_buttons for tile in row]
        buttons = tile_buttons_list + [ng_button]
        player_mark_surf = font.render("Player:", True, "black")
        player_mark_rect = player_mark_surf.get_rect(center = (13/16*WINDOW_WIDTH, 7/18*WINDOW_HEIGHT))
        CHECK = False
        #will be checked for having correct length
        while (running):
        #Setting_up activity
            if len(self.input_str) == 0:
                for i in range(8):
                    for j in range(8):
                        button = tile_buttons[i][j]
                        x, y = button.board_coords
                        if self.board.legal_moves[x][y]:
                            button.is_active = True
                        else:
                            button.is_active = False
            else:
                y = ord(self.input_str[0]) - 97
                x = ord(self.input_str[1]) - 49
                possible_moves = self.board.legal_moves[x][y]
                for move in possible_moves:
                    i, j = move
                    tile_buttons[7-i][j].is_active = True

            # for i in range(8):
            #     for j in range(8):
            #         button = tile_buttons[i][j]
            #         x, y = button.board_coords
            #         if  not self.board.legal_moves[x][y] and not button in moveable_onto_tiles :
            #             button.is_active = False
            # for tile in moveable_onto_tiles:
            #     tile.is_active = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for button in buttons:
                    if button.check_pushdown(event) and button.is_active:
                        self.pressed_button = button
                    if button.check_release(event):
                        if button == self.pressed_button:
                            button.act()
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





            display_surface.fill('white')

            for button in buttons:
                button.draw(display_surface)

            #CURSOR STYLE CHANGE
            hovering = False
            for button in buttons:
                if button.is_hovered() and button.is_active:
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

            if len(self.input_str) == 2:
                self.highlight_possible_moves(display_surface, red_circle)




            #INFO

            #player on the move
            display_surface.blit(player_mark_surf, player_mark_rect.topleft)
            outer_on_the_move_rect = pygame.Rect(0,0, int(1/9*WINDOW_HEIGHT)+10, int(1/9*WINDOW_HEIGHT)+10)
            outer_on_the_move_rect.center = (15/16*WINDOW_WIDTH, 7/18*WINDOW_HEIGHT)
            inner_on_the_move_rect = pygame.Rect(0,0, int(1/9*WINDOW_HEIGHT), int(1/9*WINDOW_HEIGHT))
            inner_on_the_move_rect.center = (15 / 16 * WINDOW_WIDTH, 7 / 18 * WINDOW_HEIGHT)
            pygame.draw.rect(display_surface, "black", outer_on_the_move_rect)
            player_color = "black" if self.player else "white"
            pygame.draw.rect(display_surface, player_color, inner_on_the_move_rect)

            #current turn
            turn_surf = font.render(f"Turn {self.turn}", True, "black")
            turn_rect = player_mark_surf.get_rect(center=(13 / 16 * WINDOW_WIDTH, 4 / 18 * WINDOW_HEIGHT))
            display_surface.blit(turn_surf, turn_rect.topleft)

            player_str = "Black" if self.player else "White"
            not_player_str = "White" if self.player else "Black"

            #check
            if CHECK:
                check_surf = font.render(f"{player_str} is in check", True, "black")
                check_rect = check_surf.get_rect(center=(14/16*WINDOW_WIDTH, 10/18*WINDOW_HEIGHT))
                display_surface.blit(check_surf, check_rect.topleft)

            #mate and draw announcements
            if self.mate or self.draw:
                text = f"{player_str} has no legal moves\n but is not in check - draw" if self.draw else f"Checkmate - {not_player_str} won"
                end_info_surf = font.render(text, True, "black")
                end_info_rect = end_info_surf.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
                outer_bg_rect = end_info_rect.inflate(60,60)
                bg_rect = end_info_rect.inflate(50, 50)
                pygame.draw.rect(display_surface, "black", outer_bg_rect)
                pygame.draw.rect(display_surface, "white", bg_rect)
                display_surface.blit(end_info_surf, end_info_rect.topleft)

            pygame.display.update()
    pygame.quit()


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

    def board_coords_to_display_coords(self, x, y, width, height):
        return (5/16*width + 1/12*height*(y+1/2), 1/6*height + 1/12*height*(7-x+1/2))
    def highlight_possible_moves(self, display, marking):
        if len(self.input_str) == 2:
            y = ord(self.input_str[0])-97
            x = ord(self.input_str[1])-49
            possible_moves = self.board.legal_moves[x][y]
            if not possible_moves:
                return False
            width, height = display.get_size()
            for move in possible_moves:
                z, w = move
                display_coords = self.board_coords_to_display_coords(z, w, width, height)
                display.blit(marking, marking.get_rect(center=display_coords))
        return True

