from game import Game
from chess_board import ChessBoard
from tile import Tile
from piece import Piece, Knight


def main():

    # board = ChessBoard()
    # print(board)
    # print(board.move((0,3), (7,3), True))
    # print(board)
    # print(board.move((7,4), (7,3), False))
    # print(board)
    game = Game()
    game.play()
if __name__ == '__main__':
    main()