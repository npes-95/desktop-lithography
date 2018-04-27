# class that holds the main exposure process

from time import sleep
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

class MainExposure(QThread):
	
	progess = pyqtSignal(int)
	
	def __init__(self, DMD, LED, stage, photomask, substrate, exposureTime, iterations):
		super().__init__()
		
		self.DMD = DMD
		self.LED = LED
		self.stage = stage
		self.photomask = photomask
		self.substrate = substrate
		self.exposureTime = exposureTime
		self.iterations = iterations
		
		self.cancelled = False
		
	def run(self):
		
		
		# assuming here there is only one photomask file for now
		photomaskFiles = self.photomask.getFiles()
		
		self.DMD.setImage(photomaskFiles)
		
		coordinates = self.substrate.getPackingCoordinates()
		
		patternsExposed = 0
		
		for x,y in coordinates:
			
			if self.cancelled or patternsExposed > self.iterations:
				break
			
			# set coordinates
			self.stage.setX(x)
			self.stage.setY(y)
			self.stage.moveToCoordinates()
			
			# expose substrate
			#self.LED.setUVLED(1)
			self.LED.setRedLED(1)
			
			# sleep for exposure time
			sleep(self.exposureTime)
			
			#self.LED.setUVLED(0)
			self.LED.setRedLED(0)
			
			patternsExposed += 1
			
			self.progress.emit(int(100*patternsExposed/self.iterations))
			
		def cancel(self):
			self.cancelled = True
			
		
		
