#!/usr/bin/env python

import os
import os.path
import sys

# sudo pip3 install piexif
import piexif

if len(sys.argv) < 2:
    sys.stderr.write('ERROR: Must provide a file to remove EXIF tags from\n')
    sys.exit('Usage: {} FILE'.format(sys.argv[0]))

# Get the mtime of the file
infile_mtime_original = os.path.getmtime(sys.argv[1])

# Remove all Exif metadata
piexif.remove(sys.argv[1])

# Set the atime and mtime of the file back to their original values
os.utime(sys.argv[1], (infile_mtime_original, infile_mtime_original))
