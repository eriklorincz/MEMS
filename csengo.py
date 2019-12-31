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

#for GUI
from tkinter import *

#init global variables
camera = PiCamera()
reader = SimpleMFRC522()
prevcount=0
password = "1234"
pwd=""

#for matrix keypad
cols = [digitalio.DigitalInOut(x) for x in (board.D6, board.D13, board.D19, board.D26)]
rows = [digitalio.DigitalInOut(x) for x in (board.D16, board.D20, board.D21, board.D5)]

keys = ((1, 2, 3, 'A'),
        (4, 5, 6, 'B'),
        (7, 8, 9, 'C'),
        ('*', 0, '#', 'D'))
 
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
numbers = ("[0]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]", "[9]")

#Quit program
def Close():
    camera.stop_preview()
    gui.after_cancel(poll)
    gui.destroy()

#Start / Stop camera
def checkPrev():
    global prevcount
    
    if (prevcount == 0):
        camera.start_preview(fullscreen=False,window=(500,50,1280,960))
        prevcount=1
        
    else:
        camera.stop_preview()
        prevcount=0


#Open Door
def OpenDoor():
    print("Door is open")

#loop to control peripherials
def poll():
    
    global pwd
    keys = keypad.pressed_keys
    if (str(keys) == "['C']"):
        kep()
        time.sleep(0.3)
        
    elif (str(keys) == "['B']"):
        preview()
        time.sleep(0.3)
        
    elif (str(keys) == "['A']"):
        idread()
        time.sleep(0.3)
        
    elif (str(keys) == "['*']"):
        pwd=""
        time.sleep(0.3)
        
    elif (str(keys) in numbers):
        pwd=pwd+(str(keys)[1])
        print(pwd)
        if (pwd == password):
            pwd=""
            OpenDoor()
        time.sleep(0.3)
            
    else:
        print("Invalid command")
        
    gui.after(10, poll)


#function that takes picture with current date and time as name
def kep():
    print("Taking pic")
    x = "/home/pi/mems/" + (time.strftime("%b-%d-%Y-%H-%M-%S")) + ".jpg"
    camera.capture(x)


#function reading card id and text
def idread():
    print("Reading card")
    id, text = reader.read()
    print(id)
    print(text)


gui = Tk()

gui.configure(background="light green")

gui.title("Csengo")

gui.geometry("530x250")
gui.attributes('-zoomed', True)

AwayButton = Button(gui, text = "Away", fg = "black", bg = "grey", font=('comicsans', 80), height = 1, width = 6)
AwayButton.place(x = 10, y = 20)

DoorButton = Button(gui, text = "Open", fg = "black", bg = "grey", command = OpenDoor, font=('comicsans', 80), height = 1, width = 6)
DoorButton.place(x = 10, y = 200)

CallButton = Button(gui, text = "Call", fg = "black", bg = "grey", command = checkPrev, font=('comicsans', 80), height = 1, width = 6)
CallButton.place(x = 10, y = 380)

SettingsButton = Button(gui, text = "Settings", fg = "black", bg = "grey", font=('comicsans', 80), height = 1, width = 6)
SettingsButton.place(x = 10, y = 560)

QuitButton = Button(gui, text = "Quit", fg = "black", bg = "grey", font=('comicsans', 80), height = 1, width = 6, command = Close)
QuitButton.place(x = 10, y = 740)

#Body of the program
gui.after(10, poll)
gui.mainloop()
    
print("End of program")
    
GPIO.cleanup()
