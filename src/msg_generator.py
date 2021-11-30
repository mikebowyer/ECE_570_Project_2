import socket
import time
import numpy as np
import cv2
import os
from tqdm import tqdm

class Frame:

    def __init__(self, header = [], counter = [], payload = [], crc = []):
        self.header = header
        self.counter = counter
        self.payload = payload
        self.crc = crc
    
    def createFrameFromBytes(self, bytes):
        bitstream = []
        for byte in bytes:
            byte_in_int_list = [int(i) for i in list(format(byte,'b'))]
            numZerosToPad = 8 - len(byte_in_int_list)
            byte_in_int_list = ([0] * (numZerosToPad)) + byte_in_int_list
            bitstream = bitstream + byte_in_int_list

        self.header = bitstream[0:8]
        self.counter = bitstream[8:16]
        self.payload = bitstream[16:-8]
        self.crc = bitstream[-8:]


    def get_frame(self):
        return self.header + self.counter + self.payload + self.crc

    def get_frame_wo_crc(self):
        return self.header + self.counter + self.payload
    
    def get_frame_bytes(self):
        frame = self.get_frame()

        if (len(frame) % 8) != 0:
            raise Exception("The length of the frame is not divisable by 8 bits without a remainder. More padding necassary")

        frame_bytes_as_ints = []
        for i in range(0, int(len(frame)/8)):
            byte = frame[i * 8 : i * 8 + 8]
            byte_val = byte[0] * 128 + byte[1] * 64 + byte[2] * 32 + byte[3] * 16 +byte[4] * 8 + byte[5] * 4 + byte[6] * 2 + byte[7]
            frame_bytes_as_ints.append(byte_val)
        return bytes(frame_bytes_as_ints)

class CRCCalculator:
    def __init__(self):
        pass

    def padInputBits(self, frameToSend, degreeOfDiv):
        padded_frame = frameToSend + [0] * (degreeOfDiv - 1)
        return padded_frame

    def leftStripBits(self,inputBits):
        inputBitsStr = str(inputBits)
        #print(inputBitsStr)
        i = 0
        indexTochopTo = None
        for char in inputBits:
            #print(char)
            if char == 1:
                indexTochopTo = i
                #print("Ind to chop to " + str(indexTochopTo))
                break
            i = i + 1
        return inputBits[indexTochopTo:]

    def padDiv(self, lenOfRemainingBits, div):
        padded_div = div + [0] * (lenOfRemainingBits - len(div))
        #print(padded_div)
        return padded_div

    def subtract(self, leftStrippedRemainingBits, rightPaddedDiv):
        remainder = []
        for remainBit, divBit in zip(leftStrippedRemainingBits, rightPaddedDiv):
            #print(str(remainBit) + "^" + str(divBit) )
            remainder.append(int(remainBit) ^ int(divBit))
            #print(remainder)
        return remainder
    
    def left_strip_and_pad_remainder(self, remainder, div):
        # crc_length = len(div) - 1
        crc_length = 8
        stripped_padded_crc = [0] * crc_length
        if (len(remainder) <= crc_length):
            left_stipped_crc = self.leftStripBits(remainder)

            # Create 0 padded list
            num_pad_bits_needed = crc_length - len(left_stipped_crc)
            padding_bits = [0] * num_pad_bits_needed

            stripped_padded_crc = padding_bits + left_stipped_crc
        else: #CRC is all zeros of large length
            # Return CRC of all zeros
            pass
        return stripped_padded_crc


    
    def getCRC(self, frame, div):
        # print("Original frame to send: " + str(frame))
        # print("Div: " + str(div))
        
        #Pad the frame with added zeros
        padded_frame = self.padInputBits(frame, len(div))
        # print("Padded original frame: " + str(padded_frame))
        
        remainingBits = padded_frame
        while 1:
            #print("Remaining Bits: " + str(len(remainingBits)))
            remainingBits = self.leftStripBits(remainingBits)
            if len(remainingBits) < len(div):
                break
            # print("Left Stripped remaining bits: \t" + str(remainingBits))
            padded_div = self.padDiv(len(remainingBits), div)
            # print("Zero Padded Div: \t\t" + str(padded_div))
            remainingBits = self.subtract(remainingBits, padded_div)
            if (max(remainingBits) == 0):
                #crc is all zeros
                break
            # print("Remainder: \t\t\t" + str(remainingBits))
            
        # Ensure CRC is always desired 
        return self.left_strip_and_pad_remainder(remainingBits, div)



