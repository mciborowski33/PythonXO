import socket
from sys import argv


class Client:

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server_address):
        self.client_socket.connect(server_address)
        try:
            message = 'ALE ON MA........ NIHIHIHHIHHIHIHIHIHIHIHIHIHIHIHIHIHIHII!'
            print("sending: " + message)
            self.client_socket.sendall(message.encode())

            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = self.client_socket.recv(16).decode()
                amount_received += len(data)
                print("Received: " + str(data))
        finally:
            print("Closing socket....")
            self.close()

    def close(self):
        # Shut down the socket to prevent further sends/receives
        self.client_socket.shutdown(socket.SHUT_RDWR)
        # Close the socket
        self.client_socket.close()


def main():
    # If there are more than 3 arguments
    if (len(argv) >= 3):
        # Set the address to argument 1, and port number to argument 2
        address = argv[1]
        port_number = argv[2]
    else:
        # Ask the user to input the address and port number
        # address = input("Please enter the address:")
        port_number = input("Please enter the port:")
        address = input("Please eneter the server address: ")

    client = Client()
    server_address = (address, int(port_number))
    client.connect(server_address)


main()
