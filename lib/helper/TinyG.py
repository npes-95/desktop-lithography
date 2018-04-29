# HELPER CLASS FOR MOTOR DRIVER

import time;
import serial;
import io;
from PyQt5.QtCore import pyqtSignal, QObject

class MotorDriver(QObject):
    
    coordinatesChanged = pyqtSignal(float,float,float)

    def __init__(self):
        
        super().__init__()
        
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
       
        #print ("Serial configuration established: " + str(self.ser.isOpen()))
       
        self.textWrapper = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))
        
        # we want to be able to toggle whether the move to coordinates function blocks
        # when it blocks, it reduces the camera framerate, so we want it off when the user is using the camera
        self.blocking = False
        
        
        
        # init motors: set scale to mm, assign m1 = x, m2 = y, m3 = z, set lead screw pitch (0.9mm), set microsteps, set polarity, set power management (z motor always on to hold dmd in place), set max speed
        initGCode = "\nG21 \n$1ma=0 \n$2ma=1 \n$3ma=2 \n$1SA=0.9 \n$2SA=0.9 \n$3SA=0.9 \n$4SA=0.9 \n$1tr=8 \n$2tr=8 \n$3tr=8 \n$4tr=8 \n$1mi=8 \n$2mi=8 \n$3mi=8 \n$4mi=8 \n$1po=0 \n$2po=0 \n$3po=0 \n$4po=0 \n$3pm=2 \n$xvm=1000 \n$yvm=1000 \n$zvm=1000 \n$sv=0"
        
        self.textWrapper.write(initGCode)
        self.textWrapper.flush()
        
        print("Motor driver connected!")
        
        self.setCoordinates((0,0,0))
        
        # for some reeason doesn't respond to first command sent?
        self.moveToCoordinates()
        self.moveToCoordinates()
        
    def __del__(self):
        
        self.setCoordinates((0,0,0))
        self.moveToCoordinates()
        
        
        
    def setX(self, x):
        self.x = x
        
    def setY(self, y):
        self.y = y
        
    def setZ(self, z):
        self.z = z 
        
    def incrementX(self, increment):
        self.x += increment
        
    def incrementY(self, increment):
        self.y += increment    
        
    def incrementZ(self, increment):
        self.z += increment     
            
    def setCoordinates(self, coordinates):
        self.x, self.y, self.z = coordinates
        
    def getCurrentCoordinates(self):
        return (self.x,self.y,self.z)
        
    def moveToCoordinates(self):
        
        gcode = "G0 X" + str(self.x) + " Y" + str(self.y) + " Z" + str(self.z)
        self.writeGCodeLine(gcode)
        self.coordinatesChanged.emit(self.x,self.y,self.z)
        
        if self.blocking:
        
            while "Run" in self.getMachineStatus():
                time.sleep(1)
        
    def getMachineStatus(self):
        return(self.writeGCodeLine("$stat")[0])
        
        
    def writeGCodeLine(self, gcode):
        
        # write gcode line
        self.textWrapper.write(gcode + " \n")
        self.textWrapper.flush()
        
        # return answer sent from tiny (if performing a read request)
        return self.textWrapper.readlines()
        
    def block(self):
        self.blocking = True
       
    def unblock(self):
        self.blocking = False
        
        
