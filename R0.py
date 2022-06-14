#THIS FILE TAKES CLEAN AIR SAMPLES TO BE USED FOR COMPARISON WITH THE MQ-3 DATASHEET GRAPH
import busio
import digitalio
import board
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import adafruit_mcp3xxx.mcp3008 as MCP
import RPi.GPIO as GPIO
from analog_in import AnalogIn


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
rsair= (3.28-r0avg)/(r0avg)
#rsair=6.1393234912537835
print ('rsair= '+str(rsair))
#rsair represents the clean air. On the graph (Rs/r0)~Y-intercept (mg/l)-X-intercept
#we know from the datasheet that Rs/R0=60 which is clean air
#solve for R0 and we get the equation below.
#Here we can compare the relative change to the max value of 60 
r0=rsair/60
print ("r0 = " + str(r0))






