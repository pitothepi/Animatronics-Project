import serial
import time
import socket

MSP_PORT = 'COM4'

def read_serial(port):
    time.sleep(.0005)
    start = time.time()
    val = []
    val += [port.read()]
    while val[-1] != b';':
        if time.time() > start + 1:
            raise IOError('Incorrect serial data.')
        val += [port.read()]
    end = val.index(b';')
    int_val = 0
    for i in range(0, end):
        int_val += int(val[i]) * 10 ** (end - (i + 1))
    port.flush()
    return int_val

port = serial.Serial(MSP_PORT, baudrate=9600, timeout=1)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('',1337))
time.sleep(5)
hzs = []
try:
    while 1:
        start = time.time()
        m = sock.recvfrom(1024)
        if m[0] == b'q':
            raise KeyboardInterrupt
        port.write(m[0])
        try:
            print(m[0].decode('utf-8') + '\t' + str(1/(time.time()-start)) + ' hz')      
        except ZeroDivisionError:
            print(m[0].decode('utf-8') + '\tfast hz')
finally:
    port.flush()
    port.close()
    sock.close()
    print('Serial closed.')
