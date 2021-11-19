import socket
import time
import numpy as np

class Frame:
    def __init__(self, header = [], counter = [], payload = [], crc = []):
        self.header = header
        self.counter = counter
        self.payload = payload
        self.crc = crc

class MsgGenerator:
    def __init__(self, filename, packet_length_in_bits):
        # Save passed variables into class variables
        self.filename = filename
        self.packet_len = packet_length_in_bits

        # Read in the desired file to transmit
        with open(self.filename,'rb') as file:
            file_buffer = file.read()

        # Read the files contents into a bitstream
        self.message_in_bytes = ['{:08b}'.format(b) for b in file_buffer]
        self.message_in_bits = self.message_in_bytes_to_bits(self.message_in_bytes)

        # Calculate the number of frames needed to transmit this bad boi
        self.total_number_of_frames = int(np.ceil(len(self.message_in_bits)/self.packet_len))
        
        # Generate a list of frames to send
        self.frames = self.generate_msg(self.total_number_of_frames)



    def generate_msg(self, total_number_of_frames):
        frames = []
        for i in range(0, total_number_of_frames):
            # Create new frame to add to list of frames
            newFrame = Frame()
            newFrame.header = list([0, 1, 1, 1, 1, 1, 1, 0])
            newFrame.counter = [int(b) for b in '{:08b}'.format(i)]

            # Stuff payload
            bitIndexStart = i * self.packet_len
            # if(i < len(total_number_of_frames)-1):
            bitIndexEnd = ((i + 1) * self.packet_len)
            newFrame.payload = self.message_in_bits[bitIndexStart:bitIndexEnd]
            # else:
            #     # Calculate how many additional bits are needed in the last frame
            #     numBitsToStuff = (total_number_of_frames * self.packet_len) - len(self.message_in_bits)
            #     bitIndexEnd = ((i + 1) * self.packet_len) - 1
            #     lastPayload = 
            #     newFrame.payload = self.message_in_bits[bitIndexStart:bitIndexEnd]

            frame_wo_crc = newFrame.header + newFrame.counter + newFrame.payload

            newFrame.crc = self.calc_frame_crc(frame_wo_crc, [1, 1, 0, 0, 1])

            frames.append(newFrame)



            

    def calc_frame_crc(self, frame_wo_crc, generator):
        
        return list([1, 1, 1, 1])



    def message_in_bytes_to_bits(self, msg):
        bt = []
        for i in range(len(msg)):
            for b in msg[i]:
                bt.append(int(b))
        return bt

    def bt2int(self, bt):
        w = 2 ** np.array(range(8))[::-1]
        return np.dot(bt, w)
