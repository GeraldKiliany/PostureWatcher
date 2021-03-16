#Senior Design ECE 1896 Posture Watcher
#Gerald Kiliany

#Read the input for vibration mode and output vibration

import sys
import time
import RPi.GPIO as GPIO


#Define variables
isSeated = True
samplePeriod = 1.0
seatCount = 0
standCount = 0
timeElapsed = 0
oversittingThresh = 5 #samples of sitting in a row that will generate alert for sitting too long
notsittingThresh = 2 #samples of input not sitting a row that will reset sitting time 
vibMode = False
vibrating = False
vibPinIn = 17 #GPIO pin to read vibration mode input
vibPinOut = 26 #GPIO pin for vibration motor

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(vibPinIn, GPIO.IN)
GPIO.setup(vibPinOut, GPIO.OUT)


#main loop
while True:    
    timeElapsed+=1
    
    vibMode = GPIO.input(17) #read pin 17 for if vibration switch on or off
    
    
    if isSeated:
        seatCount +=1 #increment time spent seated
        standCount = 0 #reset counter for standing
    else :
        standCount+=1
        if standCount == notsittingThresh: #sense standing, reset seated count
            seatCount = 0
    
    print("Time elapsed: ", timeElapsed) 
    
    if (seatCount >= oversittingThresh) & ((seatCount % oversittingThresh) == 0): #compare time sitting to the threshold considered to be too long
        if(vibMode) :
            print("Vibration Mode: Vibrating")
            GPIO.output(vibPinOut, GPIO.HIGH)
        else:
             print("Seated too long")
    
    time.sleep(samplePeriod)
    GPIO.output(vibPinOut, GPIO.LOW)
    
    
