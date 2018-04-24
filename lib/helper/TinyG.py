# HELPER CLASS FOR MOTOR DRIVER

import time;
import serial;
import io;

class MotorDriver():

    def __init__(self):
        
        # init serial port
        self.ser = serial.Serial(
              
               port='/dev/ttyUSB0',
               baudrate = 115200,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               xonxoff = True,
               timeout=1
           )
       
        print ("Serial configuration established: " + str(self.ser.isOpen()))
       
        self.textWrapper = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))
        
        self.x = 0
        self.y = 0
        self.z = 0
       
    def __del__(self):
        self.ser.close()
        
    def setX(self, x):
		self.x = x
		
    def setY(self, y):
		self.y = y
		
	def setZ(self, z):
		self.z = z
		
	def moveToCoordinates(self):
		
		gcode = "G1 f400 X" + str(self.x)
		self.writeGCodeLine(gcode)
		
		gcode = "G1 f400 Y" + str(self.y)
		self.writeGCodeLine(gcode)
		
		gcode = "G1 f400 Z" + str(self.z)
		self.writeGCodeLine(gcode)
		
        
    def writeGCodeLine(self, gcode):
        
        # write gcode line
        self.textWrapper.write(gcode + " \n")
        self.textWrapper.flush()
        
        # return answer sent from tiny (if performing a read request)
        return self.textWrapper.readline()
        
        
