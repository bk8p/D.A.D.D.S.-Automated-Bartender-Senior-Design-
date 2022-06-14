#Here we import each libraries to the file to be used within the project
import busio 
import digitalio
import board
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import adafruit_mcp3xxx.mcp3008 as MCP
from R0 import r0
from analog_in import AnalogIn
import statistics 



#Initialize BAC list 
baclist= []
'''
#Gets input from the MCP3008 connecting to 'board'
#board is a type of pinning for the raspberry pi, It is the classic printed numbering on the board
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

#Initialize R0(clean air) sample list 
number_list=[]


#Initialize i fro the while loop
i=0

#takes 10001 samples for getting higher accuracey of R0
while (i != 10000):
    #Takes voltage samples of clean air up to 3.3V
    sensorR0Samples= float((AnalogIn(mcp, MCP.P0)).voltage)
    #adds(appends) this voltage to a list
    addtolist= number_list.append(sensorR0Samples)
    
    
    #Increment While loop by 1
    i=i+1
#Takes the average of the list     
r0avg= sum(number_list)/10001


#Relative change formula for clean air
#3.3v being our highest voltage(final) - accurate samples of clean air using the average of clean air samples).
#added 1 to make it not zero
rsair= (2.3-r0avg)/(r0avg)
#rsair=6.1393234912537835
print ('rsair= '+str(rsair))
#rsair represents the clean air. On the graph (Rs/r0)~Y-intercept (mg/l)-X-intercept
#we know from the datasheet that Rs/R0=60 which is clean air
#solve for R0 and we get the equation below.
#Here we can compare the relative change to the max value of 60 
r0=rsair/60 

#print R0
print ('r0= '+str(r0))
'''
#Here we make an infinite loop to trap the user until they blow either a true or a false
#this is seen at the end code below
#rsair = 5.973044752944263
#r0=rsair/60

