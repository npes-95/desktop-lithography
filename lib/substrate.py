# CLASS TO HOLD SOFTWARE REPRESENTATION OF SUBSTRATE
# diameters and coordinates are in mm

from math import *

class Substrate():

	def __init__(self):
		self.shape = "Circle"
		self.diameter = 100

		self.photomaskWidth = 6.5718
		self.photomaskLength = 3.699
		self.photomaskDiameter = sqrt(self.photomaskWidth**2 + self.photomaskLength**2)



	def setShape(self, shape):
		self.shape = shape

	def setDiameter(self, diameter):
		self.diameter = diameter

	def getPackingCoordinates(self):

		if self.shape = "Circle":
			return self.getCirclePackingCoordinates()

		else:
			return self.getRectanglePackingCoordinates()

	def getCirclePackingCoordinates(self):

		numPoints = self.diameter//self.photomaskWidth

		coordinates = list()

		for i in range(-numPoints//2, numPoints//2):

			for j in range(-numPoints//2, numPoints//2):

				x = i*self.photomaskWidth
				y = j*self.photomaskLength

				if sqrt(x**2 + y**2) <= self.diameter/2 - self.photomaskDiameter/2

					coordinates.append((x, y))

		return coordinates

	def getRectanglePackingCoordinates(self):

		numPoints = floor(self.diameter/self.photomaskDiameter)

		coordinates = list()

		for i in range(-numPoints//2, numPoints//2):

			for j in range(-numPoints//2, numPoints//2):

				x = i*self.photomaskWidth
				y = j*self.photomaskLength

				coordinates.append((x, y))

		return coordinates





