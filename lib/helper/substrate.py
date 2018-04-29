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
        
        
        self.deviceWidth = self.photomaskWidth
        self.deviceHeight = self.photomaskHeight


    def setShape(self, shape):
        self.shape = shape
        
    def setBottomLeft(self, x, y):
        self.bottomLeft = (x,y)
        
    def setTopRight(self, x, y):
        self.topRight = (x,y)
    
    def setDeviceWidth(self, width):
        # input to this function is the device width as the number of DMD frames it takes to represent it
        self.deviceWidth = self.photomaskWidth*width
        
    def setDeviceHeight(self, height):
        self.deviceHeight = self.photomaskHeight*height
        

    def getPackingCoordinates(self):

        if self.shape == "Circle":
            return self.getCirclePackingCoordinates()

        else:
            return self.getRectanglePackingCoordinates()

    def getCirclePackingCoordinates(self):
        
        x1,y1 = self.bottomLeft
        x2,y2 = self.topRight
        
        circleDiam = sqrt((x2-x1)**2 + (y2-y1)**2)

        numPoints = floor(circleDiam/self.deviceHeight)
        
        # device diameter
        deviceDiameter = sqrt(self.deviceWidth**2 + self.deviceHeight**2)
        
        # get centre offset
        centreOffsetX = (x1 + x2)/2
        centreOffsetY = (y1 + y2)/2
        

        coordinates = list()

        for i in range(-numPoints//2, numPoints//2):

            for j in range(-numPoints//2, numPoints//2):
                
                # coordinates for centre of device
                x = i*self.deviceWidth
                y = j*self.deviceHeight

                if sqrt(x**2 + y**2) <= circleDiam/2 - deviceDiameter/2:
                    
                    # coordinates for first DMD frame of device (use an offset based on this point to print all of the device)
                    x = x - (self.deviceWidth/2) + (self.photomaskWidth/2)
                    y = y + (self.deviceHeight/2) - (self.photomaskHeight/2)

                    coordinates.append((x+centreOffsetX, y+centreOffsetY))

        return coordinates

    def getRectanglePackingCoordinates(self):
        
        x1,y1 = self.bottomLeft
        x2,y2 = self.topRight
        
        numPointsWidth = floor((x2-x1)/self.deviceWidth)
        numPointsHeight = floor((y2-y1)/self.deviceHeight)


        coordinates = list()
        
        # compensate for the fact that the points calculated are not calculated with the centre of the rectangle
        offsetWidth = 0
        offsetHeight = 0
        
        # get centre offset
        centreOffsetX = (x1 + x2)/2
        centreOffsetY = (y1 + y2)/2
        
        if (numPointsWidth%2 == 0):
            offsetWidth = self.deviceWidth/2
        else:
            offsetWidth = self.deviceWidth
            
        if (numPointsHeight%2 == 0):
            offsetHeight = self.deviceHeight/2
        else:
            offsetHeight = self.deviceHeight
            

        for i in range(-numPointsWidth//2, numPointsWidth//2):

            for j in range(-numPointsHeight//2, numPointsHeight//2):
                
                # coordinates for centre of device
                x = i*self.deviceWidth + offsetWidth + centreOffsetX
                y = j*self.deviceHeight + offsetHeight + centreOffsetY
                
                # coordinates for first DMD frame of device
                x = x - (self.deviceWidth/2) + (self.photomaskWidth/2)
                y = y + (self.deviceHeight/2) - (self.photomaskHeight/2)

                coordinates.append((x, y))

        return coordinates





