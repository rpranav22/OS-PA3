import socket


class Node:
    def __init__(self, data):
        self.data = data

def sync(socket):
    print("syncing")
    fp = open('Files/test.txt', 'rb')
    fp_data = fp.read(1024)
    while fp_data:
        print(fp_data)
        socket.send(fp_data)
        fp_data = fp.read(1024)


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
        if str(message) == "sync":
            sync(s)
        data = s.recv(1024)
        print (str(data))
        message = input("-> ")
    s.close()

if __name__ == '__main__':
    Main()