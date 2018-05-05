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

data_host = '127.0.0.1'
DataNode1 = DataNodes('pdf', 5005)
DataNode2 = DataNodes('mp3', 5006)
DataNode3 = DataNodes('txt', 5007)
DataNode4 = DataNodes('other', 5008)

nodes = [DataNode1, DataNode2, DataNode3, DataNode4]

indexdict = {'pdf': [], 'mp3':[], 'txt':[], 'other': []}
filelist = ['data.pdf', 'data.mp3', 'data.txt']


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
def rec(c):
    data_length = c.recv(20)
    print("Data Length: ", data_length)
    c.send("Received file data size.".encode())
    file_data = c.recv(2 * int(data_length.decode()))
    # file_data = receive(c)
    print("file data: ", file_data)
    c.send("Acknowledgement: Received file data.".encode())
    return file_data.decode()


def checknode(f):
    f = f.split('.')
    # print (f)
    if f[1] == 'pdf':
        return 0
    elif f[1] == 'mp3':
        return 1
    elif f[1] == 'txt':
        return 2
    else:
        return 3

def update_dict(index, filename):
    if index == 0:
        if filename not in indexdict['pdf']:
            indexdict['pdf'].append(filename)
    elif index == 1:
        if filename not in indexdict['pdf']:
            indexdict['mp3'].append(filename)
    elif index == 2:
        if filename not in indexdict['pdf']:
            indexdict['txt'].append(filename)
    else:
        if filename not in indexdict['pdf']:
            indexdict['other'].append(filename)

def assign(filename):
    s = socket.socket()
    index = checknode(filename)
    # print(nodes[index].port)
    if filename not in indexdict[nodes[index].name]:
        s.connect((data_host, nodes[index].port))
        s.send(filename.encode())
        update_dict(index, filename)
    else:
        s.connect((data_host, nodes[index].port))
        s.send(b"nothing")
    a = s.recv(1024).decode()
    print(a)
    s.close()



def Main():
    host = '127.0.0.1'
    port = 5000
    # GOING TO STArt using SSH
    print("indexDict: ", indexdict)

    index =0
    s = socket.socket()
    s.bind((host,port))

    # s.listen(1)
    # c, addr = s.accept()
    # print ("Connection from: " + str(addr) + " at index " + str(index + 1))
    # c.send("Connected successfully. Start Syncing now if necessary.".encode())
    # cmd = c.recv(4)
    # print(cmd)
    while True:
        s.listen(1)
        c, addr = s.accept()
        print("Connection from: " + str(addr) + " at index " + str(index + 1))
        c.send("Connected successfully. Start Syncing now if necessary.".encode())
        cmd = c.recv(4)
        # while cmd == b"":
        #     cmd = c.recv(4)
        print("cmd: ", cmd)
        # c.close()
        print("Input", cmd.decode())
        if cmd.decode() == "sync":
            print("Entering sync")
            num = c.recv(3)
            num = int(num.decode())
            print("Number of Files: ", num)
            for i in range(num):
                filename = rec(c)
                print("filename: ", filename)
                assign(filename)
                # print("Final index: ", indexdict)
                file_data = rec(c)
                # file_data = receive(c)
                print("file data: ", file_data)

                print("_____________________________________________\n")
            c.send(b"Your data has been synced.")
        elif cmd.decode() == "quit":
            break
        elif cmd.decode() == "qury":
            send = str(indexdict)
            c.send(send.encode())
            print("sent: ", send)
        elif cmd == b"":
            break


        print("Taking next input...")


        # print("cmd: ", cmd)

        c.close()
    # client = Clients([1,2],)


    s.close()

    # c.send('Talk, CS, Workshop, Economics, History, Fest, Sport, Environment')


if __name__ == '__main__':
    Main()