#Senior Design ECE 1896 Posture Watcher
#Gerald Kiliany

#Read input from Force Sensitive Resistors through ADC (MCP3008)


#import necessary libraries
import spidev
import time

#variables
samplePeriod = 0.5
FSR_channel = 0
SeatedThresh = 300 #threshold for pressure to consider a user to be seated (1024 range)

#SPI Comm setup
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000


def readadc(adcnum):
    #Read SPI data from ADC, 8 channels
    
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data


    while True:
        FSR_value = readADC(FSR_channel) #should be 0-1023 for 10 bit ADC
        
        
        #perform ops on data
        if FSR_value > seatedThresh:
            isSeated = True; 
        else:
            isSeated = False;
        #for testing
        print("Pressure Pad Value: %d" %pad_value)    
        print("Seated or not: %b" %isSeated)
        
        time.sleep(samplePeriod)
        
        #end