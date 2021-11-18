import socket
import time
from numpy.random import randint
from matplotlib.pyplot import figure, plot, grid
import argparse


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--port', type=int, default=4444, help='The port of the server you would like to send a message to.')
if __name__ == '__main__':
    args = parser.parse_args()
    print("Connecting to Server on Port: " + str(int(args.port)))
    # Establish connection with server
    # Create message which will be sent
    # latency, sucess_or_fail = sendMessageToServer(socket, message, crc)
    # plot