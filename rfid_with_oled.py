from oled_091 import SSD1306
from subprocess import check_output
from time import sleep
from datetime import datetime
from os import path
import serial
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)

DIR_PATH = path.abspath(path.dirname(__file__))
DefaultFont = path.join(DIR_PATH, "Fonts/GothamLight.ttf")



class read_rfid:
   
    def read_rfid (self):
        ser = serial.Serial ("/dev/ttyS0")                           #Open named port 
        ser.baudrate = 9600                                            #Set baud rate to 9600
        data = ser.read(12)                                            #Read 12 characters from serial port to data
        if(data != " "):
            GPIO.output(17,GPIO.HIGH)
            sleep(.2)
            GPIO.output(17,GPIO.LOW)
        ser.close ()                                                   #Close port
        data=data.decode("utf-8")
        return data
def convert(id):
    new=""
    for x in id:
        new+=x
        
    return new


def info_print():
    op = False
    #display.WhiteDisplay()
    #display.DirImage(path.join(DIR_PATH, "Images/SB.png"))
    #display.DrawRect()
    #display.ShowImage()
    #sleep(1)
    #display.PrintText("Place your TAG", FontSize=14)
    #display.ShowImage()
    
    
#display = SSD1306()



SB = read_rfid()

info_print()
op = False
locker = 0
while op == False:
    
    id=SB.read_rfid()
    if convert(id) == "130031755601" :
        print ("guest 1")
        locker = 1
        op = True
        name = "Guest 1"
    elif convert(id) == "1600369D47FA" :
        print ("Guest 2")
        locker = 2
        op = True
        name = "Guest 2"
    elif convert(id) == "160036F4EF3B" :
        print ("Guest 3")
        locker = 3
        op = True
        name = "Guest 3"
    elif convert(id) == "160077646B6E" :
        print ("Guest 4")
        locker = 4
        op = True
        name = "Guest 2"
        
 #spare rfid 
    elif convert(id) == "160036AF46C9" :
        print("Guest 5")
        locker = 4
        name = "Guest 4"
        op = True
    else:
        print("RFID dont belong not here")
        op= False
        name = "RFID Not Found"
        break
GPIO.cleanup()
