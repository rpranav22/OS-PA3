import socket


class Node:
    def __init__(self, data):
        self.data = data


def send_filename(filename, sock):
    for ch in filename:
        sock.send(ch.encode())
    sock.send('$'.encode())

def send_fileData(filename, sock):
    dir = 'Files/'
    fp = open(dir + filename, 'rb')
    fp_data = fp.read(1)
    while fp_data:
        print(fp_data)
        sock.send(fp_data)
        fp_data = fp.read(1)
    sock.send('$'.encode())

def sync(sock):
    print("syncing")
    # dir = 'Files/'
    filename = 'test.txt'
    send_filename(filename, sock)
    ack = sock.recv(1024)
    print(ack.decode())
    send_fileData(filename, sock)
    ack = sock.recv(1024)
    print(ack.decode())



def Main():
    host = '127.0.0.2'
    port = 5000

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
        print (str(data))
        message = input("-> ")
    s.close()

if __name__ == '__main__':
    Main()