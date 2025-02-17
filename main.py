from game import Game
from chess_board import ChessBoard


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
    game.play()
if __name__ == '__main__':
    main()