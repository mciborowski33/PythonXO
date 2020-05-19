import socket
from sys import argv


class Server:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self, server_address):
        self.server_socket.bind(server_address)
        self.server_socket.listen(1)
        while True:
            # Wait for a connection
            print("Waiting for clients....")
            connection, client_address = self.server_socket.accept()
            try:
                print("Connection from: " + str(client_address))
                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    print("Recived: " + str(data.decode()))
                    if data:
                        print("Sending data back to the client")
                        connection.sendall(data)
                    else:
                        print("No more data from: " + str(client_address))
                        break
            finally:
                print("Closing connection....")
                connection.close()

    def close(self):
        self.server_socket.close()


def main():
    # If there are more than 2 arguments
    if (len(argv) >= 2):
        # Set port number to argument 1
        port_number = argv[1]
    else:
        # Ask the user to input port number
        port_number = input("Please enter the port: ")

    try:
        server_address = ("192.168.1.4", int(port_number))
        server = Server()
        server.bind(server_address)
    finally:
        print("Boranheyo <3")


main()

