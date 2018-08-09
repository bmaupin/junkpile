#!/usr/bin/env python3

'''
Generates commands that can be used to restore false positives moved by clamav (e.g. https://lists.gt.net/clamav/users/73374)

Usage:
cat clamav-output.txt | python restore-clamav-false-positives.py
'''

import sys

print('sudo -v')

for line in sys.stdin:
    if line.find('moved to') != -1:
        source, ignore, ignore, destination = line.strip().split()
        source = source[:-1]
        destination = destination[1:-1]
        print('sudo mv {} {}'.format(destination, source))
