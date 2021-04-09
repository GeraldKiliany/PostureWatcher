#Senior Design ECE 1896 Posture Watcher
#Gerald Kiliany

#Read the input from the Wheatstone bridge sensor and timing


 
#import libraries
import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711 


#Declare variables
refUnit = -100 #will need to set manually when in possession of sensor
hx = HX711(5,6)
isSeated = False #keep track if user seated or not
seatedThreshHx = 100 #sensor value that will be interpreted as seater person present
samplePeriod = 1 #time between signal samples
seatCount = 0
standCount = 0
timeElapsed = 0
oversittingThresh = 5 #samples of sitting in a row that will generate alert for sitting too long
notsittingThresh = 2 #samples of input not sitting a row that will reset sitting time 



#setup
hx.set_reading_format("MSB","MSB") #from datasheet read in MSB order
hx.set_reference_unit(refUnit)
hx.reset()
hx.tare()
print("Setup complete")





#Main loop

while True:
    timeElapsed+=1
    
    #Read input
    pressureVal = hx.get_weight(5)
    print(pressureVal)#for debugging
    
    
    #Determine if seated
    if pressureVal > seatedThreshHx:
        isSeated = True
    else:
        isSeated = False
    
    
    if isSeated:
        seatCount +=1 #increment time spent seated
        standCount = 0 #reset counter for standing
    else :
        standCount+=1
        if standCount == notsittingThresh: #sense standing, reset seated count
            seatCount = 0
    
    print("Time elapsed: ", timeElapsed) 
    
    if (seatCount >= oversittingThresh) & ((seatCount % oversittingThresh) == 0): #compare time sitting to the threshold considered to be too long
        print("Seated too long")
    

    
    #prepare to read input again
    hx.power_down()
    hx.power_up()
    time.sleep(samplePeriod)
    
    #EOF
