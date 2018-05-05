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

files_list = []
files_dict = {}
def Main():
    host = '127.0.0.1'
    port = 5008

    index =0

    s = socket.socket()
    s.bind((host,port))

    while True:
        s.listen(1)
        c, addr = s.accept()
        print("Connection from: " + str(addr) + " at index " + str(index + 1))
        d = c.recv(1024)
        d = d.decode()
        if(d == "nothing"):
            c.send(b"nothing")
            c.close()
            continue
        elif d[-1:] == "$":
            print("Data received: ", d[:-1])
            filename = d[:-1]
            files_list.append(filename)
            files_dict[filename] = "dummy data"
            data = "The data has been stored."
            c.send(data.encode())
        elif d[-1:] == "#":
            print("Query received: ", d[:-1])
            filename = d[:-1]
            data = files_dict[filename]
            print("Queried data: ", data)
            c.send(data.encode())
        c.close()

if __name__ == '__main__':
    Main()