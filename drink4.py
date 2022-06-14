import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

GPIO.setup(32, GPIO.OUT)
GPIO.output(32, GPIO.HIGH)
GPIO.setup(36,  GPIO.OUT)
GPIO.output(36, GPIO.HIGH)
GPIO.setup(38, GPIO.OUT)
GPIO.output(38, GPIO.HIGH)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.HIGH)

GPIO.output(38, GPIO.LOW)
time.sleep(15.5) #155 sec, modifed for testing
GPIO.cleanup()
print("ALL OFF.... DONE!!")