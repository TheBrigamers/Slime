#!/usr/bin/env python
#-*- coding: utf-8 -*-
from tkinter import *
from PIL import Image,ImageTk
import ipgetter
import socket
import os
import requests
import json
import ctypes
import time

""" Connection """

hote = ''
port = 25565
main_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_co.bind((hote, port))
main_co.listen(5)
client_co , info = main_co.accept()
print("Connexion établie")
ip = info[0]

def closeConnection():
    client_co.close()
    main_co.close()

def recieve():
    recv = client_co.recv(999999)
    recv = recv.decode(encoding='utf-8', errors='ignore')
    recv = recv.split('/')
    return recv[0]

def send(msg):
    msg = msg.encode(encoding='utf-8',errors='ignore')
    client_co.send(msg)
    reponse = recieve()
    setResult(reponse)

def setResult(rslt):
    Resulttext.config(state=NORMAL)
    Resulttext.insert(INSERT, rslt + "\n\n")
    Resulttext.config(state=DISABLED)
 
def clearResult():
    Resulttext.config(state=NORMAL)
    Resulttext.delete(1.0,END)
    Resulttext.config(state=DISABLED)
""" Graphique """
window = Tk()

def getInfos():
    send('infos')
    
def getEnviron():
    send('environ')

def sendMessage(message):
    send('message ' + message)
    
def setMessage():
    getMessageWindow = Tk()
    getMessageEntry = Entry(getMessageWindow, width=50)
    getMessageEntry.pack(side = TOP)
    getMessageSend = Button(getMessageWindow, text="Envoyer", relief=RAISED, width=50, command=lambda : sendMessage(getMessageEntry.get()))
    getMessageSend.pack(side = BOTTOM)
    getMessageWindow.mainloop()
    
def setImage(imgFile,sizex,sizey):
    imgBase = Image.open(imgFile)
    imgBase = imgBase.resize((sizex,sizey))
    img = ImageTk.PhotoImage(imgBase)
    return img

def setShutdown():
    send('shutdown')

window.geometry("800x600+300+200")

# Ordinateur #

ComputerFrame = Frame(window,width=200, bg='light gray')
ComputerFrame.config(width=800, height=100)
ComputerFrame.pack_propagate(False)
ComputerFrame.pack(side = TOP)
#Ordinateur - Label
Computerlabel = Label(ComputerFrame,text="Ordinateur", bg='light gray')
Computerlabel.config(font=("Courier", 20))
Computerlabel.pack()
#Bouttons - Frame
ComputerButtonsFrame = Frame(ComputerFrame, width=200, height=50)
ComputerButtonsFrame.pack(side = BOTTOM)
#Arret - Button
stopConnexionImg = setImage('img/arret.png',50,50)
stopConnexionButton = Button(ComputerButtonsFrame, image=stopConnexionImg, relief=RAISED, width=50,height=50, command=setShutdown)
stopConnexionButton.pack(side = LEFT)
#Redemarer - Button
RestartConnexionImg = setImage('img/redemarrer.png',50,50)
RestartConnexionButton = Button(ComputerButtonsFrame, image=RestartConnexionImg, relief=RAISED, width=50,height=50)
RestartConnexionButton.pack(side = LEFT)
#Veille - Button
VeilleImg = setImage('img/veille.png',50,50)
VeilleButton = Button(ComputerButtonsFrame, image=VeilleImg, relief=RAISED, width=50,height=50)
VeilleButton.pack(side = LEFT)

# Action #

ActionFrame = Frame(window, width=800, height=400,highlightbackground="black", highlightcolor="black", highlightthickness=1, bd=0, bg='light gray')
ActionFrame.config(width=800, height=400)
ActionFrame.pack_propagate(False)
ActionFrame.pack()
#Action - Label
ActionLabel = Label(ActionFrame, text="Actions", bg='light gray')
ActionLabel.config(font=("Courier", 20))
ActionLabel.pack(side = TOP)
#Outis - Frame
ActionOutisFrame = Frame(ActionFrame, width=200, height=300,highlightbackground="black", highlightcolor="black", highlightthickness=1, bd=0, bg='gray')
ActionOutisFrame.config(width=200, height=300)
ActionOutisFrame.pack_propagate(False)
ActionOutisFrame.pack(side = LEFT)
#Clear console - Button
ClearConsole = Button(ActionOutisFrame, text="Effacer la console", relief=RAISED, width=20,height=1, command=clearResult)
ClearConsole.config(font=("Courier", 10))
ClearConsole.pack(side = TOP)
#Message - Button
MessageButton = Button(ActionOutisFrame, text="Envoyer un message", relief=RAISED, width=20,height=1, command=setMessage)
MessageButton.config(font=("Courier", 10))
MessageButton.pack(side = TOP)
#Environ - Button
EnvironButton = Button(ActionOutisFrame, text="Commande 'Environ'", relief=RAISED, width=20,height=1, command=getEnviron)
EnvironButton.config(font=("Courier", 10))
EnvironButton.pack(side = TOP)
#IpInfos - Button
IpInfosButton = Button(ActionOutisFrame, text="Infos", relief=RAISED, width=20,height=1, command=getInfos)
IpInfosButton.config(font=("Courier", 10))
IpInfosButton.pack(side = TOP)
#Flotant - Frame
FlotFrame = Frame(ActionFrame, width=50, height=300, bg='light gray')
FlotFrame.config(width=50, height=300)
FlotFrame.pack_propagate(False)
FlotFrame.pack(side = RIGHT)
#Result - Frame
ResultFrame = Frame(ActionFrame, width=500, height=300, bg='black')
ResultFrame.config(width=500, height=300)
ResultFrame.pack_propagate(False)
ResultFrame.pack(side = RIGHT)
#Result - Label
ResultLabel = Label(ResultFrame, text="Console", bg='black', fg='white')
ResultLabel.config(font=("Courier", 15))
ResultLabel.pack(side = TOP)
#Result - Scroll
Resultscroll=Scrollbar(ResultFrame)
Resultscroll.pack(side=RIGHT, fill=Y)
#Result - Text
Resulttext=Text(ResultFrame, yscrollcommand=Resultscroll.set, bg='black', fg='white')
Resulttext.insert(INSERT, "")
Resulttext.config(state=DISABLED)
Resulttext.pack(side=LEFT, fill=BOTH)
#Suite Result - Scroll
Resultscroll.config(command=Resulttext.yview)

# Perso #

PersoFrame = Frame(window, width= 800, bg='light gray')
PersoFrame.config(width=800, height=100)
PersoFrame.pack_propagate(False)
PersoFrame.pack(side = BOTTOM)
#Perso - Label
PersoLabel = Label(PersoFrame, text="Personnel", bg='light gray')
PersoLabel.config(font=("Courier", 20))
PersoLabel.pack(side = TOP)
#Leave - Button
leaveButton = Button(PersoFrame, text="Quitter", command=window.quit)
leaveButton.pack(side = BOTTOM)

# Fin #

window.mainloop()