# CLASS TO HOLD SOFTWARE REPRESENTATION OF SUBSTRATE
# diameters and coordinates are in mm

from math import *

class Substrate():

    def __init__(self):
        self.shape = "Circle"

        self.photomaskWidth = 6.5718
        self.photomaskHeight = 3.699 
        self.photomaskDiameter = sqrt(self.photomaskWidth**2 + self.photomaskHeight**2)
        
        self.bottomLeft = (-10,-10)
        self.topRight = (10,10)


    def setShape(self, shape):
        self.shape = shape
        
    def setBottomLeft(self, x, y):
        self.bottomLeft = (x,y)
        
    def setTopRight(self, x, y):
        self.topRight = (x,y)
        

    def getPackingCoordinates(self):

        if self.shape == "Circle":
            return self.getCirclePackingCoordinates()

        else:
            return self.getRectanglePackingCoordinates()

    def getCirclePackingCoordinates(self):
        
        x1,y1 = self.bottomLeft
        x2,y2 = self.topRight
        
        circleDiam = sqrt((x2-x1)**2 + (y2-y1)**2)

        numPoints = floor(circleDiam/self.photomaskHeight)
        
        # get centre offset
        centreOffsetX = (x1 + x2)/2
        centreOffsetY = (y1 + y2)/2
        

        coordinates = list()

        for i in range(-numPoints//2, numPoints//2):

            for j in range(-numPoints//2, numPoints//2):

                x = i*self.photomaskWidth
                y = j*self.photomaskHeight

                if sqrt(x**2 + y**2) <= circleDiam/2 - self.photomaskDiameter/2:

                    coordinates.append((x+centreOffsetX, y+centreOffsetY))

        return coordinates

    def getRectanglePackingCoordinates(self):
        
        x1,y1 = self.bottomLeft
        x2,y2 = self.topRight
        
        numPointsWidth = floor((x2-x1)/self.photomaskWidth)
        numPointsHeight = floor((y2-y1)/self.photomaskHeight)


        coordinates = list()
        
        # compensate for the fact that the points calculated are not calculated with the centre of the rectangle
        offsetWidth = 0
        offsetHeight = 0
        
        # get centre offset
        centreOffsetX = (x1 + x2)/2
        centreOffsetY = (y1 + y2)/2
        
        if (numPointsWidth%2 == 0):
            offsetWidth = self.photomaskWidth/2
        else:
            offsetWidth = self.photomaskWidth
            
        if (numPointsHeight%2 == 0):
            offsetHeight = self.photomaskHeight/2
        else:
            offsetHeight = self.photomaskHeight
            

        for i in range(-numPointsWidth//2, numPointsWidth//2):

            for j in range(-numPointsHeight//2, numPointsHeight//2):

                x = i*self.photomaskWidth + offsetWidth + centreOffsetX
                y = j*self.photomaskHeight + offsetHeight + centreOffsetY

                coordinates.append((x, y))

        return coordinates





