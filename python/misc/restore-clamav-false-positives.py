#!/usr/bin/env python3

'''
Generates commands that can be used to restore false positives moved by clamav (e.g. https://lists.gt.net/clamav/users/73374)
'''

import sys

if sys.stdin.isatty():
    sys.exit('Usage: cat clamav-output.txt | python restore-clamav-false-positives.py')

print('# Enter these commands to restore false positives:')
print('sudo -v')

for line in sys.stdin:
    if line.find('moved to') != -1:
        source, destination = line.split('moved to')
        source = source.strip()
        # Drop the colon
        source = source[:-1]
        destination = destination.strip()
        # Drop the beginning and end single quotes
        destination = destination[1:-1]
        print('sudo mv {} {}'.format(destination, source))
