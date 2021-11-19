import socket
import time

class MsgSender:
    packet_header = [0, 1, 1, 1, 1, 1, 1, 0]


    def __init__(self, server_address, server_port, message_to_send):
        # Save server information to member variables
        self.m_server_address = (server_address, server_port)
        self.message_to_send = message_to_send

        # Setup Socket 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.1)

        # Setup lists to save metrics into 
        self.latencies = []

        # Send Message!
        self.send_msg(self.message_to_send)


    def send_and_wait_for_packet(self, packet):
        print("Sending packet: " + str(packet))
        # print('.............' + str(cnt) + '.............')
        send_time = time.time()
        sent = self.sock.sendto(packet.encode(), self.server_address)
        
        try:
            packetRx, server = self.sock.recvfrom(1024)
            recv_time = time.time()
            latency = int((recv_time - send_time) * 1e6)
            print('package bounced back latency: ' + str(latency) + ' mu')
        except socket.timeout:
            raise "Recieve Timeout"

        return packetRx
        

    def send_msg(self, msg):
        print("Sending msg: " + str(msg))



