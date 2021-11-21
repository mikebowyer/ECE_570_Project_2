import socket
import time

class MsgSender:
    packet_header = [0, 1, 1, 1, 1, 1, 1, 0]


    def __init__(self, server_address, server_port):
        # Save server information to member variables
        self.m_server_address = (server_address, server_port)

        # Setup Socket 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.1)

        # Setup lists to save metrics into 
        self.received_frames = []
        self.latencies = []

    def send_and_wait_for_packet(self, packet):
        # print("Sending packet: " + str(packet))
        # print('.............' + str(cnt) + '.............')
        send_time = time.time()
        sent = self.sock.sendto(packet, self.m_server_address)
        
        try:
            packetRx, server = self.sock.recvfrom(1024)
            recv_time = time.time()
            latency = int((recv_time - send_time) * 1e6)
            print('package bounced back latency: ' + str(latency) + ' mu')
        except socket.timeout:
            raise "Recieve Timeout"

        return packetRx
        

    def send_msg(self, message_to_send):
        packets_successfully_sent_count = 0
        while packets_successfully_sent_count < message_to_send.total_number_of_frames:
            # Grab frame to send
            i = packets_successfully_sent_count
            frame = message_to_send.frames[i]
            
            # Debug it a 
            if True:
                print("\n------ Frame Number " + str(i) + "------")
                print("Sent Packet Length: " + str(len(frame.get_frame())))
                if False:
                    print("Header: " + str(frame.header))
                    print("Counter" + str(frame.counter))
                    print("Payload" + str(frame.payload))
                    print("CRC" + str(frame.crc))

            sent_frame = frame.get_frame_bytes()
            try:
                recieved_frame = self.send_and_wait_for_packet(sent_frame)
            except:
                # Messa
                continue

            # print("Recieved Packet Length: " + str(len(recieved_frame)))

            if (recieved_frame == sent_frame):
                packets_successfully_sent_count +=1
                self.received_frames.append(recieved_frame)
            else:
                continue

            # crc_length = len(frame.crc)
            # if(recieved_packet[-crc_length:] == frame.crc):
            #     packets_successfully_sent_count +=1
            # else: 
            #     continue
            




