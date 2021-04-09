#Senior Design ECE 1896 Posture Watcher
#Gerald Kiliany

#Read the input from the Wheatstone bridge sensor


 
#import libraries
import time
import sys
import RPI.GPIO as GPIO
from hx711 import HX711 


#Declare variables
refUnit = 1 #will need to set manually when in possession of sensor
hx = HX711(5,6)
isSeated = False #keep track if user seated or not
seatedThreshHx = 100 #sensor value that will be interpreted as seater person present
samplePeriod = 1 #time between signal samples

#setup
hx.set_reading_format("MSB","MSB") #from datasheet read in MSB order
hx.set_reference_unit(refUnit)
hx.reset()
hx.tare()
print("Setup complete")





#Main loop

while True:
    
    #Read input
    pressureVal = hx.get_weight(5)
    print(pressureVal)#for debugging
    
    
    #Determine if seated
    if pressureVal > seatedThreshHx:
        isSeated = True
    else:
        isSeated = False
    
    #prepare to read input again
    hx.power_down()
    hx.power_up()
    time.sleep(samplePeriod)
    
    #EOF