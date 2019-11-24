from picamera import PiCamera  #for camera
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522   #for RFID reader
from time import sleep

import time                 
from datetime import date  
import datetime

#for the matrix keypad
import digitalio
import board
import adafruit_matrixkeypad

#init global variables
camera = PiCamera()
reader = SimpleMFRC522()

cols = [digitalio.DigitalInOut(x) for x in (board.D6, board.D13, board.D19, board.D26)]
rows = [digitalio.DigitalInOut(x) for x in (board.D16, board.D20, board.D21, board.D5)]

keys = ((1, 2, 3, 'A'),
        (4, 5, 6, 'B'),
        (7, 8, 9, 'C'),
        ('*', 0, '#', 'D'))
 
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)


#function that takes picture with current date and time as name
def kep():
    print("Taking pic")
    x = "/home/pi/mems/" + (time.strftime("%b-%d-%Y-%H-%M-%S")) + ".jpg"
    camera.capture(x)

#function showing camera picture for predefined time
def preview():
    camera.start_preview()
    sleep(5)
    camera.stop_preview()

#function reading card id and text
def idread():
    print("Reading card")
    id, text = reader.read()
    print(id)
    print(text)
        


#loop to give commands
keys = keypad.pressed_keys
while (str(keys) != "['D']"):
        
    if (str(keys) == "['C']"):
        kep()
        
    elif (str(keys) == "['B']"):
        preview()
        
    elif (str(keys) == "['A']"):
        idread()
            
    else:
        print("Invalid command")
    
    keys = keypad.pressed_keys
    if keys:
        print("Pressed: ", keys)
    time.sleep(0.1)
    
print("End of program")
    
GPIO.cleanup()
