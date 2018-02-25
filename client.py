#!/usr/bin/env python3
import socket
import sys
from threading import Thread

import drawing


def main():
    host = input('host: ')
    port = int(input('port: '))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print('connected')
    drawing.main(s)


if (__name__ == '__main__'):
    main()
