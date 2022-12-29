import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    line = ser.readline()
    line_str = line.decode('utf-8')
    print(line_str)
    time.sleep(.1)