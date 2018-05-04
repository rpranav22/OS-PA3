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

def receive(c):
    while True:
        fulltext = b''
        data = c.recv(1)
        while data:
            if data.decode() == '$':
                print("Data received from client: " + fulltext.decode())
                msg = "This is in response to: \n{0}.".format(fulltext.decode())
                c.send(msg.encode())
                return fulltext.decode()
            fulltext += data

            data = c.recv(1)
        if not data:
            break
        print ("Data received from client: " + str(data))
        msg="This is in response to {0}.".format(data.decode())

        print ("Sending(shouldn't be): " + msg)
        # c.send(msg.encode())
    c.close()


def Main():
    host = '127.0.0.1'
    port = 5001


    nodeData=[]
    index =0

    s = socket.socket()
    s.bind((host,port))

    s.listen(5)
    c, addr = s.accept()
    print ("Connection from: " + str(addr) + " at index " + str(index + 1))
    c.send("Connected successfully. Start Syncing now if necessary.".encode())
    cmd = c.recv(4)
    # print(cmd)
    while cmd:
        # c.close()
        print("Input", cmd.decode())
        if cmd.decode() == "sync":
            print("Entering sync")
            filename = receive(c)
            print("filename: ", filename)
            file_data = receive(c)
            print("file data: ", file_data)
        elif cmd.decode() == "quit":
            break
        print("Taking next input...")
        cmd = c.recv(4)


    c.close()
    # client = Clients([1,2],)




    # c.send('Talk, CS, Workshop, Economics, History, Fest, Sport, Environment')


if __name__ == '__main__':
    Main()