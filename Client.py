import socket
import os
import struct




class Node:
    def __init__(self, data):
        self.data = data

def send_filename(filename, sock):
    data_length = str(len(filename.encode()))
    print("Data Length: ", data_length)
    length_pad = data_length
    for i in range (20 - len(data_length)):
        length_pad = '0' + data_length

    msg = struct.pack('>I', int(length_pad)) + filename.encode()
    print("Message: ", msg)
    print("Message length: ", len(msg))

    sock.sendall(msg)


def send_fileData(filename, sock):
    dir = 'Files/'

    fp = open(dir + filename, 'rb')
    fp_data = fp.read()
    data_length = str(os.path.getsize(dir+filename))
    length_pad = data_length
    for i in range(20 - len(data_length)):
        data_length = '0' + data_length
    print("Data Length: ", data_length)
    print("OS Data Length: ", data_length)
    msg = struct.pack('>I', int(length_pad)) + fp_data

    print("Message: ", msg)
    print("Message length: ", msg)
    print("fpData: ", fp_data)
    sock.sendall(msg)

def sync(sock):
    print("syncing")
    # dir = 'Files/'
    filename = 'test.txt'
    files = ['frame.png', 'test1.txt', 'test3.txt', 'test.txt', 'data.pdf', 'new.mp3']
    num = len(files)
    num = str(num)
    print("Numfiles: ", num)
    for i in range (3 - len(num)):
        num = '0' + num
    print("Final num: ", num)
    sock.send(num.encode())
    for filename in files:
        send_filename(filename, sock)
        ack = sock.recv(36)
        print(ack.decode())
        send_fileData(filename, sock)
        ack = sock.recv(36)
        print(ack.decode())
        print("__________________________________________\n")




def Main():
    host = '127.0.0.2'
    port = 5000


    print("The server has started. Type sync to connect and get started.")
    message = input("-> ")
    while message != 'q':
        s = socket.socket()
        s.connect(('127.0.0.1', port))
        conn = s.recv(60)
        print(conn.decode())
        s.send(message.encode())
        if str(message) == "sync":
            sync(s)
        elif str(message) == "quit":
            break
        elif str(message) == "retr":
            req = s.recv(30)
            print(req.decode())
            query = input(req.decode())
            s.send(query.encode())
        data = s.recv(1000)
        print (data.decode())
        print("\n____________________________\nClosing connection.\n")
        s.close()
        message = input("-> ")
        # time.sleep(5)
    s.close()

if __name__ == '__main__':
    Main()