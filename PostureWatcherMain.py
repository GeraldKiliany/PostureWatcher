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

#variables
samplePeriod = 1
FSR_channel0 = 0
FSR_channel1 = 1
FSR_channel2 = 2
FSR_channel3 = 3
FSR_channel4 = 4
seatedThresh = 30 #threshold for pressure to consider a user to be seated (1024 range)
timeElapsed = 0
vibMode = False
vibrating = False
vibPinIn = 17 #GPIO pin to read vibration mode input
vibPinOut = 7 #GPIO pin for vibration motor #7 on pcb, used to be 26
seatCount = 0
oversittingThresh = 5
notSittingThresh = 2
standCount = 0

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(vibPinIn, GPIO.IN)
GPIO.setup(vibPinOut, GPIO.OUT)


#SPI Comm setup
mcp0 = spidev.SpiDev()
mcp0.open(0,0) #open communication between spi bus 0 and mcp device on channel 0
mcp0.max_speed_hz = 1000000


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


while timeElapsed < 5069: #for debugging don't run forever
        timeElapsed+=1
       
        vibMode = GPIO.input(17) #read pin 17 for if vibration switch on or off
        

        
        FSR_value0 = readADC(FSR_channel0) #0-1023 for 10 bit ADC, sensor 0
        FSR_value1 = readADC(FSR_channel1) #sensor 1
        FSR_value2 = readADC(FSR_channel2) #sensor 2
        FSR_value3 = readADC(FSR_channel3) #sensor 3
        FSR_value4 = readADC(FSR_channel4) #sensor 4
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
                GPIO.output(vibPinOut, GPIO.HIGH)
            else:
                print("Seated too long")
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
        #end
mcp0.close() #end comms with mcp device
#shut down raspberry pi
