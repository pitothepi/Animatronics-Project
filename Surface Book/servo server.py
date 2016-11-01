import serial
import time

MSP_PORT = 'COM4'
BT_PORT = 'COM10'

def read_serial(port):
    time.sleep(.005)
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
bt = serial.Serial(BT_PORT, baudrate=115200, timeout=1)
time.sleep(5)
hzs = []
try:
    while 1:
        start = time.time()
        bt.write('0'.encode('utf-8'))
        #data = port.read(port.in_waiting)
        #data = read_serial(bt)
        try:
            data = read_serial(bt)
        except IOError:
            print('bad data')
            continue
        port.write((str(data) + ';').encode('utf-8'))
        #time.sleep(.5)
        #print(port.read(port.in_waiting))
        print(str(data) + '\t at ' + str(1/(time.time()-start)) + ' hz')      
        
finally:
    port.flush()
    port.close()
    print('Serial closed.')
