
from chess_board import ChessBoard


def main():
    board = ChessBoard()
    print(board)
    print(board.move((1,4), (3,4)))
    print(board)
    print(board.move((7,6), (5,7)))
    print(board)
    print(board.move((3,4), (4,4)))
    print(board)
    print(board.move((6,3), (4,3)))
    print(board)
    print(board.move((4,4), (5,3)))
    print(board)
    print(board.move((6,2), (5,3)))
    print(board)

if __name__ == '__main__':
    main()