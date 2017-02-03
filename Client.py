# -*- coding: utf-8 -*-

import socket
import threading
import getpass

inString = ''
outString = ''
nick = ''

def DealOut(s):
    computername=socket.gethostname()#获取计算机名
    global nick, outString
    while True:
        outString = raw_input(nick+":")
        outString = nick + "@" + computername + ': ' + outString
        s.send(outString)

def DealIn(s):
    global inString
    while True:
        try:
            inString = s.recv(1024)
            if not inString:
                break
            if outString != inString:
                print inString
        except:
            break
        

nick = getpass.getuser()#获取操作系统用户名
ip = "0.0.0.0"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, 5000))
sock.send(nick)

thin = threading.Thread(target = DealIn, args = (sock,))#开辟一个读入的线程
thin.start()
thout = threading.Thread(target = DealOut, args = (sock,))#开辟一个写出的线程
thout.start()

