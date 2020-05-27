import socket
import threading
from sys import argv


class Server:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self, server_address):
        while True:
            try:
                self.server_socket.bind(server_address)
                print("Waiting for clients....")
                self.server_socket.listen(1)
                break
            except:
                print("There is an error when trying to bind " +
                      str(server_address[1]))
                print("Try again")
                exit()

    def close(self):
        print("Closing connection....")
        self.server_socket.close()

    def start_game(self):
        self.waiting_players = []
        self.__main_loop()

    def __main_loop(self):
        # Loop to infinitely accept new clients
        while True:
            #akceptujemy klientow
            connection, client_address = self.server_socket.accept()
            new_player = Player(connection)
            self.waiting_players.append(new_player)
            print("Recived connection from: " + str(client_address))
            print(new_player.id)
            try:
                threading.Thread(target=self.client_thread, args = (new_player,)).start()
            except:
                print("Sth went wrong..... ")

    def client_thread(self, player):
        try:
            player.send("A", str(player.id))
        except:
            print("Sth went wrong")
        finally:
            self.waiting_players.remove(player)


class Player:

    count = 0

    def __init__(self, connection):
        Player.count = Player.count+1
        self.id = Player.count
        self.connection = connection
        self.is_waiting = True

    def send(self, command_type, msg):
        try:
            self.connection.send((command_type + msg).encode())
        except:
            print("EH")
            exit()



def main():
    # If there are more than 2 arguments
    if (len(argv) >= 2):
        # Set port number to argument 1
        # address = argv[1]
        port_number = argv[1]
    else:
        # Ask the user to input port number
        port_number = input("Please enter the port: ")
        # address = int("Please enter the server address: ")

    try:
        address = "192.168.1.4"
        server_address = (address, int(port_number))
        server = Server()
        server.bind(server_address)
        server.start_game()
        #server.close()
    finally:
        print("Boranheyo <3")


main()
