import RPi.GPIO as gpio
import serial
import time
import socket

port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)
port.flush()

def get_data(pin=0):
    port.write(str(pin).encode('utf-8'))
    time.sleep(.0005)
    start = time.time()
    val = []
    val += [port.read()]
    while val[0] == b'\x00':
        port.flush()
        val = []
        val += [port.read()]
    while val[-1] != b'\n':
        if time.time() > start + 1:
            raise IOError('Incorrect serial data.')
        val += [port.read()]
    end = val.index(b'\r')
    int_val = 0
    for i in range(0, end):
        int_val += int(val[i]) * 10 ** (end - (i + 1))
    return int_val

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  #John 11:35

try:
    while True:
        for pin in range(0,5):
            data = int(get_data(pin) / 10) * 10 + pin
            print(data)
            sock.sendto((str(data) + ';').encode('utf-8'), ('255.255.255.255', 1337))
            time.sleep(.002)
finally:
    sock.sendto('q'.encode('utf-8'), ('255.255.255.255', 1337))
    sock.close()
    port.close()
    print('Serial cleanup successful.')