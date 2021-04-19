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


#Google Cloud variables
project_id = 'smart-chair-307219'
compute_region = 'us-central1'
model_display_name = 'BigData_20210418125437'
from google.cloud import automl_v1beta1 as automl
from google.oauth2 import service_account
inputs = {0,1,2,3,4,5,6,7}
client = automl.TablesClient( credentials=service_account.Credentials.from_service_account_file("/home/pi/Desktop/smart-chair-307219-34ce5caf904d.json"), project=project_id, region=compute_region)

#Sensor Inputs Variables


#Vibration Mode Variables

vibMode = True #change from user 
vibPinOut1 = 7
vibPinOut2 = 25

#Seat/Posture Timing Variables
samplePeriod = 10


#checkSitting() Variables
oversittingThresh = 5 #can be updated from user
badPosThresh = 5 #can be updated from user
seatedThresh = 30 #pressure value that is considered seated
notSittingThresh = 2 #time standing to mark user as having stood


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
timeElapsed = 0


#Setup
#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(vibPinOut1, GPIO.OUT)
GPIO.setup(vibPinOut2, GPIO.OUT)

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



        
def checkSitting():

    #Local variables
    standCount = 0
    timeElapsed = 0
    seatCount = 0
    
    while timeElapsed < 60: #for debugging don't run forever
        timeElapsed+=1
       
        

        
        FSR_value0 = readADC(0) #0-1023 for 10 bit ADC, sensor 0
        FSR_value1 = readADC(1) #sensor 1
        FSR_value2 = readADC(2) #sensor 2
        FSR_value3 = readADC(3) #sensor 3
        FSR_value4 = readADC(4) #sensor 4
        FSR_value5 = readADC(5) #sensor 5
        FSR_value6 = readADC(6) #sensor 6
        FSR_value7 = readADC(7) #sensor 7
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
        print("FSR5 value: ", FSR_value5)
        print("FSR6 value: ", FSR_value6)
        print("FSR7 value: ", FSR_value7)
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
            
            currValues = [FSR_value0, FSR_value1, FSR_value2, FSR_value3, FSR_value4, FSR_value5, FSR_value6, FSR_value7] 
            
            #GOOGLE CLOUD BS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            response = client.predict(model_display_name=model_display_name, inputs=currValues)
            currClass=8;
            currScore=0.0001;
            for result in response.payload:
                if (float(result.tables.score) > currScore):
                    currScore = float(result.tables.score)
                    currClass= int(result.tables.value)
                #print(currScore)
                #print(result.tables.score)
                print("Predicted class name: {}".format(result.tables.value))
                print("Predicted class score: {}".format(result.tables.score))
            print("Predicted Class: {}".format(str(currClass)))
            print("Confidence: {}".format(currScore))
            if (currClass==8):
                print("something fucked up")

            with open('mlData.csv', 'a') as csvfile:
                outWriter = csv.writer(csvfile, delimiter = ' ')
                outWriter.writerow(currValues)
            
        time.sleep(samplePeriod)
        #turn of vibration motors
        GPIO.output(vibPinOut1, GPIO.LOW)
        GPIO.output(vibPinOut2, GPIO.LOW)
    
    

    return True


#Control loop

#while True
while True: #run through once for testing
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
            
            call("sudo shutdown -h now", shell=True) #shutdown Pi to save power
            
       
       
    #Try connecting to bluetooth
    #print('Trying to establish bluetooth connection')
    
    
        #Check for settings from user
    from blueConfig import * #import variable values from bluetooth settings #settings in blueConfig.py #currently have blueconfig.txt
    if bluetoothOn:    
        print('Bluetooth Online')
        checkSitting()
    else :
        print('Bluetooth Offline, using default settings and vibration mode')
        checkSitting()
        
mcp0.close() #end comms with mcp device
    

#at end write default settings to bluetooth settings file 
blueDefaults = open("blueConfig.py", "w")
blueDefaults.write("bluetoothOn = False")