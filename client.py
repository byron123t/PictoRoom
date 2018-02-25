#!/usr/bin/env python3
import socket
import sys
from threading import Thread

BUF_SIZE = 4096


def handle_sending(s):
    while (True):
        s.send(input().encode())


def main():
    host = input('host: ')
    port = int(input('port: '))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print('connected')
    Thread(target=handle_sending, args=(s,), daemon=True).start()
    while (True):
        data = s.recv(BUF_SIZE)
        if (not data):
            sys.exit(1)
        print(data.decode())


if (__name__ == '__main__'):
    main()
