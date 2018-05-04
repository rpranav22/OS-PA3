# -*- coding: utf-8 -*-
import socket
import datetime
import time



class Clients:
    def __init__(self, data, index, addr ):
        self.data = data
        self.index = index
        self.addr = addr

class DataNodes:
    def __init__(self, name, port):
        self.name = name
        self.port = port

host = '127.0.0.1'
DataNode1 = DataNodes('pdf', 5005)
DataNode2 = DataNodes('mp3', 5006)
DataNode3 = DataNodes('txt', 5007)
DataNode4 = DataNodes('other', 5008)

nodes = [DataNode1, DataNode2, DataNode3, DataNode4]

indexdict = {'pdf': [], 'mp3':[], 'txt':[], 'other': []}
filelist = ['data.pdf', 'data.mp3', 'data.txt']

def receive(c):
    while True:

        data = c.recv(1024)
        if not data:
            break
        print ("Data received from client: " + str(data))
        msg="This is in response to {0}.".format(data.decode)

        print ("Sending: " + msg)
        c.send(msg.encode())
    c.close()

def checknode(f):
    f = f.split('.')
    print f
    if f[1] == 'pdf':
        return 0
    elif f[1] == 'mp3':
        return 1
    elif f[1] == 'txt':
        return 2
    else:
        return 3

def assign(filename):
    s = socket.socket()
    index = checknode(filename)
    print(nodes[index].port)
    s.connect((host, nodes[index].port))
    s.send(filename)
    if index == 0:
        indexdict['pdf'].append(filename)
    elif index == 1:
        indexdict['mp3'].append(filename)
    elif index == 2:
        indexdict['txt'].append(filename)
    else:
        indexdict['other'].append(filename)
    a = s.recv(1024).decode()
    print(a)
    s.close()


def Main():


    for file in filelist:
        assign(file)

    print(indexdict)
    nodeData = []
    index = 0

    '''s = socket.socket()
    s.bind((host, port))

    s.listen(5)
    c, addr = s.accept()
    print ("Connection from: " + str(addr) + " at index " + str(index + 1))
    c.send("Connected successfully. Start Syncing now if necessary.".encode())
    while True:
        input = c.recv(4)
        c.close()
        print("Input", input.decode())
        if input.decode() == "sync":
            receive(c)
        elif input.decode() == "quit":
            break

    c.close()'''
    # client = Clients([1,2],)




    # c.send('Talk, CS, Workshop, Economics, History, Fest, Sport, Environment')


if __name__ == '__main__':
    Main()