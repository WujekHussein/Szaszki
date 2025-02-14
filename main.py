
from chess_board import ChessBoard


def main():
    board = ChessBoard()
    print(board)
    print(board.list_accessible_coordinates((0,1)))
if __name__ == '__main__':
    main()