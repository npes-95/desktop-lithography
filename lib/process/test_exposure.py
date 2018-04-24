# class that holds the main exposure process

from time import sleep
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

class MainExposure(QThread):
	
	progess = pyqtSignal(float)
	
	def __init__(self, DMD, LED, stage, photomask, substrate, minExposureTime, maxExposureTime, step):
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
		
		# assuming here there is only one photomask file for now
		photomaskFiles = self.photomask.getFiles()
		
		self.DMD.setTestPattern()
		
		coordinates = self.substrate.getPackingCoordinates()
		
		i = 0
		
		for exposureTime in range(self.minExposureTime, self.maxExposureTime, self.step):
			
			if self.cancelled or i > len(coordinates):
				break
				
			x,y = coordinates[i]
			
			# set coordinates
			self.stage.setX(x)
			self.stage.setY(y)
			self.stage.moveToCoordinates()
			
			# expose substrate
			self.LED.setUVLED(1)
			
			# sleep for exposure time
			sleep(exposureTime)
			
			self.LED.setUVLED(0)
			
			i += 1
			
			self.progress.emit(i/((self.maxExposureTime - self.minExposureTime)/self.step))
			
		def cancel(self):
			self.cancelled = True
			
		
		
