#!/usr/bin/env python
import os
import os.path
import sys

source = sys.argv[1]

while not os.path.exists(source):
    source = raw_input('Enter a valid source directory\n')


for root, dirs, files in os.walk(source, topdown=False):
     for file in files:
        time_string = file.rsplit('.', 1)[0].rsplit('-', 1)[-1]
        
        mtime = int(time_string[:-3])
        atime = mtime
        times = (atime, mtime)
        
        os.utime(os.path.join(root,file), times)

