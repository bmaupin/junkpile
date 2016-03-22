#!/usr/bin/env python

import socket, time

serversocket = socket.socket(socket.AF_INET)
serversocket.bind(('localhost', 8080))
serversocket.listen(5)

while True:
    pass

