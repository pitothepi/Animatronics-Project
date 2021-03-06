import RPi.GPIO as gpio
import serial
import time

MIN_PWM = 2
MAX_PWM = 14    #model RS001B servos seem to like this range
min_bend = 200
max_bend = 600

servo_pin = 21

port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)
port.flush()
bt = serial.Serial('/dev/rfcomm0', baudrate=115200, timeout=1)
bt.flush()


def wait_for_key():
    trash = input()
    del trash

def get_data(pin=0):
    port.write(str(pin).encode('utf-8'))
    time.sleep(.001)
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
    bt.flush()
    return int_val

def get_reading():
    start_time = time.time()
    readings = []
    while time.time() < start_time + .05:
        readings += [get_data()]
    avg = sum(readings) / len(readings)
    return int(avg + .5)

'''
print('Fully bend finger. Press Enter when ready.')
wait_for_key()
maxvals = []
start = time.time()
while time.time() < start + 1:
    maxvals += [get_data()]
max_bend = int(sum(maxvals) / len(maxvals) + .5)

print('Fully extend finger. Press Enter when ready.')
wait_for_key()
minvals = []
start = time.time()
while time.time() < start + 1:
    minvals += [get_data()]
min_bend = int(sum(minvals) / len(minvals) + .5)
print(max_bend)
print(min_bend)
'''
try:
    while True:
        #print(get_data())
        while bt.inWaiting() == 0:
            time.sleep(.01)
        pin = int(bt.read())
        data = get_data(pin)
        bt.write((str(data)+';').encode('utf-8'))
finally:
    bt.close()
    port.close()
    print('Serial cleanup successful.')
