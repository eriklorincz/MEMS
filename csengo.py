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

expression = ""

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
    
#for the password change in settings menu
def press(num, equation): 
     
    global expression
 
    expression = expression + str(num) 

    equation.set(expression)
    
# Function to clear the contents 
# of text entry box 
def clear(equation):
    global expression 
    expression = "" 
    equation.set("")
    
#save the change of password   
def OK(equation):
    
    global expression
    global password
    password = expression
    
    clear(equation)


#Menu, available via settings button
def Options():
    
    global newpwd
    
    settings = Tk()
    settings.configure(background = "blue")
    settings.title("Settings")
    settings.geometry("530x250")
    settings.attributes('-zoomed', True)
    
    equation = StringVar(settings, "New password") 

    expression_field = Entry(settings, textvariable = equation, font =('comicsans', 50), width = 13)
    expression_field.place(x = 700, y = 100)    


    QuitS = Button(settings, text = "Quit", fg = "black", bg = "grey", font=('comicsans', 80), height = 1, width = 6, command = settings.destroy)
    QuitS.place(x=10, y=10)
    
    button1 = Button(settings, text=' 1 ', fg='black', bg='red', font=('comicsans', 50), command=lambda: press(1, equation), height=1, width=3) 
    button1.place(x=700, y=200) 
    
    button2 = Button(settings, text=' 2 ', fg='black', bg='red', font=('comicsans', 50), command=lambda: press(2, equation), height=1, width=3) 
    button2.place(x=900, y=200)
  
    button3 = Button(settings, text=' 3 ', fg='black', bg='red', font=('comicsans', 50), command=lambda: press(3, equation), height=1, width=3) 
    button3.place(x=1100, y=200) 
    
    button4 = Button(settings, text=' 4 ', fg='black', bg='red', font=('comicsans', 50), command=lambda: press(4, equation), height=1, width=3) 
    button4.place(x=700, y=400)
    
    button5 = Button(settings, text=' 5 ', fg='black', bg='red', font=('comicsans', 50), command=lambda: press(5, equation), height=1, width=3) 
    button5.place(x=900, y=400)
  
    button6 = Button(settings, text=' 6 ', fg='black', bg='red', font=('comicsans', 50), command=lambda: press(6, equation), height=1, width=3) 
    button6.place(x=1100, y=400)
    
    button7 = Button(settings, text=' 7 ', fg='black', bg='red', font=('comicsans', 50), command=lambda: press(7, equation), height=1, width=3) 
    button7.place(x=700, y=600)
    
    button8 = Button(settings, text=' 8 ', fg='black', bg='red', font=('comicsans', 50), command=lambda: press(8, equation), height=1, width=3) 
    button8.place(x=900, y=600)
  
    button9 = Button(settings, text=' 9 ', fg='black', bg='red', font=('comicsans', 50), command=lambda: press(9, equation), height=1, width=3) 
    button9.place(x=1100, y=600)
    
    button0 = Button(settings, text=' 0 ', fg='black', bg='red', font=('comicsans', 50), command=lambda: press(0, equation), height=1, width=3) 
    button0.place(x=700, y=800)
    
    buttonClear = Button(settings, text = "CLS", fg='black', bg='red', font=('comicsans', 50), command=lambda: clear(equation), height=1, width=3)
    buttonClear.place(x = 900, y = 800)
    
    buttonOK = Button(settings, text = "OK", fg='black', bg='red', command = lambda: OK(equation), font=('comicsans', 50), height=1, width=3)
    buttonOK.place(x= 1100, y = 800)
    
    
    settings.mainloop()


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

SettingsButton = Button(gui, text = "Settings", fg = "black", bg = "grey", command = Options, font=('comicsans', 80), height = 1, width = 6)
SettingsButton.place(x = 10, y = 560)

QuitButton = Button(gui, text = "Quit", fg = "black", bg = "grey", font=('comicsans', 80), height = 1, width = 6, command = Close)
QuitButton.place(x = 10, y = 740)

#Body of the program
gui.after(10, poll)
gui.mainloop()
    
print("End of program")
    
GPIO.cleanup()
