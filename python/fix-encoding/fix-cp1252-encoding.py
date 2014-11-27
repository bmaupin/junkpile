#!/usr/bin/env python

import sys

def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: {} INFILE OUTFILE'.format(sys.argv[0]))
    
    with open(sys.argv[1], 'r') as infile, open(sys.argv[2], 'w') as outfile:
        for line in infile:
            outfile.write(line.decode("utf-8").encode("windows-1252"))


if __name__ == '__main__':
    main()
