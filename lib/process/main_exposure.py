# class that holds the main exposure process

from time import sleep
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

class MainExposure(QThread):
    
    progress = pyqtSignal(int)
    
    def __init__(self, DMD, LED, stage, photomask, substrate, exposureTime, iterations):
        super().__init__()
        
        self.DMD = DMD
        self.LED = LED
        self.stage = stage
        self.photomask = photomask
        self.substrate = substrate
        self.exposureTime = exposureTime
        self.iterations = iterations
        
        
        
    def run(self):
        
        self.cancelled = False
        
        # get photomask files        
        photomaskFiles = self.photomask.getFiles()
        
        self.substrate.setDeviceWidth(self.photomask.getPhotomaskWidth())
        self.substrate.setDeviceHeight(self.photomask.getPhotomaskHeight())
        
        coordinates = self.substrate.getPackingCoordinates()
        
        patternsExposed = 0
        
        frameOffset = self.photomask.getPhotomaskFrameOffset()
        
        for x,y in coordinates:
            
            if self.cancelled or patternsExposed > self.iterations:
                break
            
            i = 0   
            
            for dmdFrame in photomaskFiles:
                
                self.DMD.setImage(dmdFrame)
                
                x_offset, y_offset = frameOffset[i]
            
                # set coordinates
                self.stage.setX(x+x_offset)
                self.stage.setY(y+y_offset)
                self.stage.moveToCoordinates()
            
                # expose substrate
                #self.LED.setUVLED(1)
                self.LED.setRedLED(1)
            
                # sleep for exposure time
                sleep(self.exposureTime)
            
                #self.LED.setUVLED(0)
                self.LED.setRedLED(0)
            
                patternsExposed += 1
                i += 1
                
                self.progress.emit(int(100*patternsExposed/self.iterations))
            
            
        # reset coordinates
        self.stage.setX(0)
        self.stage.setY(0)
        self.stage.moveToCoordinates()
        
            
    def cancel(self):
        self.cancelled = True
            
        
        
