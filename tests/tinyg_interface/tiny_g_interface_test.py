#!/usr/bin/python
import time;
import serial;
import io;
          
      
ser = serial.Serial(
              
               port='/dev/ttyUSB0',
               baudrate = 115200,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               xonxoff = True,
               timeout=1
           )

print ("Serial configuration is established: " + str(ser.isOpen()))
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
with open ('/home/pi/Desktop/G_Code') as f:
    for line in f:
        sio.write(unicode('%s \n' %line))
        sio.flush()
        
x = sio.readline()
print x