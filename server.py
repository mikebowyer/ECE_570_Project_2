from socket import *
import random
import sys

def server(port):
    # Create a UDP socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)

    # Assign IP address and port number to socket
    serverSocket.bind(('23.235.207.63', port))
    print('server bind at ', serverSocket)

    # setup counter for loop
    cnt = 1;
    while True:
        # Generate random number in the range of 0 to 10
        rand = random.randint(0, 10)

        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(2048)

        print('[', cnt, ']: ', address, '>>', message)
        cnt += 1

        # If rand is less is than 2, the packet got errors by inverting the last                                                                                                                                                              two bits
        if rand < 2:
            message = message[:-2] + b'FF'

        # Otherwise, the server responds
        serverSocket.sendto(message, address)
        if rand < 2:
            print('Send back message to ', address, 'with Errors!')
        else:
            print('Send back message to ', address)

if __name__ == "__main__":
    port = int(sys.argv[1])
    server(port)


