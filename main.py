from game import Game
from chess_board import ChessBoard
from os.path import join
import pygame

def main():
    game = Game()
    game.play()
    # board = game.board

    # ## OKNO
    # pygame.init()
    # ##Ważne stałe
    # WINDOW_WIDTH = 1920
    # WINDOW_HEIGHT = 9/16*WINDOW_WIDTH
    # display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # TILE_SIZE = WINDOW_HEIGHT / 12
    # pygame.display.set_caption("Szaszki")
    # font = pygame.font.Font(None, int(0.75*TILE_SIZE))
    #
    # running = True
    # #PIECES SURFACES
    # white_pawn = pygame.image.load(join('images', 'pieces', 'white-pawn.png'))
    # black_pawn = pygame.image.load(join('images', 'pieces', 'black-pawn.png'))
    # white_rook = pygame.image.load(join('images', 'pieces', 'white-rook.png'))
    # black_rook = pygame.image.load(join('images', 'pieces', 'black-rook.png'))
    # white_knight = pygame.image.load(join('images', 'pieces', 'white-knight.png'))
    # black_knight = pygame.image.load(join('images', 'pieces', 'black-knight.png'))
    # white_bishop = pygame.image.load(join('images', 'pieces', 'white-bishop.png'))
    # black_bishop = pygame.image.load(join('images', 'pieces', 'black-bishop.png'))
    # white_queen = pygame.image.load(join('images', 'pieces', 'white-queen.png'))
    # black_queen = pygame.image.load(join('images', 'pieces', 'black-queen.png'))
    # white_king = pygame.image.load(join('images', 'pieces', 'white-king.png'))
    # black_king = pygame.image.load(join('images', 'pieces', 'black-king.png'))
    # piece_surfaces = [[None, white_pawn, white_rook, white_knight, white_bishop, white_queen, white_king],[None, black_pawn, black_rook, black_knight, black_bishop, black_queen, black_king]]
    # for i in range(2):
    #     for j in range(7):
    #         if piece_surfaces[i][j]:
    #             piece_surfaces[i][j] = pygame.transform.scale(piece_surfaces[i][j], (TILE_SIZE, TILE_SIZE))
    # white_tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    # white_tile.fill("beige")
    # dark_tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    # dark_tile.fill((62,29,35))
    # tiles = [white_tile, dark_tile]
    # board_cordx = 5/16*WINDOW_WIDTH
    # board_cordy = 1/6*WINDOW_HEIGHT
    # while(running):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             if event.button == 1:
    #                 mouse_x, mouse_y = event.pos
    #
    #     display_surface.fill('white')
    #
    #     for i in range(8):
    #         #TILES
    #         for j in range(8):
    #             display_coords = (board_cordx+i*TILE_SIZE, board_cordy+j*TILE_SIZE)
    #             ##displaying tile itself
    #             display_surface.blit(tiles[(i+j)%2], display_coords)
    #             ##displaying piece
    #             display_color, display_piece = board.tiles[7-j][i].get_display_info()
    #             if display_piece != 0:
    #                 display_surface.blit(piece_surfaces[display_color][display_piece], display_coords)
    #         #COORDINATE MARKINGS
    #         #top letters
    #         text_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    #         text_rendered = font.render(chr(i+65), True, "black")
    #         text_rect = text_rendered.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2))
    #         text_surface.blit(text_rendered, text_rect)
    #         display_surface.blit(text_surface, (board_cordx + TILE_SIZE*i, board_cordy - TILE_SIZE))
    #         #bottop letters
    #         text_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    #         text_rendered = font.render(chr(i + 65), True, "black")
    #         text_rect = text_rendered.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2))
    #         text_surface.blit(text_rendered, text_rect)
    #         display_surface.blit(text_surface, (board_cordx + TILE_SIZE * i, board_cordy + 8 *TILE_SIZE))
    #         #left numbers
    #         text_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    #         text_rendered = font.render(chr(i + 49), True, "black")
    #         text_rect = text_rendered.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2))
    #         text_surface.blit(text_rendered, text_rect)
    #         display_surface.blit(text_surface, (board_cordx - TILE_SIZE, board_cordy + (7-i) * TILE_SIZE))
    #         #right numbers
    #         text_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    #         text_rendered = font.render(chr(i + 49), True, "black")
    #         text_rect = text_rendered.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2))
    #         text_surface.blit(text_rendered, text_rect)
    #         display_surface.blit(text_surface, (board_cordx + 8 * TILE_SIZE, board_cordy + (7 - i) * TILE_SIZE))
    #
    #
    #
    #     pygame.display.update()
    # pygame.quit()
if __name__ == '__main__':
    main()