class MsgGenerator:
    def __init__(self, filename, payload_length):
        # Save passed variables into class variables
        if filename == "webcam":
            self.filename = self.grabAndSaveWebCamImage()
        else: 
            self.filename = filename
        self.payload_length = payload_length
        self.header = list([0, 1, 1, 1, 1, 1, 1, 0])
        self.header_len = len(self.header)
        self.counter_len = 8
        self.crc_len = 8
        self.packet_len = self.payload_length + self.header_len + self.counter_len + self.crc_len


        # Read in the desired file to transmit
        with open(self.filename,'rb') as file:
            file_buffer = file.read()

        # Read the files contents into a bitstream
        self.message_in_bytes = ['{:08b}'.format(b) for b in file_buffer]
        self.message_in_bits = self.message_in_bytes_to_bits(self.message_in_bytes)

        # Calculate the number of frames needed to transmit this bad boi
        self.total_number_of_frames = int(np.ceil(len(self.message_in_bits)/(self.payload_length)))
        
        # Generate a list of frames to send
        self.crc_calculator = CRCCalculator()
        # print("Generating Message! ")
        self.frames = self.generate_msg(self.total_number_of_frames)

    def createOutputDir(self):
        # Create new directory for outputs
        output_dir_exists = os.path.exists("outputs/")
        if not output_dir_exists:
            os.makedirs("outputs/")

    def grabAndSaveWebCamImage(self):
        print("Webcam input selected as source file!")
        print("Webcam will open and wait for the user to press 'q' to capture an image which will then be sent.")

        # Create Dir where to store image
        self.createOutputDir()
        
        #Capture and show image
        vid = cv2.VideoCapture(0)
        vid.set(3,640) #Setting webcam's image width 
        vid.set(4,320) #Setting webcam' image height

  
        while(True):
            
            # Capture the video frame
            # by frame
            ret, frame = vid.read()
        
            # Display the resulting frame
            cv2.imshow('frame', frame)
            
            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Save image
        original_webcam_img_path = 'outputs/original_webcam_image.png'
        b = cv2.resize(frame,(160,80),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        cv2.imwrite(original_webcam_img_path, b)

        # Tear down and disconnect from webcam
        vid.release()
        cv2.destroyAllWindows()

        return original_webcam_img_path

    def generate_msg(self, total_number_of_frames):
        frames = []
        for i in tqdm(range(0, total_number_of_frames)):
            # print("Generating Message for frame #: " + str(i))
            # Create new frame to add to list of frames
            newFrame = Frame(header = [], counter = [], payload = [], crc = [])
            newFrame.header = self.header
            counter_mod_255 = i % 255
            newFrame.counter = [int(b) for b in '{:08b}'.format(counter_mod_255)]

            # Stuff payload
            bitIndexStart = i * self.payload_length
            if(i < (total_number_of_frames -1 )):
                bitIndexEnd = ((i + 1) * self.payload_length)
            else: # if on last message
                bitIndexEnd = len(self.message_in_bits)
            newFrame.payload = self.message_in_bits[bitIndexStart:bitIndexEnd]
            # if(len(newFrame.payload) != self.packet_len):
            #     numZerosToPad = self.packet_len - len(newFrame.payload)
            #     newFrame.payload = newFrame.payload + ([0] * numZerosToPad)
                
            # else:
            #     # Calculate how many additional bits are needed in the last frame
            #     numBitsToStuff = (total_number_of_frames * self.packet_len) - len(self.message_in_bits)
            #     bitIndexEnd = ((i + 1) * self.packet_len) - 1
            #     lastPayload = 
            #     newFrame.payload = self.message_in_bits[bitIndexStart:bitIndexEnd]

            frame_wo_crc = newFrame.header + newFrame.counter + newFrame.payload

            
            newFrame.crc = self.crc_calculator.getCRC(frame = frame_wo_crc, div = [1, 1, 0, 0, 1])

            frames.append(newFrame)
        return frames

    def message_in_bytes_to_bits(self, msg):
        bt = []
        for i in range(len(msg)):
            for b in msg[i]:
                bt.append(int(b))
        return bt

    def bt2int(self, bt):
        w = 2 ** np.array(range(8))[::-1]
        return np.dot(bt, w)


