#!/usr/bin/env python

import sys

# sudo pip3 install piexif
import piexif

if len(sys.argv) < 2:
    sys.stderr.write('ERROR: Must provide a file to remove EXIF tags from\n')
    sys.exit('Usage: {} FILE'.format(sys.argv[0]))

piexif.remove(sys.argv[1])
