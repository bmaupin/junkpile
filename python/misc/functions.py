#!/usr/bin/env python

import socket

def convert_filetime_to_epoch(filetime):
    return (filetime / 10000000) - 11644473600

# Can be used to test connectivity if telnet isn't installed (https://stackoverflow.com/a/33117579/399105)
def test_connectivity(host, port, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print(ex.message)
        return False
