import sys
sys.path.append("../../lib/helper")

from time import sleep
from LEDs import LED

ledInterface = LED()

for i in range(0,10):
	
	#ledInterface.setRedLED(0)
	ledInterface.setRedLED(1)
	sleep(2)
	
	ledInterface.setRedLED(0)
	#ledInterface.setRedLED(0)
	sleep(2)
	


