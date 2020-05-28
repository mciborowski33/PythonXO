import socket
from sys import argv


class Client:

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.board = ["", " ", " ", " ", " ", " ", " ", " ", " ", " "]

    def connect(self, server_address):
        while True:
            try:
                print("Connecting to the game server..")
                self.client_socket.connect(server_address)
                return True
            except:
                print("A problem occured...try again")
                exit()
            return False

    def close(self):
        # Shut down the socket to prevent further sends/receives
        self.client_socket.shutdown(socket.SHUT_RDWR)
        # Close the socket
        self.client_socket.close()

    def s_send(self, command_type, msg):
        try:
            self.client_socket.send((command_type + msg).encode())
        except:
            self.connection_lost()

    def s_recv(self, size, expected_type):
        try:
            msg = self.client_socket.recv(size).decode()
            # If received a quit signal from the server
            if msg[0] == "Q":
                why_quit = ""
                try:
                    why_quit = self.client_socket.recv(1024).decode()
                except:
                    pass
                print(msg[1:] + why_quit)
                # Throw an error
                raise Exception
            # If received an echo signal from the server
            elif msg[0] == 'E':
                # Echo the message back to the server
                self.s_send("e", msg[1:])
                # Recursively retrive the desired message
                return self.s_send(size, expected_type)
            elif msg[0] == 'H':
                # Echo the message back to the server
                # self.s_send("e", msg[1:])
                # Recursively retrive the desired message
                return self.s_send(size, expected_type)
            # If the command type token is not the expected type
            elif msg[0] != expected_type:
                print("The received command type \"" + msg[0] + "\" does not " +
                      "match the expected type \"" + expected_type + "\".")
                # Connection lost
                self.connection_lost()
            if msg[0] == "I":
                return int(msg[1:])
            else:
                return msg[1:]
        except:
            print("MEH EH")
            exit()
        return None

    def connection_lost(self):
        try:
            self.client_socket.send("q".encode())
        except:
            pass
        # Raise an error to finish
        raise Exception

    def start_game(self):
        # odbieramy swoje id
        self.player_id = int(self.s_recv(128, "A"))
        print(self.player_id)
        # potwierdzenie ze sie jest XDD???

        self.connected()

        # daj mi role

        self.role = str(self.s_recv(2, "R"))
        print("My role: "+ str(self.role))

        # wysylamy ze ok XD
        self.s_send("c", "2")

        # Receive the mactched player's ID from the server
        self.match_id = int(self.s_recv(128, "I"))
        print("My partner id is: "+ str(self.match_id))
        # Confirm the mactched player's ID has been received
        self.s_send("c", "3")

        print(("You are now matched with player " + str(self.match_id)
               + "\nYou are the \"" + self.role + "\""))

        # Start the main loop
        self.main_loop()

    def connected(self):
        print("Welcome to Tic Tac Toe online, player " + str(self.player_id)
              + "\nPlease wait for another player to join the game...")

    def main_loop(self):
        while True:
            board_content = self.s_recv(10, "B")
            header = self.s_recv(1024, "H")
            print(board_content)
            print(header)

    def __update_board__(self, command, board_string):

        if command == "Y":
            # If it's this player's turn to move, print out the current
            # board with " " converted to the corresponding position number
            print("Current board:\n" + self.format_board(
                self.show_board_pos(board_string)))
        else:
            # Print out the current board
            print("Current board:\n" + self.format_board(
                board_string))

    def format_board(s):
        """(Static) Formats the grid board."""

        # If the length of the string is not 9
        if (len(s) != 9):
            # Then print out an error message
            print("Error: there should be 9 symbols.");
            # Throw an error
            raise Exception;

        # Draw the grid board
        # print("|1|2|3|");
        # print("|4|5|6|");
        # print("|7|8|9|");
        return ("|" + s[0] + "|" + s[1] + "|" + s[2] + "|\n"
                + "|" + s[3] + "|" + s[4] + "|" + s[5] + "|\n"
                + "|" + s[6] + "|" + s[7] + "|" + s[8] + "|\n");


def main():
    # If there are more than 3 arguments
    if (len(argv) >= 3):
        # Set the address to argument 1, and port number to argument 2
        address = argv[1]
        port_number = argv[2]
    else:
        port_number = input("Please enter the port:")
        address = input("Please enter the server address: ")

    client = Client()
    server_address = (address, int(port_number))
    client.connect(server_address)
    client.start_game()


main()
