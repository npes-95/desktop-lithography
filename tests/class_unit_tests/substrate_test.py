
import sys
sys.path.append('../../lib/')
from substrate import Substrate
import numpy 
import matplotlib.pyplot as plt
import math


# circle
circle = plt.Circle((0,0), 50, fill = False)

substrate = Substrate()

substrate.setBottomLeft(0,-50)
substrate.setTopRight(0,50)



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

ax.add_artist(circle)
ax.scatter(x_list,y_list)
plt.show()


# rectangle
rectangle = plt.Rectangle((-20,-10), 40, 20, fill = False)



substrate.setShape("Rectangle")
substrate.setBottomLeft(-20,-10)
substrate.setTopRight(20,10)

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
