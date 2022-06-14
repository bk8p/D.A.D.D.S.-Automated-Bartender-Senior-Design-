import tkinter as tk
import tkinter.messagebox
from tkinter import *
import RPi.GPIO as GPIO
import time
import serial
from time import sleep
import importlib
import rfid_with_oled
import R0
import MCP3008x

GPIO.cleanup()
#from rfid_with_oled import *


#creates main window
main =Tk()

#Set size for specific window
main.geometry("800x480")

#sets window color
main.configure(bg='black')

drink_cost = [0,0,0,0]
drink_count= [0,0,0,0]
global name
def mainWin():
    #first popup window to verfied BAC and Drink total/cost
    def popup():
        popup= Toplevel(main)
        popup.title("new window")
        popup.geometry("800x480")
        popup.configure(bg= 'black')
        Label(popup, text = "BAC : " + str(MCP3008x.high_value), font = ('Mistral 18 bold')).place(x=150,y=80)
        if(rfid_with_oled.name == "Guest 1"):
            Label(popup, text = "Drink total: " + str(drink_count[0]), font = ('Mistral 18 bold')).place(x=150,y=50)
            Label(popup, text = "Drink cost: " + str(drink_cost[0]), font = ('Mistral 18 bold')).place(x=150,y=20)
        elif(rfid_with_oled.name == "Guest 2"):
            Label(popup, text = "Drink total: " + str(drink_count[1]), font = ('Mistral 18 bold')).place(x=150,y=50)
            Label(popup, text = "Drink cost: " + str(drink_cost[1]), font = ('Mistral 18 bold')).place(x=150,y=20)
        elif(rfid_with_oled.name == "Guest 3"):
            Label(popup, text = "Drink total: " + str(drink_count[2]), font = ('Mistral 18 bold')).place(x=150,y=50)
            Label(popup, text = "Drink cost: " + str(drink_cost[2]), font = ('Mistral 18 bold')).place(x=150,y=20)
        elif(rfid_with_oled.name == "Guest 4"):
            Label(popup, text = "Drink total: " + str(drink_count[3]), font = ('Mistral 18 bold')).place(x=150,y=50)
            Label(popup, text = "Drink cost: " + str(drink_cost[3]), font = ('Mistral 18 bold')).place(x=150,y=20)
        else :
            Label(popup, text = "BAC and RFID doesnt pass", font = ('Mistral 18 bold')).place(x=150,y=50)
            Label(popup, text = "BAC and RFID doesnt pass", font = ('Mistral 18 bold')).place(x=150,y=20)

        main.after(3000,lambda:popup.destroy())
    #second popup for displaying timer
    def popup2(time_sec):
        popup= Toplevel(main)
        popup.title("new window")
        popup.geometry("800x480")
        popup.configure(bg= 'black')
       # time_sec -= 1
        Label(popup, text = "Wait for ~ " + str(time_sec) + " secs", font = ('Mistral 18 bold')).place(x=150,y=50)
       # while time_sec >0:
        """    Label(popup, text = "Wait for :"+ str(time_sec), font = ('Mistral 18 bold')).place(x=150,y=50)
            time_sec=time_sec-1
            Label(popup, text = " ")
            main.update()"""
        
        #change 3000 to time_sec later
        main.after(3000,lambda:popup.destroy())
        #destory popup after 155 sec
        #need to modifiy seconds
    
    def popup3():
        p3 =Tk()
        popup3= Toplevel(p3)
        popup3.title("Asah Dud")
        popup3.geometry("800x480")
        popup3.configure(bg= 'black')
        Label(popup3, text = " Scan RFID tag &Blow into breathalyzer", font = ('Mistral 18 bold')).place(x=150,y=50)
        popup3.after(3000,lambda:p3.destroy())
    
        
    def countdown(time_sec):
        while time_sec:
            mins, secs = divmod(time_sec,60)
            timeformat = '{:02d}:{:02d}'.format(mins,secs)
            print(timeformat, end=('/r'))
            main.update()
            time.sleep(1)
            time_sec -= 1
            
    def checkwindow():
        tkinter.messagebox.showinfo("Check Window","Press OK and then Scan Your RFID Tag and Blow!")
        name = rfid_with_oled.name
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        importlib.reload(rfid_with_oled)
        #import rfid_with_oled

        #from MCP3008x import canudrink
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        importlib.reload(MCP3008x)
        
            #exec(open('MCP3008x.py').read())
        #GPIO.cleanup()
        
        if (rfid_with_oled.op == True and MCP3008x.canudrink == True ):
            print('yes')
            drinkMenu()
            drinkop= True
            name= rfid_with_oled.name
        elif ((rfid_with_oled.op==False) or (MCP3008x.canudrink==False)):
            print ('No drinks anymore')
            drinkop= False
            
        #exec(open('userCheck.py').read())
        #exec(open('rfid_with_oled.py').read())
       
        if(name == "Guest 1"):
            #cost = Label(main,str(drink_cost[0]), pady=0, padx=90)
            #cost.pack()
     
            print ("Cost " + str(drink_cost[0]))
            print ("Count " + str(drink_count[0]))
        elif (name == "Guest 2"):
            
            print ("Cost " + str(drink_cost[1]))
            print ("Count " + str(drink_count[1]))
        elif (name == "Guest 3"):
            
            print ("Cost " + str(drink_cost[2]))
            print ("Count " + str(drink_count[2]))
        elif (rfid_with_oled.name == "Guest 4"):
            
            print ("Cost " + str(drink_cost[3]))
            print ("Count " + str(drink_count[3]))
        else :
            print ("RFID does not match" )
            #cost = Label1(main,str(drink_cost[0]), pady=0, padx=90)
            #cost.pack()
        popup()
        return name
    
    def checkWindowSafe():
        tkinter.messagebox.showinfo("Check Window","Press OK and then Scan Your RFID Tag and Blow!")
        name = rfid_with_oled.name
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        importlib.reload(rfid_with_oled)

        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        importlib.reload(MCP3008x)

        
        if (rfid_with_oled.op == True and MCP3008x.canudrink == True ):
            print('yes')
            safeMode()
            drinkop= True
            name= rfid_with_oled.name
        elif ((rfid_with_oled.op==False) or (MCP3008x.canudrink==False)):
            print ('No drinks anymore')
            drinkop= False
            
        #exec(open('userCheck.py').read())
        #exec(open('rfid_with_oled.py').read())
       
        if(name == "Guest 1"):
            #cost = Label(main,str(drink_cost[0]), pady=0, padx=90)
            #cost.pack()
     
            print ("Cost " + str(drink_cost[0]))
            print ("Count " + str(drink_count[0]))
        elif (name == "Guest 2"):
            
            print ("Cost " + str(drink_cost[1]))
            print ("Count " + str(drink_count[1]))
        elif (name == "Guest 3"):
            
            print ("Cost " + str(drink_cost[2]))
            print ("Count " + str(drink_count[2]))
        elif (rfid_with_oled.name == "Guest 4"):
            
            print ("Cost " + str(drink_cost[3]))
            print ("Count " + str(drink_count[3]))
        else :
            print ("RFID does not match" )
            #cost = Label1(main,str(drink_cost[0]), pady=0, padx=90)
            #cost.pack()
        popup()
        return name 
        
    def drinkMenu():
            
            msLabel.destroy()
            buttonDrink.destroy()
            buttonSafe.destroy()
            #exec(open('userCheck').read())
            #destroy check window elements 
            #msLabel.destroy()
            #buttonDrink.destroy()
            #buttonSafe.destroy()
            
            buttonDrink1.grid(row=1, column=0)
            buttonDrink2.grid(row=1, column=2)
            buttonDrink3.grid(row=2, column=0)
            #buttonDrink4.grid(row=1, column=2)
            buttonDrink5.grid(row=2, column=2)
            '''buttonDrink6.grid(row=3, column=2)
            buttonDrink7.grid(row=1, column=4)
            buttonDrink8.grid(row=2, column=4)
            buttonDrink9.grid(row=3, column=4)
            buttonDrink10.grid(row=1, column=6)'''
            buttonDrink11.grid(row=3, column=0)
            '''buttonDrink12.grid(row=3, column=6)
            buttonDrink13.grid(row=1, column=8)
            buttonDrink14.grid(row=2, column=8)
            buttonDrink15.grid(row=3, column=8)'''
        
            buttonBack.grid(row=3, column=1)
            print("Drinks")
             

    def safeMode():
        msLabel.destroy()
        buttonDrink.destroy()
        buttonSafe.destroy()
        buttonLock1.grid(row=1, column=2)
        buttonBack.grid(row=2, column=10)
        print("Safe Mode")

    def back():
        buttonDrink1.destroy()
        buttonDrink2.destroy()
        buttonDrink3.destroy()
        #buttonDrink4.destroy()
        buttonDrink5.destroy()
        '''buttonDrink6.destroy()
        buttonDrink7.destroy()
        buttonDrink8.destroy()
        buttonDrink9.destroy()
        buttonDrink10.destroy()'''
        buttonDrink11.destroy()
        '''buttonDrink12.destroy()
        buttonDrink13.destroy()
        buttonDrink14.destroy()
        buttonDrink15.destroy()'''
        buttonLock1.destroy()
        buttonBack.destroy()
        mainWin()
