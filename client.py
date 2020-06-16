import socket
from sys import argv


class Client:

    def __init__(self):
        # open socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_id = None
        self.role = None
        self.match_id = None

    def connect(self, server_address):
        while True:
            try:
                print("Connecting to the game server...")
                # connect to the server
                self.client_socket.connect(server_address)
                return True
            except:
                # if problem -> end program
                print("A problem occured... try again")
                exit()
            return False

    def close(self):
        # shut down the socket to prevent further sends/receives
        self.client_socket.shutdown(socket.SHUT_RDWR)
        # close the socket
        self.client_socket.close()

    # send function to add command type and msg
    def s_send(self, command_type, msg):
        try:
            self.client_socket.send((command_type + msg).encode())
        except:
            # if send function fails send info
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
                # print(msg[1:] + why_quit)
                print(why_quit)
                # Throw an error
                #raise Exception
            elif msg[0] == 'B':  # board
                return msg[1:]
            elif msg[0] == 'C':  # state - play, wait, win, loose
                return msg[1:]
            # elif msg[0] == 'P':
            #     return msg[1:]
            # If the command type token is not the expected type
            elif msg[0] != expected_type:
                print("The received command type \"" + msg[0] + "\" does not " +
                      "match the expected type \"" + expected_type + "\".")
                # Connection lost
                self.connection_lost()
            # if msg[0] == "I":  # oppontent move
            #     return int(msg[1:])
            else:
                return msg[1:]
        except:
            pass
        raise Exception

    def connection_lost(self):
        try:
            # send info that something is wrong
            self.client_socket.send("q".encode())
        except:
            # raise and error if it something serious
            print("Connection is lost... dragon ate the server or another player")
            raise Exception

    def start_game(self):
        try:
            # recv my id
            self.player_id = int(self.s_recv(128, "A"))
            self.connected()
            # info about the role
            self.role = str(self.s_recv(2, "R"))
            print("My role: " + str(self.role))
            # send ack that everything is ok
            self.s_send("c", "2")
            # Receive the matched player's ID from the server
            self.match_id = int(self.s_recv(128, "I"))
            print("My partner id is: " + str(self.match_id))
            # Confirm the matched player's ID has been received
            self.s_send("c", "3")
            print(("You are now matched with player " + str(self.match_id)
                   + "\nYou are the \"" + self.role + "\""))
            # Start the main loop
            self.main_loop()
        except:
            self.connection_lost()

    def connected(self):
        print("Welcome to PythonXO, player " + str(self.player_id)
              + "\nPlease wait for another player to join the game...\n So get a cup of tea or something else ( ͡° ͜ʖ ͡°)")

    def main_loop(self):
        while True:
            # recv current board
            board_content = self.s_recv(1024, "B")
            # recv state
            command = self.s_recv(2, "C")
            # update board
            self.__update_board__(command, board_content)
            if command == "Y":
                # If it's this player's turn to move
                self.__player_move__(board_content)
            elif command == "N":
                # If the player needs to just wait
                self.__player_wait__()
            elif command == "D":
                # If the result is a draw
                print("It's a draw.")
                break
            elif command == "W":
                # If this player wins
                print("You WIN!")
                # Break the loop and finish
                break
            elif command == "L":
                # If this player loses
                print("You lose.... :'(")
                # Break the loop and finish
                break
            else:
                # If the server sends back anything unrecognizable
                # Simply print it
                print("Error: unknown message was sent from the server, probably it went mad so goodbye")
                # And finish
                break

    def __player_move__(self, board_string):
        while True:
            # Prompt the user to enter a position
            try:
                position = int(input('Please enter the position (1~9):'))
            except:
                print("Invalid input.")
                continue
            # check if position exists
            if 1 <= position <= 9:
                if board_string[position-1] != " ":
                    print("This position is occupied!")
                else:
                    break
            else:
                print("Please enter a value between 1 and 9 that" +
                      "corresponds to the position on the grid board.")
        self.s_send("i", str(position))

    def __player_wait__(self):
        print("Waiting for the other player to make a move...")

    def __update_board__(self, command, board_string):
        if command == "Y":
            # If it's this player's turn to move, print out the current
            # board with " " converted to the position number
            print("Current board:\n" + self.format_board(self.show_board_pos(board_string)))
        else:
            # Print out the current board
            print("Current board:\n" + self.format_board(self.show_board_pos(board_string)))

    def show_board_pos(self, s):
        new_s = list("123456789")
        for i in range(0, 9):
            if s[i] != " ":
                new_s[i] = s[i]
        return "".join(new_s)

    def format_board(self, s):
        # If the length of the string is not 9
        if len(s) != 9:
            # Then print out an error message
            print("Error: there should be 9 symbols.")
            # Throw an error
            raise Exception
        return ("|" + s[0] + "|" + s[1] + "|" + s[2] + "|\n"
                + "|" + s[3] + "|" + s[4] + "|" + s[5] + "|\n"
                + "|" + s[6] + "|" + s[7] + "|" + s[8] + "|\n")


def main():
    # If there are more than 3 arguments
    if len(argv) >= 3:
        # Set the address to argument 1, and port number to argument 2
        address = argv[1]
        port_number = argv[2]
    else:
        # port_number = input("Please enter the port:")
        # address = input("Please enter the server address: ")
        # address = socket.getaddrinfo("stormwind", 12345)[0][4][0]
        address = "127.0.0.1"
        port_number = 12345

    client = Client()
    print("Connecting to " + address)
    server_address = (address, int(port_number))
    client.connect(server_address)
    client.start_game()


main()
