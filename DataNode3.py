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


def Main():
    host = '127.0.0.1'
    port = 5007


    nodeData=[]
    index =0

    s = socket.socket()
    s.bind((host,port))

    s.listen(5)
    c, addr = s.accept()
    print ("Connection from: " + str(addr) + " at index " + str(index + 1))
    d = c.recv(1024)
    print(d)
    data = "received"
    c.send(data.encode())
    # client = Clients([1,2],)




    # c.send('Talk, CS, Workshop, Economics, History, Fest, Sport, Environment')
    '''while True:

        data = c.recv(1024)
        if not data:
            break
        print ("Request received from client: " + str(data))
        msg="This is in response to {0}.".format(data.decode)

        print ("Sending: " + msg)
        c.send(msg)'''
    c.close()

if __name__ == '__main__':
    Main()