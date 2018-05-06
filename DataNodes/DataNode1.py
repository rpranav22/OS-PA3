# -*- coding: utf-8 -*-
import socket
import datetime
import struct
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

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    print("Message length: ", msglen)
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    print("n: ", n)
    data = b''
    while len(data) < n:
        print("Data length in loop: ", len(data))
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
        print("Data length end loop: ", len(data))

    print("Data extracted: ", data)
    print("data length: ", len(data))
    return data

def writeFile(filename, data):
    print("writing file")
    dir = "DataNodes/data/"
    fp = open(dir+filename, 'wb')
    fp.write(data)
    fp.close()

def Main():
    host = '127.0.0.1'
    port = 5005

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
            data = "The data has been stored."
            c.send(data.encode())
            file_data = recv_msg(c)
            writeFile(filename, file_data)
            # files_dict[filename] = file_data.decode()
            c.send("Acknowledgement: Received file data.".encode())
            print("_________________________________________\n")
        elif d[-1:] == "#":
            print("Query received: ", d[:-1])
            filename = d[:-1]
            data = files_dict[filename]
            print("Queried data: ", data)
            c.send(data.encode())
        c.close()

if __name__ == '__main__':
    Main()