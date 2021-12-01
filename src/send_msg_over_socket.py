import socket
import time
from src.msg_generator import Frame, CRCCalculator
from tqdm import tqdm

class MsgSender:
    packet_header = [0, 1, 1, 1, 1, 1, 1, 0]


    def __init__(self, server_address, server_port):
        print("Connecting to Server: " + server_address + ":" +str(int(server_port)) + "\n")
        # Save server information to member variables
        self.m_server_address = (server_address, server_port)

        # Setup Socket 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.1)

        # Setup lists to save metrics into 
        self.received_frames = []
        self.latencies = []
        self.success_rate = []

    def send_and_wait_for_packet(self, packet):
        # print("Sending packet: " + str(packet))
        # print('.............' + str(cnt) + '.............')
        send_time = time.time()
        sent = self.sock.sendto(packet, self.m_server_address)
        
        try:
            packetRx, server = self.sock.recvfrom(1024)
            recv_time = time.time()
            latency = int((recv_time - send_time) * 1e6)
            # print('package bounced back latency: ' + str(latency) + ' mu')
            self.latencies.append(latency * 10 ** -3)
        except socket.timeout:
            raise "Recieve Timeout"

        return packetRx
        

    def send_msg(self, message_to_send):
        packets_successfully_sent_count = 0
        packets_recieved_with_errors_or_timeout = 0
        with tqdm(total=message_to_send.total_number_of_frames) as pbar:

            while packets_successfully_sent_count < message_to_send.total_number_of_frames:
                # Grab frame to send
                i = packets_successfully_sent_count
                frame = message_to_send.frames[i]
                
                # Debug it a 
                sent_frame = frame.get_frame_bytes()
                if False:
                    print("\n------ Frame Number " + str(i) + "------")
                    print("Sent Packet Length: " + str(len(sent_frame)) + " bytes")
                    if False:
                        print("Header: " + str(frame.header))
                        print("Counter" + str(frame.counter))
                        print("Payload" + str(frame.payload))
                        print("CRC" + str(frame.crc))

                try:
                    recieved_bytes = self.send_and_wait_for_packet(sent_frame)
                    # print("Recieved Packet Length: " + str(len(recieved_bytes)))
                except:
                    packets_recieved_with_errors_or_timeout += 1 
                    continue

                # print("Recieved Packet Length: " + str(len(recieved_frame)))

                recieved_frame = Frame()
                recieved_frame.createFrameFromBytes(recieved_bytes)
                recieved_frame_crc = recieved_frame.crc
                crc_calc = CRCCalculator()
                recieved_frame_calculated_crc = crc_calc.getCRC(frame = recieved_frame.get_frame_wo_crc(), div = [1, 1, 0, 0, 1])

                if (recieved_frame_crc == recieved_frame_calculated_crc) and (recieved_frame.counter == frame.counter):
                    # print("SUCCESS! Recieved frame correctly, moving to next.")
                    packets_successfully_sent_count +=1
                    self.received_frames.append(recieved_bytes)

                    # Update Metrics
                    current_success_rate = packets_successfully_sent_count / (packets_successfully_sent_count + packets_recieved_with_errors_or_timeout)
                    self.success_rate.append(current_success_rate)
                    
                    # Update Progress Bar
                    pbar.update(1)
                else: 
                    packets_recieved_with_errors_or_timeout += 1
                    # print("FAILURE! Recieved frame incorrectly, Retrying")
                    continue



            

    