#*************************--Drinks--****************************
    def drink1():
        #GPIO.cleanup()
        #exec(open('drink1.py').read())
        #name= checkwindow()
        #COUNTERS
        if(rfid_with_oled.name == "Guest 1"):
            drink_cost[0] = drink_cost[0]+2
            drink_count[0] = drink_count[0]+1    
            print ("Cost" + str(drink_cost[0]))
            print ("Count" + str(drink_count[0]))
            popup2(155)
            back()
        elif (rfid_with_oled.name == "Guest 2"):
            drink_cost[1] = drink_cost[1]+2
            drink_count[1] = drink_count[1]+1
            print ("Cost" + str(drink_cost[1]))
            print ("Count" + str(drink_count[1]))
            popup2(155)
            back()
        elif (rfid_with_oled.name == "Guest 3"):
            drink_cost[2] = drink_cost[2]+2
            drink_count[2] = drink_count[2]+1
            print ("Cost" + str(drink_cost[2]))
            print ("Count" + str(drink_count[2]))
            popup2(155)
            back()
        elif (rfid_with_oled.name == "Guest 4"):
            popup2(155)
            drink_cost[3] = drink_cost[3]+2
            drink_count[3] = drink_count[3]+1
            print ("Cost" + str(drink_cost[3]))
            print ("Count" + str(drink_count[3]))
            #popup2(155)
            back()
        else :
            print ("RFID does not match" )
        GPIO.cleanup()
        exec(open('drink1.py').read())
    def drink2():
        GPIO.cleanup()
        exec(open('drink2.py').read())
        if(rfid_with_oled.name == "Guest 1"):
            drink_cost[0] = drink_cost[0]+2
            drink_count[0] = drink_count[0]+1    
            print ("Cost" + str(drink_cost[0]))
            print ("Count" + str(drink_count[0]))
            back()
        elif (rfid_with_oled.name == "Guest 2"):
            drink_cost[1] = drink_cost[1]+2
            drink_count[1] = drink_count[1]+1
            print ("Cost" + str(drink_cost[1]))
            print ("Count" + str(drink_count[1]))
            back()
        elif (rfid_with_oled.name == "Guest 3"):
            drink_cost[2] = drink_cost[2]+2
            drink_count[2] = drink_count[2]+1
            print ("Cost" + str(drink_cost[2]))
            print ("Count" + str(drink_count[2]))
            back()
        elif (rfid_with_oled.name == "Guest 4"):
            drink_cost[3] = drink_cost[3]+2
            drink_count[3] = drink_count[3]+1
            print ("Cost" + str(drink_cost[3]))
            print ("Count" + str(drink_count[3]))
            back()
    def drink3():
        GPIO.cleanup()
        exec(open('drink3.py').read())
        if(rfid_with_oled.name == "Guest 1"):
            drink_cost[0] = drink_cost[0]+2
            drink_count[0] = drink_count[0]+1    
            print ("Cost" + str(drink_cost[0]))
            print ("Count" + str(drink_count[0]))
            back()
        elif (rfid_with_oled.name == "Guest 2"):
            drink_cost[1] = drink_cost[1]+2
            drink_count[1] = drink_count[1]+1
            print ("Cost" + str(drink_cost[1]))
            print ("Count" + str(drink_count[1]))
            back()
        elif (rfid_with_oled.name == "Guest 3"):
            drink_cost[2] = drink_cost[2]+2
            drink_count[2] = drink_count[2]+1
            print ("Cost" + str(drink_cost[2]))
            print ("Count" + str(drink_count[2]))
            back()
        elif (rfid_with_oled.name == "Guest 4"):
            drink_cost[3] = drink_cost[3]+2
            drink_count[3] = drink_count[3]+1
            print ("Cost" + str(drink_cost[3]))
            print ("Count" + str(drink_count[3]))
            back()
    '''def drink4():
        GPIO.cleanup()
        exec(open('drink4.py').read())
        if(rfid_with_oled.name == "Guest 1"):
            drink_cost[0] = drink_cost[0]+2
            drink_count[0] = drink_count[0]+1    
            print ("Cost" + str(drink_cost[0]))
            print ("Count" + str(drink_count[0]))
            back()
        elif (rfid_with_oled.name == "Guest 2"):
            drink_cost[1] = drink_cost[1]+2
            drink_count[1] = drink_count[1]+1
            print ("Cost" + str(drink_cost[1]))
            print ("Count" + str(drink_count[1]))
            back()
        elif (rfid_with_oled.name == "Guest 3"):
            drink_cost[2] = drink_cost[2]+2
            drink_count[2] = drink_count[2]+1
            print ("Cost" + str(drink_cost[2]))
            print ("Count" + str(drink_count[2]))
            back()
        elif (rfid_with_oled.name == "Guest 4"):
            drink_cost[3] = drink_cost[3]+2
            drink_count[3] = drink_count[3]+1
            print ("Cost" + str(drink_cost[3]))
            print ("Count" + str(drink_count[3]))
            back()'''
    def drink5():
        GPIO.cleanup()
        exec(open('drink5.py').read())
        if(rfid_with_oled.name == "Guest 1"):
            drink_cost[0] = drink_cost[0]+2
            drink_count[0] = drink_count[0]+1    
            print ("Cost" + str(drink_cost[0]))
            print ("Count" + str(drink_count[0]))
            back()
        elif (rfid_with_oled.name == "Guest 2"):
            drink_cost[1] = drink_cost[1]+2
            drink_count[1] = drink_count[1]+1
            print ("Cost" + str(drink_cost[1]))
            print ("Count" + str(drink_count[1]))
            back()
        elif (rfid_with_oled.name == "Guest 3"):
            drink_cost[2] = drink_cost[2]+2
            drink_count[2] = drink_count[2]+1
            print ("Cost" + str(drink_cost[2]))
            print ("Count" + str(drink_count[2]))
            back()
        elif (rfid_with_oled.name == "Guest 4"):
            drink_cost[3] = drink_cost[3]+2
            drink_count[3] = drink_count[3]+1
            print ("Cost" + str(drink_cost[3]))
            print ("Count" + str(drink_count[3]))
            back()
    '''def drink6():
        GPIO.cleanup()
        exec(open('drink6.py').read())
        if(rfid_with_oled.name == "Guest 1"):
            drink_cost[0] = drink_cost[0]+2
            drink_count[0] = drink_count[0]+1    
            print ("Cost" + str(drink_cost[0]))
            print ("Count" + str(drink_count[0]))
            back()
        elif (rfid_with_oled.name == "Guest 2"):
            drink_cost[1] = drink_cost[1]+2
            drink_count[1] = drink_count[1]+1
            print ("Cost" + str(drink_cost[1]))
            print ("Count" + str(drink_count[1]))
            back()
        elif (rfid_with_oled.name == "Guest 3"):
            drink_cost[2] = drink_cost[2]+2
            drink_count[2] = drink_count[2]+1
            print ("Cost" + str(drink_cost[2]))
            print ("Count" + str(drink_count[2]))
            back()
        elif (rfid_with_oled.name == "Guest 4"):
            drink_cost[3] = drink_cost[3]+2
            drink_count[3] = drink_count[3]+1
            print ("Cost" + str(drink_cost[3]))
            print ("Count" + str(drink_count[3]))
            back()
    def drink7():
        GPIO.cleanup()
        exec(open('drink7.py').read())
        if(rfid_with_oled.name == "Guest 1"):
            drink_cost[0] = drink_cost[0]+2
            drink_count[0] = drink_count[0]+1    
            print ("Cost" + str(drink_cost[0]))
            print ("Count" + str(drink_count[0]))
            back()
        elif (rfid_with_oled.name == "Guest 2"):
            drink_cost[1] = drink_cost[1]+2
            drink_count[1] = drink_count[1]+1
            print ("Cost" + str(drink_cost[1]))
            print ("Count" + str(drink_count[1]))
            back()
        elif (rfid_with_oled.name == "Guest 3"):
            drink_cost[2] = drink_cost[2]+2
            drink_count[2] = drink_count[2]+1
            print ("Cost" + str(drink_cost[2]))
            print ("Count" + str(drink_count[2]))
            back()
        elif (rfid_with_oled.name == "Guest 4"):
            drink_cost[3] = drink_cost[3]+2
            drink_count[3] = drink_count[3]+1
            print ("Cost" + str(drink_cost[3]))
            print ("Count" + str(drink_count[3]))
            back()
    def drink8():
        GPIO.cleanup()
        exec(open('drink8.py').read())
        if(rfid_with_oled.name == "Guest 1"):
            drink_cost[0] = drink_cost[0]+2
            drink_count[0] = drink_count[0]+1    
            print ("Cost" + str(drink_cost[0]))
            print ("Count" + str(drink_count[0]))
            back()
        elif (rfid_with_oled.name == "Guest 2"):
            drink_cost[1] = drink_cost[1]+2
            drink_count[1] = drink_count[1]+1
            print ("Cost" + str(drink_cost[1]))
            print ("Count" + str(drink_count[1]))
            back()
        elif (rfid_with_oled.name == "Guest 3"):
            drink_cost[2] = drink_cost[2]+2
            drink_count[2] = drink_count[2]+1
            print ("Cost" + str(drink_cost[2]))
            print ("Count" + str(drink_count[2]))
            back()
        elif (rfid_with_oled.name == "Guest 4"):
            drink_cost[3] = drink_cost[3]+2
            drink_count[3] = drink_count[3]+1
            print ("Cost" + str(drink_cost[3]))
            print ("Count" + str(drink_count[3]))
            back()
    def drink9():
        GPIO.cleanup()
        exec(open('drink9.py').read())
        if(rfid_with_oled.name == "Guest 1"):
            drink_cost[0] = drink_cost[0]+2
            drink_count[0] = drink_count[0]+1    
            print ("Cost" + str(drink_cost[0]))
            print ("Count" + str(drink_count[0]))
            back()
        elif (rfid_with_oled.name == "Guest 2"):
            drink_cost[1] = drink_cost[1]+2
            drink_count[1] = drink_count[1]+1
            print ("Cost" + str(drink_cost[1]))
            print ("Count" + str(drink_count[1]))
            back()
        elif (rfid_with_oled.name == "Guest 3"):
            drink_cost[2] = drink_cost[2]+2
            drink_count[2] = drink_count[2]+1
            print ("Cost" + str(drink_cost[2]))
            print ("Count" + str(drink_count[2]))
            back()
        elif (rfid_with_oled.name == "Guest 4"):
            drink_cost[3] = drink_cost[3]+2
            drink_count[3] = drink_count[3]+1
            print ("Cost" + str(drink_cost[3]))
            print ("Count" + str(drink_count[3]))
            back()
    def drink10():
        GPIO.cleanup()
        exec(open('drink10.py').read())
        if(rfid_with_oled.name == "Guest 1"):
            drink_cost[0] = drink_cost[0]+2
            drink_count[0] = drink_count[0]+1    
            print ("Cost" + str(drink_cost[0]))
            print ("Count" + str(drink_count[0]))
            back()
        elif (rfid_with_oled.name == "Guest 2"):
            drink_cost[1] = drink_cost[1]+2
            drink_count[1] = drink_count[1]+1
            print ("Cost" + str(drink_cost[1]))
            print ("Count" + str(drink_count[1]))
            back()
        elif (rfid_with_oled.name == "Guest 3"):
            drink_cost[2] = drink_cost[2]+2
            drink_count[2] = drink_count[2]+1
            print ("Cost" + str(drink_cost[2]))
            print ("Count" + str(drink_count[2]))
            back()
        elif (rfid_with_oled.name == "Guest 4"):
            drink_cost[3] = drink_cost[3]+2
            drink_count[3] = drink_count[3]+1
            print ("Cost" + str(drink_cost[3]))
            print ("Count" + str(drink_count[3]))
            back()'''
    def drink11():
        GPIO.cleanup()
        exec(open('drink11.py').read())
        if(rfid_with_oled.name == "Guest 1"):
            drink_cost[0] = drink_cost[0]+2
            drink_count[0] = drink_count[0]+1    
            print ("Cost" + str(drink_cost[0]))
            print ("Count" + str(drink_count[0]))
            back()
        elif (rfid_with_oled.name == "Guest 2"):
            drink_cost[1] = drink_cost[1]+2
            drink_count[1] = drink_count[1]+1
            print ("Cost" + str(drink_cost[1]))
            print ("Count" + str(drink_count[1]))
            back()
        elif (rfid_with_oled.name == "Guest 3"):
            drink_cost[2] = drink_cost[2]+2
            drink_count[2] = drink_count[2]+1
            print ("Cost" + str(drink_cost[2]))
            print ("Count" + str(drink_count[2]))
            back()
        elif (rfid_with_oled.name == "Guest 4"):
            drink_cost[3] = drink_cost[3]+2
            drink_count[3] = drink_count[3]+1
            print ("Cost" + str(drink_cost[3]))
            print ("Count" + str(drink_count[3]))
            back()
