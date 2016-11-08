import RPi.GPIO as gpio
import serial
import time
import socket

#http://stackoverflow.com/questions/22878625/receiving-broadcast-packets-in-python
MIN_PWM = 2
MAX_PWM = 14    #model RS001B servos seem to like this range
min_bend = 200
max_bend = 600

servo_pin = 21

port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)
port.flush()

def wait_for_key():
    trash = input()
    del trash

def get_data(pin=0):
    port.write(str(pin).encode('utf-8'))
    time.sleep(.0005)
    start = time.time()
    #while port.peek() == b'\x00':
    #    port.flush()
    val = []
    val += [port.read()]
    while val[0] == b'\x00':
        port.flush()
        val = []
        val += [port.read()]
    while val[-1] != b'\n':
        print(val)
        if time.time() > start + 1:
            raise IOError('Incorrect serial data.')
        val += [port.read()]
    end = val.index(b'\r')
    int_val = 0
    for i in range(0, end):
        int_val += int(val[i]) * 10 ** (end - (i + 1))
    return int_val

def get_reading():
    start_time = time.time()
    readings = []
    while time.time() < start_time + .05:
        readings += [get_data()]
    avg = sum(readings) / len(readings)
    return int(avg + .5)

sock = socket.socket(AF_INET, SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

try:
    while True:
        for pin in range(0,5):
            data = int(get_data(pin) / 10) + pin
            sock.sendto(str(data).encode('utf-8'), ('255.255.255.255', 1337))
            time.sleep(.001)
finally:
    sock.sendto('q'.encode('utf-8'), ('255.255.255.255', 1337))
    sock.close()
    port.close()
    print('Serial cleanup successful.')
