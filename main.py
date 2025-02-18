from game import Game
from chess_board import ChessBoard
from os.path import join
import pygame
import random

def main():
    # board = ChessBoard()
    # print(board)
    # print(board.move((0,4),(0,2)))
    # print(board)
    # print(board.if_castle(False))
    # print(board.move((7,4), (7,2)))
    # print(board)
    # # print(board.move((1,4),(3,4)))
    # # print(board)
    # # print(board)
    game = Game()
    board = game.board
    # game.play()
    # board = ChessBoard()
    # board.move((5,0), (7,0))
    # print(board)
    # print(board.player)
    # print(board.legal_moves)
    # print(board.list_legal_coordinates((0,4)))

    ## OKNO
    pygame.init()
    ##Ważne stałe
    WINDOW_WIDTH, WINDOW_HEIGHT = 2560, 1440
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    TILE_SIZE = WINDOW_HEIGHT / 10
    pygame.display.set_caption("Szaszki")
    running = True
    #PIECES SURFACES
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
    piece_surfaces = [[None, white_pawn, white_rook, white_knight, white_bishop, white_queen, white_king],[None, black_pawn, black_rook, black_knight, black_bishop, black_queen, black_king]]
    for i in range(2):
        for j in range(7):
            if piece_surfaces[i][j]:
                piece_surfaces[i][j] = pygame.transform.scale(piece_surfaces[i][j], (TILE_SIZE, TILE_SIZE))
    white_tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    white_tile.fill("beige")
    dark_tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    dark_tile.fill((62,29,35))
    tiles = [white_tile, dark_tile]
    board_cordx = (WINDOW_WIDTH-0.8*WINDOW_HEIGHT)/2
    board_cordy = WINDOW_HEIGHT/10
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        display_surface.fill('white')

        for i in range(8):
            for j in range(8):
                display_coords = (board_cordx+i*TILE_SIZE, board_cordy+j*TILE_SIZE)
                ##displaying tile itself
                display_surface.blit(tiles[(i+j)%2], display_coords)
                ##displaying piece
                display_color, display_piece = board.tiles[7-j][i].get_display_info()
                if display_piece != 0:
                    display_surface.blit(piece_surfaces[display_color][display_piece], display_coords)
        pygame.display.update()
    pygame.quit()
if __name__ == '__main__':
    main()