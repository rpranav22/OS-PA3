import socket
import time
# import pyPdf



class Node:
    def __init__(self, data):
        self.data = data

def getPDFContent(path):
    content = ""
    num_pages = 1
    p = open(path, "rb")
    pdf = pyPdf.pdf.PdfFileReader(p)
    for i in range(0, num_pages):
        content += pdf.getPage(i).extractText() + "\n"
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content

def send_filename(filename, sock):
    data_length = str(len(filename.encode()))
    print("Data Length: ", data_length)
    if(len(data_length) >= 100):
        for i in range(1000 - len(data_length)):
            data_length = '0' + data_length
    for i in range (20 - len(data_length)):
        data_length = '0' + data_length


    sock.send(str(data_length).encode())
    ack = sock.recv(24)
    print(ack)
    sock.send(filename.encode())
    # print("fpData: ", fp_data)

def send_fileData(filename, sock):
    dir = 'Files/'
    # text = getPDFContent(dir + filename)
    # send_filename(text)
    fp = open(dir + filename, 'rb')
    fp_data = fp.read()
    data_length = str(len(fp_data))
    if (len(data_length) >= 100):
        for i in range(1000 - len(data_length)):
            data_length = '0' + data_length
    for i in range(20 - len(data_length)):
        data_length = '0' + data_length
    print("Data Length: ", data_length)
    sock.send(str(data_length).encode())
    ack = sock.recv(24)
    print( ack)
    print("fpData: ", fp_data)
    sock.send(fp_data)
    # while fp_data:
    #     # print(fp_data)
    #     sock.send(fp_data)
    #     fp_data = fp.read(1)
    # sock.send('$'.encode())

def sync(sock):
    print("syncing")
    # dir = 'Files/'
    filename = 'test.txt'
    files = ['3bit.deb', 'test1.txt', 'test3.txt', 'test.txt']
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

    # s = socket.socket()
    # s.connect(('127.0.0.1', port))
    # conn = s.recv(60)
    # print(conn.decode())
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
        data = s.recv(100)
        print (data.decode())
        print("\n____________________________\nClosing connection.\n")
        s.close()
        message = input("-> ")
        # time.sleep(5)
    s.close()

if __name__ == '__main__':
    Main()