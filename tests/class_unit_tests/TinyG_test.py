import sys
sys.path.append("../../lib/helper")

from TinyG import MotorDriver
from time import sleep

stage = MotorDriver()

print(stage.getMachineStatus())

stage.setCoordinates((0,0,0))
stage.moveToCoordinates()

sleep(1)

stage.setCoordinates((5,2,2))
stage.moveToCoordinates()

sleep(1)

stage.setCoordinates((0,0,0))
stage.moveToCoordinates()
