from chess_board import ChessBoard
class Game:
    def __init__(self):
        self.player = True # White player starts
        self.board = ChessBoard()
        self.turn = 1
        self.wcheck = False
        self.bcheck = False
    def play(self):
        #turns will take place for infinite amount of time or will end upon mate or a tie
        while(True):
            print(f"Turn {self.turn}")
            if self.player:
                player_text = "White"
                print(self.board)
                if self.wcheck:
                    print("White is in check")
            else:
                player_text = "Black"
                print(self.board.str_black())
                if self.bcheck:
                    print("Black is in check")
            print(f"{player_text} is on the move")
            #player will provide moves until they are correct or he can surrender by typing s
            while(True):
                proposed_move = input("Provide move: ")
                move = self.string_to_pair_of_pairs(proposed_move)
                if move!=0:
                    origin, destination = move
                    if not (self.board.move(origin, destination, self.player)):
                        print("It's not a legal move")
                    else:
                        break
                else:
                    print("It's not a valid move notationwise.")
            self.wcheck = False
            self.bcheck = False
            self.player = not self.player
            if self.player in self.board.check():
                if self.player:
                    self.wcheck = True
                else:
                    self.bcheck = True
                if self.board.does_not_have_legal_moves(self.player):
                    print(self.board)
                    print(f"Checkmate {player_text} won")
                    break
            elif self.board.does_not_have_legal_moves(self.player):
                print(f"{player_text} has not left his oponent any legal moves but also has not put him in check - a draw")
                break
            if self.player:
                self.turn += 1

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
