#Senior Design ECE 1896 Posture Watcher
#Gerald Kiliany

#Read input from Force Sensitive Resistors through ADC (MCP3008)
#Determine if seated
#Send sensor readings

#import necessary libraries
import spidev
import time
import sys
import RPi.GPIO as GPIO
import csv
from subprocess import call #used in sleep shutdown


#variables


#Sensor Inputs Variables


#Vibration Mode Variables

vibMode = True #change from user 
vibPinOut1 = 7
vibPinOut2 = 25

#Seat/Posture Timing Variables
samplePeriod = 1


#checkSitting() Variables
oversittingThresh = 5 #can be updated from user
badPosThresh = 5 #can be updated from user



#Bluetooth Variables 
connectTime = 2
bluetoothOn = False




#Control Variables
#all updated each call of checkSitting()
currSeated = False
stood = False
badPos = False
seatedMins = 0
badPosMins = 0
sleepTimer = 0
sleepThresh = 10000 #can be updated from User


#Setup
#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(vibPinIn, GPIO.IN)
GPIO.setup(vibPinOut, GPIO.OUT)


#SPI Comm setup
mcp0 = spidev.SpiDev()
mcp0.open(0,0) #open communication between spi bus 0 and mcp device on channel 0
mcp0.max_speed_hz = 1000000



#Functions
def readADC(adcnum):
    #Read SPI data from ADC, 8 channels
    if adcnum > 7 or adcnum < 0:
        return -1
   # mcp0.open(0,0)
   # mcp0.max_speed_hz = 1000000
    
    r = mcp0.xfer2([1, (8 + adcnum) << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    
    
    
    #spi.close()
    return data



#Control loop

#while True
if True: #run through once for testing
    lastTime = time.time()
    now = lastTime;
    #read user settings from bluetooth
    while((now - lastTime) < connectTime) and not bluetoothOn: 
        now = time.time()
       # print('Checking Bluetooth')
       
       
    if not stood:
        seatedMins+=1
        
    if badPos:
        badPosMins+=1
    
    if not currSeated:
        sleepTimer+=1
        if sleepTimer > sleepThresh:
            
            call("sudo nohup shutdown -h now", shell=True) #shutdown Pi to save power
            
       
       
    #Try connecting to bluetooth
    #print('Trying to establish bluetooth connection')
    
    if bluetoothOn:
        #settings from user
        from blueConfig import * #import variable values from bluetooth settings #settings in blueConfig.py #currently have blueconfig.txt
        print('Bluetooth Online')
        #checkSitting(params)
    else :
        print('Bluetooth Offline, using default settings and vibration mode')
        #checkSitting(defaults)
        
mcp0.close() #end comms with mcp device
        
        
def checkSitting():
    while timeElapsed < 60: #for debugging don't run forever
        timeElapsed+=1
       
        

        
        FSR_value0 = readADC(0) #0-1023 for 10 bit ADC, sensor 0
        FSR_value1 = readADC(1) #sensor 1
        FSR_value2 = readADC(2) #sensor 2
        FSR_value3 = readADC(3) #sensor 3
        FSR_value4 = readADC(4) #sensor 4
        #FSR_value5 = readADC(5) #sensor 5
        #FSR_value6 = readADC(6) #sensor 6
        #FSR_value7 = readADC(7) #sensor 7
        #adc = MCP3008()
        #FSR_value0 = adc.read(channel = 0)
        #FSR_value1 = adc.read(channel = 1)
        
        #perform ops on data
        if ((FSR_value0 > seatedThresh) | (FSR_value1 > seatedThresh) | (FSR_value2 > seatedThresh) | (FSR_value3 > seatedThresh)):
            isSeated = True; 
        else:
            isSeated = False;
        #for testing
            
        if isSeated:
            seatCount +=1 #increment time spent seated
            standCount = 0 #reset counter for standing
        else :
            standCount+=1
            if standCount >= notSittingThresh: #sense standing, reset seated count
                seatCount = 0
        
        print("Time elapsed: ", timeElapsed)
        print("FSR0 value: ", FSR_value0)
        print("FSR1 value: ", FSR_value1)
        print("FSR2 value: ", FSR_value2)
        print("FSR3 value: ", FSR_value3)
        print("FSR4 value: ", FSR_value4)
        print("Seated or not: ", isSeated)
        
        if (seatCount >= oversittingThresh) & ((seatCount % oversittingThresh) == 0) & (standCount < 1): #compare time sitting to the threshold considered to be too long
            if(vibMode) :
                print("Vibration Mode: Vibrating")
                GPIO.output(vibPinOut1, GPIO.HIGH)
                GPIO.output(vibPinOut2, GPIO.HIGH)
            else:
                print("Seated too long")
               # Send to bluetooth connected device, seated or not,

               
               # print("Pressure Pad Value: ", FSR_value0)    
               # print("Seated or not: ", isSeated)
        
        #Write to file seated pressure values
        if(isSeated) :
            
            currValues = [FSR_value0, FSR_value1, FSR_value2, FSR_value3, FSR_value4] 
            with open('mlData.csv', 'a') as csvfile:
                outWriter = csv.writer(csvfile, delimiter = ' ')
                outWriter.writerow(currValues)
            
        time.sleep(samplePeriod)
        GPIO.output(vibPinOut, GPIO.LOW)
    
    
    



#at end write default settings to bluetooth settings file 

