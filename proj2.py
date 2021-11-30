import socket
import time
import numpy as np
import matplotlib.pyplot as plt
import argparse
from src.send_msg_over_socket import MsgSender
from src.msg_generator import MsgGenerator
from src.output_creator import OutputCreator


def bt2int(bt):
    w = 2 ** np.array(range(8))[::-1]
    return np.dot(bt, w)

def msg2bt(msg):
    bt = []
    for i in range(len(msg)):
        for b in msg[i]:
            bt.append(int(b))
    return bt



parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--port', type=int, default=4444, help='The port of the server you would like to send a message to.')
parser.add_argument('--serv_address', type=str, default='23.235.207.63', help='The address of the server you would like to send a message to.')
parser.add_argument('--file_to_send', type=str, default='resources/umdlogo.jpg', help='The name of the file to send. If unspecified, the default umdlogo image will be used. ')
parser.add_argument('--show_plots', dest='show_plots', action='store_true')

if __name__ == '__main__':
    args = parser.parse_args()

    # Create message to send
    print("------------------------------------------------------------------------")
    print("------------------ Creating Message To Send From File ------------------")
    print("------------------------------------------------------------------------")
    print("Creating message to send from following file: " + str(args.file_to_send) + "\n")
    msg = MsgGenerator(args.file_to_send, payload_length = 1024)

    # Send the message and collect stats as we go!
    print("\n------------------------------------------------------------------------")
    print("-------------------------- Sending the Message -------------------------")
    print("------------------------------------------------------------------------")
    message_sender = MsgSender(args.serv_address, args.port)
    message_sender.send_msg(msg)

    # Take the raw bits recieved back from the server and recreate the original
    print("\n------------------------------------------------------------------------")
    print("----------------- Saving recieved file and metrics ---------------------")
    print("------------------------------------------------------------------------")
    output_created = OutputCreator(message_sender, args.file_to_send, args.show_plots)