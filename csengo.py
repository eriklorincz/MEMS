from picamera import PiCamera       #for camera
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

#for external commands
import os

#for GUI
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import linecache

#for doorbell sound
from playsound import playsound

#for sending emails
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#init global variables
camera = PiCamera()      #name of the camera
reader = SimpleMFRC522() #name of the RFID reader
prevcount=0              #start or stop call
speakcount=0             #decide who is speaking (microphone activation)
password = "1234"        #default password, if no password file is available
pwd=""                   #variable for the matrix keypad password input

IsHome = 0               #For the Away - Home button
CallAct = 0              #determine if call is active

expression = ""          #used for password changing in settings menu

#file locations
pwfile = "/home/pi/mems/files/passwords"    #for the password(s)
rffile = "/home/pi/mems/files/IDs"          #for RFID numbers
picfile = "/home/pi/mems/files/picfile"     #folder of the taken pictures

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
    os.system("pkill -9 -f stream2.py")
    os.system("pkill -9 -f stream3.py")
    #os.system("amixer -c 0 cset numid=3 1")
    gui.destroy()

#Start / Stop camera
def checkPrev():
    global prevcount
    global speakcount
    
    if (prevcount == 0):
        camera.start_preview(fullscreen=False, window=(500,50,480,480))
        prevcount=1
        
        #start program for voice communication
        os.system("python3 /home/pi/mems/MEMS/stream3.py &")
        
        
    else:
        camera.stop_preview()
        prevcount=0
        speakcount=0
        os.system("pkill -9 -f stream2.py")
        os.system("pkill -9 -f stream3.py")
        os.system("amixer -c 0 cset numid=3 1")

#change the direction of active voice communication
def Speak():

    global speakcount
    global prevcount
    if (prevcount == 1):
        if (speakcount == 0):
            os.system("pkill -9 -f stream3.py")
            os.system("python3 /home/pi/mems/MEMS/stream2.py &")
            speakcount=1
        else:
            os.system("pkill -9 -f stream2.py")
            os.system("python3 /home/pi/mems/MEMS/stream3.py &")
            speakcount=0
            

#alternate between home and away
def Gone():
    
    global IsHome
    
    if (IsHome == 0):
        AwayButton.config(text = "Home" , bg = "red")
        IsHome = 1
    else:
        AwayButton.config(text = "Away", bg = "grey")
        IsHome = 0

#Open Door
def OpenDoor():
    SaveToPicF()
    os.system("python3 /home/pi/mems/MEMS/OpenDoor.py &")
    

#Play sound and take picture
def DoorBell():
    global IsHome
    os.system("amixer -c 0 cset numid=3 1")
    y = SaveToPicF()
    os.system("aplay /home/pi/pythonok/match3.wav")
    
    if (IsHome == 1):
        SendEmail(y)

#Send email with the taken picture as attachment
def SendEmail(fname):
    subject = "Someone Ringed"
    body = "Someone Ringed"
    sender_email = "frommail@gmail.com"  #set sender address
    receiver_email = "tomail@gmail.com"  #set reciever address
    password = "Password!"               #set sender password

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "/home/pi/mems/" + fname + ".jpg"  


    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {fname}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    
#loop to control peripherials
def poll():
    
    global pwd
    keys = keypad.pressed_keys

    if (str(keys) == "['A']"):
        DoorBell()
        time.sleep(0.3)
        
    elif (str(keys) == "['B']"):
        checkid()
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
    global pwfile
    password = expression
    
    f = open(pwfile, "w")
    f.write(password)
    f.close()
    
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


    ButtonBack = Button(settings, text = "Back", fg = "black", bg = "grey", font=('comicsans', 80), height = 1, width = 6, command = settings.destroy)
    ButtonBack.place(x=10, y=10)
    
    ButtonNID = Button(settings, text = "New ID", fg = "black", bg = "grey", font=('comicsans', 80), height = 1, width = 6, command = writeid)
    ButtonNID.place(x = 10, y = 200)
    
    ButtonData = Button(settings, text = "Data", fg = "black", bg = "grey", font=('comicsans', 80), height = 1, width = 6, command = ShowData)
    ButtonData.place(x = 10, y = 390)
    
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


#open an external program, which can show the taken pictures
def ShowData():

    os.system("python3 /home/pi/mems/MEMS/database.py")

#write a line to Pictures list file
def SaveToPicF():
    y = TakePic()
    f = open(picfile, "a")
    f.write("%s\n" % (y))
    #f.write("%s %d\n" % (y, origin))
    f.close()
    return y


#function that takes picture with current date and time as name
def TakePic():
    print("Taking pic")
    y = (time.strftime("%b-%d-%Y-%H-%M-%S"))
    x = "/home/pi/mems/" + y + ".jpg"
    camera.capture(x)
    return y


#function reading card id
def idread():
    id, text = reader.read()
    strid = str(id)
    return strid

#save a new id to the database
def writeid():
    ID = idread()
    f = open(rffile, "a")
    f.write("%s\n" % (ID))
    f.close()
    
#check if the read id is allowed to open the door
def checkid():
    ID = idread()
    
    try:
        f = open(rffile, "r")
        for x in f:
            x=x[:-1]
            if (x == ID):
                
                OpenDoor()
            
        f.close()
        
    except:
        k=1 #Basically: "Do nothing"

#get password from the file    
def pwFileHandle():
    
    global pwfile
    global password
    
    try:
        f = open(pwfile, "r")
        password = f.readline()
        f.close()
    #or create file with default password
    except:
        f = open(pwfile, "a")
        f.write(password)
        f.close()
        
        
        
pwFileHandle()

#os.system("amixer -c 0 cset numid=3 2")

gui = Tk()

gui.configure(background="light green")

gui.title("Csengo")

gui.geometry("530x250")
gui.attributes('-zoomed', True)

AwayButton = Button(gui, text = "Away", fg = "black", bg = "grey", command = Gone, font=('comicsans', 80), height = 1, width = 6)
AwayButton.place(x = 10, y = 20)

DoorButton = Button(gui, text = "Open", fg = "black", bg = "grey", command = OpenDoor, font=('comicsans', 80), height = 1, width = 6)
DoorButton.place(x = 10, y = 200)

CallButton = Button(gui, text = "Call", fg = "black", bg = "grey", command = checkPrev, font=('comicsans', 80), height = 1, width = 6)
CallButton.place(x = 10, y = 380)

SettingsButton = Button(gui, text = "Settings", fg = "black", bg = "grey", command = Options, font=('comicsans', 80), height = 1, width = 6)
SettingsButton.place(x = 10, y = 560)

QuitButton = Button(gui, text = "Quit", fg = "black", bg = "grey", font=('comicsans', 80), height = 1, width = 6, command = Close)
QuitButton.place(x = 10, y = 740)

SpeakButton = Button(gui, text = "Speak", fg = "black", bg = "grey", font=('comicsans', 80), height = 1, width = 6, command = Speak)
SpeakButton.place(x= 900, y = 850)

#Body of the program
gui.after(10, poll)
gui.mainloop()
    
print("End of program")
    
GPIO.cleanup()

