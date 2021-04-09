#Senior Design ECE 1896 Posture Watcher
#Gerald Kiliany

#Timing to Determine if sitting for too long


import time

#Define variables
isSeated = True
samplePeriod = 1.0
seatCount = 0
standCount = 0
timeElapsed = 0
oversittingThresh = 5 #samples of sitting in a row that will generate alert for sitting too long
notsittingThresh = 2 #samples of input not sitting a row that will reset sitting time 


#main loop
while True:    
    timeElapsed+=1
    
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
    
    
    time.sleep(samplePeriod)

    
    