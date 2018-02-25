#!/usr/bin/env python3
import json
import re
import socket
import sys
from threading import Thread

import drawing


def my_parse_url(url):
    if (url[:12] != 'pictochat://'):
        return (None, None)
    url = url[12:]
    if (not re.search(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(\:[0-9]{1,4})?\/?$', url)):
        return (None, None)
    foo = url.split(':')
    if (foo[1][-1] == '/'):
        foo[1] = foo[1][:-1]
    return (foo[0], int(foo[1]))


def main(argv):
    if (len(argv) > 2):
        sys.stderr.write('usage: %s [url]' % argv[0])
        sys.exit(1)
    if (len(argv) == 2):
        host, port = my_parse_url(argv[1])
    else:
        host = None
        port = None
    try:
        f = open('config.json', 'r')
        d = json.loads(f.read())
    except FileNotFoundError:
        d = None
    if (host is None or port is None):
        try:
            host = d['host']
        except (TypeError, KeyError):
            host = input('host: ')
        try:
            port = int(d['port'])
        except (TypeError, KeyError, ValueError):
            port = int(input('port: '))
        if (d is None):
            d = {
                'host': host,
                'port': port,
            }
            f = open('config.json', 'w')
            f.write(json.dumps(d))
            f.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except ConnectionRefusedError:
        print('failed to connect to server')
        sys.exit(1)
    print('connected')
    drawing.main(s)


if (__name__ == '__main__'):
    main(sys.argv)
