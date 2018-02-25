#!/usr/bin/env python3
import socket
from threading import Thread

HOST = '0.0.0.0'

PORT = 8000

BUF_SIZE = 1048576

socket_list = []


def handle_client(client, addr):
    while (True):
        data = client.recv(BUF_SIZE)
        if (not data):
            print('%s disconnected' % str(addr))
            socket_list.remove(client)
            client.close()
            return
        print('%s: %s' % (str(addr), data.decode()))
        for s in socket_list:
            s.send(data)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print('accepting connections')
    while True:
        client, addr = s.accept()
        print('%s connected' % str(addr))
        socket_list.append(client)
        Thread(target=handle_client, args=(client, addr), daemon=True).start()


if (__name__ == '__main__'):
    main()
