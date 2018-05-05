import socket

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
    for ch in filename:
        sock.send(ch.encode())
    sock.send('$'.encode())

def send_fileData(filename, sock):
    dir = 'Files/'
    # text = getPDFContent(dir + filename)
    # send_filename(text)
    fp = open(dir + filename, 'rb')
    fp_data = fp.read(1)
    while fp_data:
        # print(fp_data)
        sock.send(fp_data)
        fp_data = fp.read(1)
    sock.send('$'.encode())

def sync(sock):
    print("syncing")
    # dir = 'Files/'
    filename = 'test.txt'
    files = ['test.txt', 'test1.txt', 'test3.txt', 'data.pdf', 'test.mp3']
    num = len(files)
    num = str(num)
    print("Numfiles: ", num)
    for i in range (3 - len(num)):
        num = '0' + num
    print("Final num: ", num)
    sock.send(num.encode())
    for filename in files:
        send_filename(filename, sock)
        ack = sock.recv(1024)
        print(ack.decode())
        # send_fileData(filename, sock)
        # ack = sock.recv(1024)
        # print(ack.decode())




def Main():
    host = '127.0.0.2'
    port = 5001

    s = socket.socket()
    s.connect(('127.0.0.1', port))
    # s.send(data)
    conn = s.recv(1024)
    print(conn.decode())
    # s.send({"Data": data})

    message = input("-> ")
    while message != 'q':
        s.send(message.encode())
        if str(message) == "sync":
            sync(s)
        data = s.recv(1024)
        print("_____________________________________\n")
        print (data.decode())
        message = input("-> ")
    s.close()

if __name__ == '__main__':
    Main()