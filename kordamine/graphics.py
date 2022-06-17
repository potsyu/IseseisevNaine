from tkinter import *


def run(): #Defineerib klassi
    name1 = name_storage.get() #Lisab variable name1
    print(name1) # prindib name1
    name.delete(0, END)


screen = Tk() # uus variable tk
screen.title("My first graphics program") # lisab tiitli "My first graphics program"
screen.geometry("500x500") # suurus 500x500

welcome_text = Label(text="Welcome to our first graphics program ", fg="red", bg="yellow") # lisab welcome texti
welcome_text.pack()

click_me = Button(text="Click me", fg="red", bg="yellow", command=run) #lisab nuppu
click_me.place(x=10, y=20) # nuppu suurus

name_storage = StringVar() # loob storage
name = Entry(textvariable=name_storage) # loob nime storage
name.pack()
screen.mainloop()