while True:

    #Gets input from the MCP3008 connecting to 'board'
    #board is a type of pinning for the raspberry pi, It is the classic printed numbering on the board
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D5)
    mcp = MCP.MCP3008(spi, cs)
   
   #Chnanges the analog input value to a binary output
    channel= bin(AnalogIn(mcp, MCP.P0).value)[2:] 
   #Makes it read 10 bits of the binary data  
    channel1= channel.zfill(16)
    #get the 10 bit reading from MCP 
    
    print ("channel in binary = " +str(channel))
    
    #reads voltage going into the raspberry pi    
    dirtysense= AnalogIn(mcp, MCP.P0).voltage 
    print("voltage " + str(dirtysense))

    #max value of voltage siganl is 3.3v and we do the relative change formula
    #where (3.3v(Max we can read)- dirtysense(New voltage)) / dirtysense(New Voltage))
    #rs=(56)/60
    rs=(3.28-dirtysense)/(dirtysense)
    
    #gets ratio of dirty air resistance over clean air resistance
    ratio=rs/r0
    print ('ratio= '+ str(ratio))
    
    #This is used to set our arbitrary starting axis's and prints the values of our intercept once 
    x= np.linspace(0.1,10,num=1)
    
    #This is the line in accordance to the data sheet.
    #this was done by porting each point into excell, connecting each point and finding the equation
    y= (0.5377*pow(x,-0.669))
    #linear y=-0.33*x+2.426
    #BADy=pow(10,(-0.669*math.log(x)+0.5377))
    #COPIEDy= ((math.log(ratio)-2.426)/(-0.33)) 
    
    #Gets the Rs/R0
    y2 =0*x+ratio
    
    #This is the line intersect formula for variable y to solve for x
    #This will convert our Rs/R0 to mg/l according to the chart
    xnew= float((0.41162949)/(pow(ratio,1.43061516)))
    #linear xnew=((ratio-2.426)/-0.33)
    #BADxnew= pow(10,((math.log(ratio)-0.5377)/-0.669))
    #COPIEDxnew= pow(10,y)
    
    print('mg/l= ' + str(xnew))
    #convert BRAC (mg/l) to BAC using the 2100:1
    mgLpercent= xnew
    promille= 2.1*mgLpercent
    bac =promille*10
    
    #Rounds the BAC 4 decimal places
    baclimited= round(bac,3)
    print('bac= ' +str(baclimited))
    
    channel2 = AnalogIn(mcp, MCP.P0).value
    print ("ADC = " + str(channel2))
    #case statements to determine the quality of breath
    # using ranges to determine what type of air quality it is
    #Appends to the list
    #checks if list hits 11 samples to determine when to stop appending samples.
    if (baclimited >= 0.00) and (baclimited <= 0.025)   :
        baclimited= 0.00
        print(baclimited)
        print("NOT BLOWING!!!")
    elif (baclimited >= 0.026) and (baclimited <= 0.029)  :
        if (len(baclist)<= 14):
            print("clean")
            baclimited= 0.00
            baclist.append(baclimited)
            print (baclist)
        elif len(baclist) == 15 :
            break
    elif (baclimited >= 0.029) and (baclimited <= 0.049)  :
        if (len(baclist)<= 14):
            print("light headed")
            baclist.append(baclimited)
            print (baclist)
        elif len(baclist) == 15 :
            break
    elif (baclimited >= 0.050) and (baclimited <= 0.079)  :
        if (len(baclist)<= 14):
            print("buzzed")
            baclist.append(baclimited)
            print (baclist)
        elif len(baclist) == 15 :
            break
    elif (baclimited >= 0.080) and (baclimited <= 0.109)  :
        if (len(baclist)<= 14):
            print ("Legally Impaired")
            baclist.append(baclimited)
            print (baclist)
        elif len(baclist) == 15 :
            break
    elif (baclimited >= 0.110) and (baclimited <= 0.159)  :
        if (len(baclist)<= 14):
            print ("Drunk")
            baclist.append(baclimited)
            print (baclist)
        elif len(baclist) == 15 :
            break
    elif (baclimited >= 0.160) and (baclimited <= 0.199)  :
        if (len(baclist)<= 14):
            print ("Very Drunk")
            baclist.append(baclimited)
            print (baclist)
        elif len(baclist) == 15 :
            break
    elif (baclimited >= 0.200) and (baclimited <= 0.249)  :
        if (len(baclist)<= 14):
            print ("Dazed and Confused")
            baclist.append(baclimited)
            print (baclist)
        elif len(baclist) == 15 :
            break
    elif (baclimited >= 0.250) and (baclimited <= 0.309)  :
        if (len(baclist)<= 14):
            print ("Stupor")
            baclist.append(baclimited)
            print (baclist)
        elif len(baclist) == 15 :
            break
    elif (baclimited >= 0.310) :
        if (len(baclist)<= 14):
            print ("Your in a coma ")
            baclist.append(baclimited)
            print (baclist)
        elif len(baclist) == 15 :
            break
    print()
    time.sleep(.5)

#gets the average value using the list created in the begining of the code. 
high_value= max(baclist)
avg_value= sum(baclist)/15
#mode_value= statistics.mode(baclist)
'''
l1=[]
for i in baclist:
    if i not in l1:
        l1.append(i)
        print(l1)
        
        
if len(l1)<=11 :
    mode_value= statistics.mode(baclist)
    bacdisplay= mode_value
    if high_value >= .06:
        canudrink= False
        print ("Falsemode")
        print ("Here is your Mode ", mode_value)
    else :
        canudrink = True
        print ("truemode")
        print ("Here is your Mode ", mode_value)
if len(l1)>= 12 :
    high_value= max(baclist)
    bacdisplay= high_value
    if high_value >= .06:
        canudrink= False
        print ("False")
        print("Here is your highest BAC level ", high_value)
    else :
        canudrink = True
        print ("true")
        print("Here is your highest BAC level ", high_value)
''' 
 
#print("Here is your highest BAC level ", high_value)
#print ("Here is your average BAC level ", avg_value )
"""
    #mode_value= statistics.mode(baclist)
    print ("Here is your Mode ", mode_value)
    if mode_value >= .06:
        canudrink= False
    
    else :
        canudrink = True
except failure1:
    if high_value >= .06:
        canudrink= False
    
    else :
        canudrink = True
"""

print("Here is your highest BAC level ", high_value)
print ("Here is your average BAC level ", avg_value )
#print ("Here is your Mode ", mode_value)
#Here it determines if you can drink or not as well as access locker or not
#This is done by sending either a true or false statement to which ever code needs it to be answered

if high_value >= .06:
    canudrink= False
    
else :
    canudrink = True
    
   
