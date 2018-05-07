import socket
import os
import struct
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print ("\nFile was modified in {}! Please sync again to update your files.\n".format(event))

    def on_created(self, event):
        print("\n{} was modified. Please sync again to update your files.\n".format(event.src_path))




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

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # print("Message length: ", msglen)
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
    dir = 'Files/'
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    print("List of file in {0}: ".format(dir),str(files) )
    # files = ['frame.png', 'test1.txt', 'test3.txt', 'test.txt', 'data.pdf', 'new.mp3']
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


def save_file(filename, data):
    dir = "downloads/"
    fp = open(dir+filename, 'wb')
    fp.write(data)
    print("\nSaved {} in downloads.\n".format(filename))

def Main():
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='Files/', recursive=False)
    observer.start()

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
            res = s.recv(5)
            print("Result: ", res)
            if res.decode() == "True":
                print("Downloading your file...")
                file_data = recv_msg(s)
                print("\n\nDownloaded size: ", len(file_data))
                while True:
                    ch = input("Do you want to save it? (y/n) ")
                    if ch.lower() == "y":
                        save_file(query, file_data)
                        break
                    else:
                        break


            else:
                res = s.recv(5)
                print("Sorry, file could not be found in the server.")
        data = s.recv(1000)
        print (data.decode())
        print("\n____________________________\nClosing connection.\n")
        s.close()
        message = input("Enter command -> ")
        # time.sleep(5)
    # s.close()
    observer.stop()
    observer.join()

if __name__ == '__main__':
    Main()