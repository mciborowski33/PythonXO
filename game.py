import os
import time
import random

#plansza
from pip._vendor.distlib.compat import raw_input

board = ["", " ", " ", " ", " ", " ", " ", " ", " ", " "]

def print_header():
    print("""
    1|2|3
    4|5|6
    7|8|9
    """)
#Funkcja rysujaca tablice
def print_board():
    print("   |   |   ")
    print(" "+board[1]+" | "+board[2]+" | "+board[3]+" ")
    print("---|---|---")
    print(" " + board[4] + " | " + board[5] + " | " + board[6] + " ")
    print("---|---|---")
    print(" " + board[7] + " | " + board[8] + " | " + board[9] + " ")
    print("   |   |   ")


def is_winner(board, player):
    if (board[1] == player and board[2] == player and board[3] == player) or \
        (board[4] == player and board[5] == player and board[6] == player) or \
        (board[7] == player and board[8] == player and board[9] == player) or \
        (board[1] == player and board[4] == player and board[7] == player) or \
        (board[2] == player and board[5] == player and board[8] == player) or \
        (board[3] == player and board[6] == player and board[9] == player) or \
        (board[1] == player and board[5] == player and board[9] == player) or \
        (board[3] == player and board[5] == player and board[7] == player):
        return True
    else:
        return False


def is_board_full(board):
    if " " in board:
        return False
    else:
        return True


while True:
    os.system("cls")
    print_header()
    print_board()

#   Gracz X
    choice = raw_input("Wybierz puste miejsce na X ")
    choice = int(choice)

#   sprawdzenie czy miejsce jest puste
    while board[choice] != " ":
        print("To miejsce jest już zajęte")
        choice = raw_input("Wybierz inne miejsce na X ")
        choice = int(choice)

    if board[choice] == " ":
        board[choice] = "X"


#   sprawdzanie wygranej
    if is_winner(board, "X"):
        os.system("cls")
        print_header()
        print_board()
        print("X wygrał! Gratulacje!")
        time.sleep(2)
        break

    os.system("cls")
    print_header()
    print_board()

# Akcja gdy tablica jest pełna
    if is_board_full(board):
        print("REMIS!")
        time.sleep(2)
        break

#   Gracz O
    choice = raw_input("Wybierz puste miejsce na O ")
    choice = int(choice)

    #   sprawdzenie czy miejsce jest puste
    while board[choice] != " ":
        print("To miejsce jest już zajęte")
        choice = raw_input("Wybierz inne miejsce na O ")
        choice = int(choice)

    if board[choice] == " ":
        board[choice] = "O"

#   sprawdzanie wygranej
    if is_winner(board, "O"):
        os.system("cls")
        print_header()
        print_board()
        print("O wygrał! Gratulacje!")
        time.sleep(2)
        break

    os.system("cls")
    print_header()
    print_board()

# Akcja gdy tablica jest pełna
    if is_board_full(board):
        print("REMIS!")
        time.sleep(2)
        break
