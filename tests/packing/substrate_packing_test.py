# demonstrate the packing of designs onto a circular substrate using a graphical drawing library

from graphics import *
from math import *

# assume all lengths are in mm (here they are pixels)

CIRCLE_RADIUS = 50
PHOTOMASK_WIDTH = 4
PHOTOMASK_LEN = 7
PHOTOMASK_DIAM = sqrt(PHOTOMASK_WIDTH**2 + PHOTOMASK_LEN**2)


def getGridPoints():

	numPoints = 2*CIRCLE_RADIUS//PHOTOMASK_WIDTH

	gridPoints = list()

	for i in range(-numPoints//2, numPoints//2):

		for j in range(-numPoints//2, numPoints//2):

			gridPoints.append((i*PHOTOMASK_WIDTH, j*PHOTOMASK_LEN))

	return gridPoints







win = GraphWin("Packing Demo", 1000, 700)

# substrate
c = Circle(Point(500,350), CIRCLE_RADIUS)
c.draw(win)

grid = getGridPoints()



for x,y in grid:

	#if sqrt((x+500 - 500)**2 + (y+350 - 350)**2) <= CIRCLE_RADIUS - PHOTOMASK_DIAM:
	if sqrt(x**2 + y**2) <= CIRCLE_RADIUS - PHOTOMASK_DIAM:
		p1 = Point(x+500 - PHOTOMASK_WIDTH//2,y+350 - PHOTOMASK_LEN//2)
		p2 = Point(x+500 + PHOTOMASK_WIDTH//2,y+350 + PHOTOMASK_LEN//2)

		rect = Rectangle(p1,p2)
		rect.draw(win)


win.getMouse() # Pause to view result
win.close()    # Close window when done