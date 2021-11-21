import socket
import time
import numpy as np
from matplotlib.pyplot import figure, plot, grid
import argparse
from src.send_msg_over_socket import MsgSender
from src.msg_generator import MsgGenerator
import os.path

def bt2int(bt):
    w = 2 ** np.array(range(8))[::-1]
    return np.dot(bt, w)

def msg2bt(msg):
    bt = []
    for i in range(len(msg)):
        for b in msg[i]:
            bt.append(int(b))
    return bt

def extract_payload_from_bitstream(bitstream):
        return bitstream[2:-1]

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--port', type=int, default=4444, help='The port of the server you would like to send a message to.')
parser.add_argument('--serv_address', type=str, default='23.235.207.63', help='The address of the server you would like to send a message to.')
parser.add_argument('--file_to_send', type=str, default='resources/umdlogo.jpg', help='The name of the file to send. If unspecified, the default umdlogo image will be used. ')
if __name__ == '__main__':
    args = parser.parse_args()

    # Create message to send
    print("Creating message to send from following file: " + str(args.file_to_send))
    msg = MsgGenerator(args.file_to_send, packet_length_in_bits = 1024)

    # # Establish connection with server
    print("Connecting to Server: " + args.serv_address + ":" +str(int(args.port)))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message_sender = MsgSender(args.serv_address, args.port)
    message_sender.send_msg(msg)

    bt = bytes()
    for recievedFrame in message_sender.received_frames:
        bt = bt + extract_payload_from_bitstream(recievedFrame)

    ext = os.path.splitext(args.file_to_send)[-1]
    print(ext)
    with open("Output_file" + ext,'wb') as ofile:
        ofile.write(bt) 

    
    # latency, sucess_or_fail = sendMessageToServer(socket, message, crc)
    # plot