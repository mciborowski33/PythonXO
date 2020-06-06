import socket
import threading
import time
from sys import argv
from game import Game


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
        self.lock_matching = threading.Lock()
        self.__main_loop()

    def __main_loop(self):
        # Loop to infinitely accept new clients
        while True:
            # accept client
            connection, client_address = self.server_socket.accept()
            new_player = Player(connection)
            self.waiting_players.append(new_player)
            print("Recived connection from: " + str(client_address))
            print(new_player.id)
            try:
                threading.Thread(target=self.client_thread, args=(new_player,)).start()
            except:
                print("The problem with client occured")

    def client_thread(self, player):
        try:
            # send client ids
            player.send("A", str(player.id))
            while player.is_waiting:
                # If the player is still waiting for another player to join
                # Try to match this player with other waiting players
                match_result = self.matching_player(player)

                if match_result is None:
                    time.sleep(1)
                else:
                    # if matched with another player
                    # Initialize a new Game object to store the game's infomation
                    new_game = Game(player, match_result)
                    try:
                        new_game.start()
                    except:
                        print("Game is unexpectadly finished -,-")
                    return
        except:
            print("Player " + str(player.id) + " disconnected.")
        finally:
            # remove client from waiting list
            self.waiting_players.remove(player)

    def matching_player(self, player):
        self.lock_matching.acquire()
        try:
            for p in self.waiting_players:
                if p.is_waiting and p is not player:
                    player.match = p
                    p.match = player
                    player.role = "X"
                    p.role = "O"
                    player.is_waiting = False
                    p.is_waiting = False
                    return p
        finally:
            # eh XD!
            self.lock_matching.release()
        return None


class Player:

    count = 0

    def __init__(self, connection):
        Player.count = Player.count+1
        self.id = Player.count
        self.connection = connection
        self.is_waiting = True
        self.role = None
        self.match = None

    def recv(self, size, expected_type):
        try:
            msg = self.connection.recv(size).decode()
            if msg[0] == "q":
                self.__connection_lost()
            elif msg[0] != expected_type:
                self.__connection_lost()
            elif msg[0] == "i":
                return int(msg[1:])
            else:
                return msg[1:]
            return msg
        except:
            # If any error occurred, the connection might be lost
            self.__connection_lost()
        return None

    def send(self, command_type, msg):
        try:
            self.connection.send((command_type + msg).encode())
        except:
            self.__connection_lost()
            print("Something went wrong - one of the clients failed")

    def send_match_info(self):
        # Send to client the assigned role
        self.send("R", self.role)
        # Waiting for client to confirm
        if self.recv(2, "c") != "2":
            self.__connection_lost()
        # Sent to client the matched player's ID
        self.send("I", str(self.match.id))
        # Waiting for client to confirm
        if self.recv(2, "c") != "3":
            self.__connection_lost()

    def __connection_lost(self):
        try:
            # inform clients about lost connections
            self.match.send("Q", "The other player has lost connection" +
                            " with the server.\nGame over.")
        except:
            pass
        raise Exception


def main():
    # If there are more than 2 arguments
    if len(argv) >= 2:
        # Set port number to argument 1
        # address = argv[1]
        port_number = argv[1]
    else:
        # Ask the user to input port number
        port_number = input("Please enter the port: ")
        # address = int("Please enter the server address: ")

    try:
        address = "127.0.0.1"
        server_address = (address, int(port_number))
        server = Server()
        server.bind(server_address)
        server.start_game()
        # server.close()
    finally:
        print("I wish you Merry Christmas and a Happy New Year!")

main()
