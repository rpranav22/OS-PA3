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
    port = 5005


    nodeData=[]
    index =0

    s = socket.socket()
    s.bind((host,port))

    s.listen(1)
    c, addr = s.accept()
    print ("Connection from: " + str(addr) + " at index " + str(index + 1))
    while True:
        d =c.recv(1024)
        print("Data received: ", d.decode())
        data = "The data has been stored."
        c.send(data.encode())

    c.close()

if __name__ == '__main__':
    Main()