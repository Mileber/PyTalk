# -*- coding: utf-8 -*-
#!/usr/local/bin/python

import socket
import sys
import threading

con = threading.Condition()
HOST = "0.0.0.0"
PORT = 5000
data = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
s.bind((HOST, PORT))
s.listen(10)
print 'Socket now listening'

def clientThreadIn(conn, nick):#开辟线程
    global data
    while True:#接受客户端数据
        try:
            temp = conn.recv(1024)
            if not temp:
                conn.close()#连接关闭
                return
            NotifyAll(temp)
            print data
        except:
            NotifyAll(nick + " leaves the room!")
            print data
            return


def NotifyAll(sss):#广播
    global data
    if con.acquire():
        data = sss
        con.notifyAll()
        con.release()
 
def ClientThreadOut(conn, nick):#客户端输出
    global data
    while True:
        if con.acquire():
            con.wait()
            if data:
                try:
                    conn.send(data)
                    con.release()
                except:
                    con.release()
                    return
                    

while 1:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    nick = conn.recv(1024)
    NotifyAll('Welcome ' + nick + ' to the room!')
    print data
    print str((threading.activeCount() + 1) / 2) + ' person(s)!'
    conn.send(data)
    threading.Thread(target = clientThreadIn , args = (conn, nick)).start()#开辟线程
    threading.Thread(target = ClientThreadOut , args = (conn, nick)).start()

s.close()
