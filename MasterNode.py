# -*- coding: utf-8 -*-

import socket
import struct



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

def write_file(file_data):
    print("file data: ", file_data)
    fp = open('recv1.mp3', "wb")
    # file = b''
    for file in str(file_data):
        print(file)
        fp.write(file.encode())

def rec(c):
    data_length = c.recv(20)
    print("Data Length: ", data_length)
    c.send("Received file data size.".encode())
    file_data = c.recv(2 * int(data_length.decode()))
    # file_data = receive(c)
    print("file data: ", file_data)
    c.send("Acknowledgement: Received file data.".encode())
    return file_data.decode()


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
    # print("n: ", n)
    data = b''
    while len(data) < n:
        # print("Data length in loop: ", len(data))
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
        # print("Data length end loop: ", len(data))

    # print("Data extracted: ", data)
    # print("data length: ", len(data))
    return data

def checknode(f):
    print("f: ", f)

    try:
        f = f.split('.')
    except TypeError:
        f = f.decode()
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
        if filename not in indexdict['mp3']:
            indexdict['mp3'].append(filename)
    elif index == 2:
        if filename not in indexdict['txt']:
            indexdict['txt'].append(filename)
    else:
        if filename not in indexdict['other']:
            indexdict['other'].append(filename)

def sendFileData(fp_data, sock):
    data_length = len(fp_data)
    print("OS Data Length: ", data_length)
    msg = struct.pack('>I', int(data_length)) + fp_data
    print("Message: ", msg)
    print("Message length: ", len(msg))
    print("fpData: ", fp_data)
    sock.sendall(msg)

def assign(filename, file_data):
    s = socket.socket()
    index = checknode(filename)
    if filename not in indexdict[nodes[index].name]:
        s.connect((data_host, nodes[index].port))
        filename += "$"
        s.send(filename.encode())
        update_dict(index, filename[:-1])
        a = s.recv(40).decode()
        print(a)
        sendFileData(file_data, s)

    else:
        s.connect((data_host, nodes[index].port))
        s.send(b"nothing")
    a = s.recv(1024).decode()
    print(a)
    s.close()

def retrieve(filename, index):
    s = socket.socket()
    s.connect((data_host, nodes[index].port))
    filename += "#"
    s.send(filename.encode())
    data = recv_msg(s)
    print("Data received from DataNode.")
    s.close()
    return data



def Main():
    host = '127.0.0.1'
    port = 5000
    # GOING TO STArt using SSH
    print("indexDict: ", indexdict)

    index =0
    s = socket.socket()
    s.bind((host,port))


    while True:
        s.listen(1)
        c, addr = s.accept()
        print("Connection from: " + str(addr) + " at index " + str(index + 1))
        c.send("Connected successfully. Start Syncing now if necessary.".encode())
        cmd = c.recv(4)
        print("cmd: ", cmd)

        print("Input", cmd.decode())
        if cmd.decode() == "sync":
            print("Entering sync")
            num = c.recv(3)
            num = int(num.decode())
            print("Number of Files: ", num)
            for i in range(num):
                filename = recv_msg(c)
                c.send("Acknowledgement: Received file data.".encode())
                print("filename: ", filename)
                filename = filename.decode()

                file_data = recv_msg(c)
                assign(filename, file_data)
                c.send("Acknowledgement: Received file data.".encode())


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
        elif cmd.decode() == "retr":
            c.send(b"Enter the file you need: ")
            query = c.recv(20)
            print("Query: ", query.decode())
            index = checknode(query.decode())
            print("Corresponding dict: ", indexdict[nodes[index].name])
            flag = query.decode() in indexdict[nodes[index].name]
            print("search result: ", flag)
            response = "{0}".format(str(flag))
            if flag:
                print("Truee")
                data = retrieve(query.decode(), index)
                final_data = ""
                c.send(response.encode())
                sendFileData(data, c)
            else:
                c.send(response.encode())

            c.send("Retrieval over.".encode())
            print("_____________________________________________\n")


        print("Taking next input...")


        c.close()


    s.close()



if __name__ == '__main__':
    Main()