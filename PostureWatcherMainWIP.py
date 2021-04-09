#Senior Design ECE 1896 Posture Watcher
#Gerald Kiliany

#Read input from Force Sensitive Resistors through ADC (MCP3008)
#Determine if seated
#Send sensor readings

#import necessary libraries
#import spidev
import time
#import sys
#import RPi.GPIO as GPIO
#import csv
#from subprocess import call #used in sleep shutdown


#variables


#Sensor Inputs Variables


#Vibration Mode Variables



#Seat/Posture Timing Variables

#checkSitting() Variables

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
            
       
       
       
    if bluetoothOn:
        #settings from user
        print('Bluetooth Online')
        #checkSitting(params)
    else :
        print('Bluetooth Offline, using default settings and vibration mode')
        #checkSitting(defaults)
