import socket
import time
from numpy.random import randint
from matplotlib.pyplot import figure, plot, grid

def hexString(bt):
    hs = ''
    for i in range(int(len(bt)/4)):
        bt4 = bt[i * 4 : i * 4 + 4]
        a = bt4[0] * 8 + bt4[1] * 4 + bt4[2] * 2 + bt4[3]
        hs += hex(a)[2:]
    return hs

def bitStream(msg):
    return [int(b) for b in bin(int(msg, 16))[2:].zfill(4 * len(msg))]

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('23.235.207.63', 4444)
msg = ''
lst = randint(256, size = 1)
for n in lst:
    msg += str(hex(n)[2:])

btTx = bitStream(msg)
btTx += [0, 0, 0, 0]
div = [1, 1, 0, 0, 1]
header = [0, 1, 1, 1, 1, 1, 1, 0]
    
latency = []
per = []
cnt = 0
Nout = 0
sock.settimeout(0.1)
for i in range(142):
    packet = []
    packet += header
    counter = [int(b) for b in bin(i)[2:].zfill(8)]
    packet += counter
    packet += btTx[:-4]
    packetTx = hexString(packet)
    print('.............' + str(cnt) + '.............')
    ts1 = time.time()
    sent = sock.sendto(packetTx.encode(), server_address)
    try:
        packetRx, server = sock.recvfrom(1024)
        ts2 = time.time()
        print('package bounced back latency: ' + str(int((ts2 - ts1) * 1e6)) + ' mu')
    except socket.timeout:
        Nout += 1
    
    latency.append((ts2 - ts1) * 1e3)
    print(packetTx)
    print(packetRx)
    btRx = bitStream(packetRx)
    cnt += 1
    time.sleep(0.1)

print('Number of timeout during transmission: >>', Nout)
sock.close()
print('socket closed')

fig = figure(1, figsize = (8, 6))
plot(latency)
grid(True)
fig.savefig('1', dpi = 300)

