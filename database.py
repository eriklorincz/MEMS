#for GUI
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

#for getting a line from the file
import linecache

#global variables
picfile="/home/pi/mems/files/picfile"     #file containing the dates, when pictures were taken
counter = 1                    #the number of the showed image
num_lines = sum(1 for line in open(picfile))


#create window
database = Tk()
database.title("Database")
database.geometry("530x250")
database.attributes('-zoomed', True)

#get line from file
name = linecache.getline(picfile, counter)
name = name [:-1]
path = "/home/pi/mems/"
fullname = path + name + ".jpg"

#load picture
img = ImageTk.PhotoImage(Image.open("%s" % (fullname)).resize((768, 480), Image.ANTIALIAS))
panel = tk.Label(database, image=img)
panel.pack(side="bottom", fill="both", expand="yes")
panel.place(x = 400, y= 80)

#Write the date = the name of the picture above it
date = StringVar(database, name)
datepanel = tk.Label(database, textvariable = date, font =('comicsans', 40))
datepanel.place(x = 500, y = 10)

#next picture
def NextPic():
    global num_lines
    global counter
    global date
    
    if (counter != num_lines):
        counter = counter + 1
    
    #get a line from the file
    name = linecache.getline(picfile, counter)
    name = name [:-1]
    path = "/home/pi/mems/"
    fullname = path + name + ".jpg"
    
    date.set(name)
    
    
    img = ImageTk.PhotoImage(Image.open("%s" % (fullname)).resize((768, 480), Image.ANTIALIAS))
    panel.configure(image=img)
    panel.image = img
    
    
#previous picture    
def PrevPic():
    global counter
    global date
    
    if (counter != 1):
        counter = counter - 1
        
    #get a line from the file    
    name = linecache.getline(picfile, counter)
    name = name [:-1]
    path = "/home/pi/mems/"
    fullname = path + name + ".jpg"
    
    date.set(name)
    
    img = ImageTk.PhotoImage(Image.open("%s" % (fullname)).resize((768, 480), Image.ANTIALIAS))
    panel.configure(image=img)
    panel.image = img
    
    

Next = Button(database, text = "Next", command = NextPic, fg = "black", bg = "grey", font=('comicsans', 60), height = 1, width = 5)
Next.place(x = 50, y = 30)

Prev = Button(database, text = "Prev", command = PrevPic, fg = "black", bg = "grey", font=('comicsans', 60), height = 1, width = 5)
Prev.place(x = 50, y = 200)

Back = Button(database, text = "Back", command = database.destroy, fg = "black", bg = "grey", font=('comicsans', 60), height = 1, width = 5)
Back.place(x = 50, y = 370)


database.mainloop()
