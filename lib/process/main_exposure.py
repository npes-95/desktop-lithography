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
		
		# assuming here there is only one photomask file for now
		photomaskFiles = self.photomask.getFiles()
		
		self.DMD.setImage(photomaskFiles[0])
		
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
			
			
		# reset coordinates
		self.stage.setX(0)
		self.stage.setY(0)
		self.stage.moveToCoordinates()
		
			
	def cancel(self):
		self.cancelled = True
			
		
		
