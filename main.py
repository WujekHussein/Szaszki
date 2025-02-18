from game import Game
from chess_board import ChessBoard
from os import path
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
    # game = Game()
    # game.play()
    # board = ChessBoard()
    # board.move((5,0), (7,0))
    # print(board)
    # print(board.player)
    # print(board.legal_moves)
    # print(board.list_legal_coordinates((0,4)))
    pygame.init()
    WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Szaszki")
    running = True
    x=0
    surf = pygame.Surface((100, 100))
    surf.fill("yellow")
    pawn_surface = pygame.image.load(path.join('images', 'pieces', 'white-king.png'))
    it=0.2
    yvals = [random.randint(-20, WINDOW_HEIGHT) for i in range(20)]
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        display_surface.fill('white')

        for i in range(20):
            display_surface.blit(pawn_surface, (x - 15, yvals[i]))
        pygame.display.update()
        x+=it
        if x >= WINDOW_WIDTH - 100 or x <= 0:
            it=-it
    pygame.quit()
if __name__ == '__main__':
    main()