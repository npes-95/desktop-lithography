
import sys
sys.path.append('../../lib/helper')
from substrate import Substrate
import numpy 
import matplotlib.pyplot as plt
import math


# circle
circle = plt.Circle((10,5), 50, fill = False)

substrate = Substrate()

substrate.setDeviceWidth(3)
substrate.setDeviceHeight(2)

substrate.setBottomLeft(10,-45)
substrate.setTopRight(10,55)



coordinates = substrate.getPackingCoordinates()

x_list = numpy.empty(len(coordinates))
y_list = numpy.empty(len(coordinates))



i = 0

for x,y in coordinates:
	
	x_list[i] = x
	y_list[i] = y
	i+=1
	




fig, ax = plt.subplots()
ax.set_xlim((-70,70))
ax.set_ylim((-70,70))

ax.add_artist(circle)
ax.scatter(x_list,y_list)
plt.show()


# rectangle
rectangle = plt.Rectangle((-10,0), 40, 20, fill = False)



substrate.setShape("Rectangle")
substrate.setBottomLeft(-10,0)
substrate.setTopRight(30,20)

substrate.setDeviceWidth(2)

coordinates = substrate.getPackingCoordinates()

x_list = numpy.empty(len(coordinates))
y_list = numpy.empty(len(coordinates))

i = 0

for x,y in coordinates:
	
	x_list[i] = x
	y_list[i] = y
	i+=1



fig, ax = plt.subplots()
ax.set_xlim((-50,50))
ax.set_ylim((-50,50))

ax.add_artist(rectangle)
ax.scatter(x_list,y_list)
plt.show()
