import os
import time
import random

# plansza
from pip._vendor.distlib.compat import raw_input

board = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]


class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board_content = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.header = """
                1|2|3
                4|5|6
                7|8|9
                """

    def start(self):
        # info o tym że mamy kogoś dla nich :o
        self.player1.send_match_info()
        self.player2.send_match_info()

        while True:
            # Player 1 move
            if self.move(self.player1, self.player2):
                return
            # Player 2 move
            if self.move(self.player2, self.player1):
                return

    def move(self, moving_player, waiting_player):
        moving_player.send("B", ("".join(self.board_content)))
        moving_player.send("H", ("".join(self.header)))
        waiting_player.send("B", ("".join(self.board_content)))
        waiting_player.send("H", ("".join(self.header)))
        # # Let the moving player move, Y stands for yes it's turn to move,
        # # and N stands for no and waiting
        moving_player.send("C", "Y")
        waiting_player.send("C", "N")
        # # Receive the move from the moving player
        move = int(moving_player.recv(2, "i"))
        # # Send the move to the waiting player
        waiting_player.send("I", str(move))
        # # Check if the position is empty
        if self.board_content[move - 1] == " ":
            # Write the it into the board
            self.board_content[move - 1] = moving_player.role
        else:
            print("hehe")
            # logging.warning("Player " + str(moving_player.id) +
            #                 " is attempting to take a position that's already " +
            #                 "been taken.");
            # This player is attempting to take a position that's already
            # taken. HE IS CHEATING, KILL HIM!
            # moving_player.send("Q", "Please don't cheat!\n" +
            #                    "You are running a modified client program.")
            # waiting_player.send("Q", "The other playing is caught" +
            #                     "cheating. You win!")
            # # Throw an error to finish this game
            # raise Exception
        #
        # # Check if this will result in a win
        result, winning_path = self.check_winner(moving_player)
        if result >= 0:
            # If there is a result
            # Send back the latest board content
            moving_player.send("B", ("".join(self.board_content)))
            waiting_player.send("B", ("".join(self.board_content)))

            if result == 0:
                # If this game ends with a draw
                # Send the players the result
                moving_player.send("C", "D")
                waiting_player.send("C", "D")
                print("Game between player " + str(self.player1.id) + " and player "
                      + str(self.player2.id) + " ends with a draw.")
                return True
            if result == 1:
                # If this player wins the game
                # Send the players the result
                moving_player.send("C", "W")
                waiting_player.send("C", "L")
                # Send the players the winning path
                moving_player.send("P", winning_path)
                waiting_player.send("P", winning_path)
                print("Player " + str(self.player1.id) + " beats player "
                      + str(self.player2.id) + " and finishes the game.")
                return True
            return False

    def print_header(self):
        self.header = """
        1|2|3
        4|5|6
        7|8|9
        """

    # Funkcja rysujaca tablice
    def print_board(self):
        print("   |   |   ")
        print(" " + board[1] + " | " + board[2] + " | " + board[3] + " ")
        print("---|---|---")
        print(" " + board[4] + " | " + board[5] + " | " + board[6] + " ")
        print("---|---|---")
        print(" " + board[7] + " | " + board[8] + " | " + board[9] + " ")
        print("   |   |   ")

    # def is_winner(self, board, player):
    #     if (board[1] == player and board[2] == player and board[3] == player) or \
    #             (board[4] == player and board[5] == player and board[6] == player) or \
    #             (board[7] == player and board[8] == player and board[9] == player) or \
    #             (board[1] == player and board[4] == player and board[7] == player) or \
    #             (board[2] == player and board[5] == player and board[8] == player) or \
    #             (board[3] == player and board[6] == player and board[9] == player) or \
    #             (board[1] == player and board[5] == player and board[9] == player) or \
    #             (board[3] == player and board[5] == player and board[7] == player):
    #         return True
    #     else:
    #         return False

    def check_winner(self, player):
        """Checks if the player wins the game. Returns 1 if wins,
        0 if it's a draw, -1 if there's no result yet."""
        s = self.board_content

        # Check columns
        if len({s[0], s[1], s[2], player.role}) == 1:
            return 1, "012"
        if len({s[3], s[4], s[5], player.role}) == 1:
            return 1, "345"
        if len({s[6], s[7], s[8], player.role}) == 1:
            return 1, "678"

        # Check rows
        if len({s[0], s[3], s[6], player.role}) == 1:
            return 1, "036"
        if len({s[1], s[4], s[7], player.role}) == 1:
            return 1, "147"
        if len({s[2], s[5], s[8], player.role}) == 1:
            return 1, "258"

        # Check diagonal
        if len({s[0], s[4], s[8], player.role}) == 1:
            return 1, "048"
        if len({s[2], s[4], s[6], player.role}) == 1:
            return 1, "246"

        # If there's no empty position left, draw
        if " " not in s:
            return 0, ""

        # The result cannot be determined yet
        return -1, ""

    def is_board_full(self, board):
        if " " in board:
            return False
        else:
            return True

# def main():
#     while True:
#
#         game = Game()
#         os.system("cls")
#         game.print_header()
#         game.print_board()
#
#     #   Gracz X
#         choice = raw_input("Wybierz puste miejsce na X ")
#         choice = int(choice)
#
#     #   sprawdzenie czy miejsce jest puste
#         while board[choice] != " ":
#             print("To miejsce jest już zajęte")
#             choice = raw_input("Wybierz inne miejsce na X ")
#             choice = int(choice)
#
#         if board[choice] == " ":
#             board[choice] = "X"
#
#
#     #   sprawdzanie wygranej
#         if game.is_winner(board, "X"):
#             os.system("cls")
#             game.print_header()
#             game.print_board()
#             print("X wygrał! Gratulacje!")
#             time.sleep(2)
#             break
#
#         os.system("cls")
#         game.print_header()
#         game.print_board()
#
#     # Akcja gdy tablica jest pełna
#         if game.is_board_full(board):
#             print("REMIS!")
#             time.sleep(2)
#             break
#
#     #   Gracz O
#         choice = raw_input("Wybierz puste miejsce na O ")
#         choice = int(choice)
#
#         #   sprawdzenie czy miejsce jest puste
#         while board[choice] != " ":
#             print("To miejsce jest już zajęte")
#             choice = raw_input("Wybierz inne miejsce na O ")
#             choice = int(choice)
#
#         if board[choice] == " ":
#             board[choice] = "O"
#
#     #   sprawdzanie wygranej
#         if game.is_winner(board, "O"):
#             os.system("cls")
#             game.print_header()
#             game.print_board()
#             print("O wygrał! Gratulacje!")
#             time.sleep(2)
#             break
#
#         os.system("cls")
#         game.print_header()
#         game.print_board()
#
#     # Akcja gdy tablica jest pełna
#         if game.is_board_full(board):
#             print("REMIS!")
#             time.sleep(2)
#             break
# main()
