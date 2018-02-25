#!/usr/bin/env python3
import json
import socket
import sys
from threading import Thread

import drawing


def main():
    try:
        f = open('config.json', 'r')
        d = json.loads(f.read())
        host = d['host']
        port = d['port']
    except FileNotFoundError:
        host = input('host: ')
        port = int(input('port: '))
        d = {
            'host': host,
            'port': port,
        }
        f = open('config.json', 'w')
        f.write(json.dumps(d))
        f.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print('connected')
    drawing.main(s)


if (__name__ == '__main__'):
    main()
