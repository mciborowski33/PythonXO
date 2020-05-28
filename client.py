import socket
from sys import argv


class Client:

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
                return self.s_recv(size, expected_type)
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
        self.player_id = int(self.s_recv(128, "A"))
        print(self.player_id)
        # potwierdzenie ze sie jest XDD???

        self.connected()

        # daj mi role

        self.role = str(self.s_recv(2, "R"));

    def connected(self):
        print("Welcome to Tic Tac Toe online, player " + str(self.player_id)
              + "\nPlease wait for another player to join the game...");


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
