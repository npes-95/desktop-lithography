# HELPER CLASS FOR LED CONNECTION

import RPi.GPIO as GPIO

class LED():
    
    def __init__(self):
        
        GPIO.setwarnings(False)
        
        # set board mode to broadcom
        GPIO.setmode(GPIO.BCM)
        
        # init LED pins(nb: need to define pins here)
        self.redLEDPin = 17
        self.uvLEDPin = 18
        
        
        GPIO.setup(self.redLEDPin, GPIO.OUT)
        GPIO.setup(self.uvLEDPin, GPIO.OUT)
        
        print("LEDs connected!")
        
    def __del__(self):
        self.setRedLED(0)
        self.setUVLED(0)
        
    def setRedLED(self, state):
        GPIO.output(self.redLEDPin, state)
        
    def setUVLED(self, state):
        GPIO.output(self.uvLEDPin, state)
        
