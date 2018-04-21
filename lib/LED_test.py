from time import sleep
from LEDs import LED

ledInterface = LED()

for i in range(0,10):
	
	ledInterface.setRedLED(0)
	ledInterface.setRedLED(1)
	sleep(1)
	
	ledInterface.setRedLED(1)
	ledInterface.setRedLED(0)
	sleep(1)
	