#*************************--Locekrs--****************************
    def locker1():
        #buttonLock1.destroy()
        #buttonLock2.destroy()
        #buttonLock3.destroy()
        #buttonLock4.destroy()
        #buttonBack.grid(row=1, column=10)
        #print("Opening Locker 1")
        GPIO.cleanup()
        exec(open('safemenu_intergration.py').read())
        back()

    # Creating Title Label
    msLabel = Label(main, text="D.A.D.D.S.", pady=0, padx=90)

    # Buttons for drink menu, safe box, and back
    
    buttonDrink = Button(main, text="Drink Menu", command=checkwindow, pady=90, padx=90, bg='blue', fg='white')
    buttonSafe = Button(main, text="Safe Box Mode", command=checkWindowSafe, pady=90, padx=90, bg='red', fg='white')
    buttonBack = Button(main, text="BACK", command=back, pady=15, padx=15, bg='red', fg='white')
    
    # Buttons for Lockers
    buttonLock1 = Button(main, text="Open Locker ", command=locker1, padx=150, pady=100, bg='purple', fg='cyan')
    
    # Buttons for Drinks
    buttonDrink1 = Button(main, text="Spiked Lemonade", padx=80, pady=60, bg='green', fg='black', command=drink1)
    buttonDrink2 = Button(main, text="Vodka Shot", padx=80, pady=60, bg='green', fg='black', command=drink2)
    buttonDrink3 = Button(main, text="Ginger Ale", padx=80, pady=60, bg='green', fg='black', command=drink3)
    #buttonDrink4 = Button(main, text="Drink 4", padx=50, pady=60, bg='green', fg='black', command=drink4)
    buttonDrink5 = Button(main, text="Club Soda", padx=80, pady=60, bg='green', fg='black', command=drink5)
    '''buttonDrink6 = Button(main, text="Drink 6", padx=50, pady=60, bg='green', fg='black', command=drink6)
    buttonDrink7 = Button(main, text="Drink 7", padx=50, pady=60, bg='blue', fg='white', command=drink7)
    buttonDrink8 = Button(main, text="Drink 8", padx=50, pady=60, bg='blue', fg='white', command=drink8)
    buttonDrink9 = Button(main, text="Drink 9", padx=50, pady=60, bg='blue', fg='white', command=drink9)
    buttonDrink10 = Button(main, text="Drink 10", padx=50, pady=60, bg='blue', fg='white', command=drink10)'''
    buttonDrink11 = Button(main, text="Moscow Mule", padx=150, pady=60, bg='blue', fg='white', command=drink11)
    '''buttonDrink12 = Button(main, text="Drink 12", padx=50, pady=60, bg='blue', fg='white')#, command=drink12)
    buttonDrink13 = Button(main, text="Drink 13", padx=50, pady=60, bg='yellow', fg='black')#, command=drink13)
    buttonDrink14 = Button(main, text="Drink 14", padx=50, pady=60, bg='yellow', fg='black')#, command=drink14)
    buttonDrink15 = Button(main, text="Drink 15", padx=50, pady=60, bg='yellow', fg='black')#, command=drink15)'''

#certain place for text   **********Dont Mix with .pack()*****************
#msLabel1.grid(row=0, column= 0)
#, bg='black',fg ='white'

#Push to the screen #
    buttonDrink.pack(side = LEFT )
    buttonSafe.pack(side = RIGHT)
    msLabel.pack()

mainWin()

main.mainloop()











