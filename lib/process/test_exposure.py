# class that holds the main exposure process
import numpy as np
from time import sleep
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

class TestExposure(QThread):
	
	progress = pyqtSignal(int)
	
	def __init__(self, DMD, LED, stage, substrate, minExposureTime, maxExposureTime, step):
		super().__init__()
		
		self.DMD = DMD
		self.LED = LED
		self.stage = stage
		self.substrate = substrate
		self.minExposureTime = minExposureTime
		self.maxExposureTime = maxExposureTime
		self.step = step
		
		self.cancelled = False
		
	def run(self):
		
		self.DMD.setTestPattern()
		
		coordinates = self.substrate.getPackingCoordinates()
		
		i = 0
		
		for exposureTime in np.linspace(self.minExposureTime, self.maxExposureTime, (self.maxExposureTime - self.minExposureTime)/self.step):
			
			if self.cancelled or i > len(coordinates):
				break
				
			x,y = coordinates[i]
			
			# set coordinates
			self.stage.setX(x)
			self.stage.setY(y)
			self.stage.moveToCoordinates()
			
			sleep(2)
			
			# expose substrate
			#self.LED.setUVLED(1)
			self.LED.setRedLED(1)
			
			# sleep for exposure time
			sleep(exposureTime)
			
			#self.LED.setUVLED(0)
			self.LED.setRedLED(0)
			
			i += 1
			
			self.progress.emit(int(100*i/((self.maxExposureTime - self.minExposureTime)/self.step)))
			
		self.stage.setX(0)
		self.stage.setY(0)
		self.stage.moveToCoordinates()
			
	def cancel(self):
		self.cancelled = True
			
		
		
