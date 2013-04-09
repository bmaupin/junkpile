#!/usr/bin/env python
import datetime
import os
import os.path
import re
import sys
import time

source = sys.argv[1]
non_decimal = re.compile(r'[^\d]*')

while not os.path.exists(source):
    source = raw_input('Enter a valid source directory\n')


for root, dirs, files in os.walk(source, topdown=False):
     for file in files:
        # drop the extension
        time_string = file.rsplit('.', 1)[0]
        # strip non-numeric characters
        time_string = non_decimal.sub('', time_string)
        # chop off any extra characters
        if len(time_string) > 14:
            time_string = time_string[:14]

        if not time_string.startswith('20'):
            sys.stderr.write('ERROR: error parsing filename %s\n' % (file))
            sys.stderr.write('\ttime_string: %s\n' % (time_string))
            continue

        # convert to datetime
        dt = datetime.datetime.strptime(time_string, '%Y%m%d%H%M%S')
        # convert to epoch/unix time
        epoch = time.mktime(dt.timetuple())

        mtime = epoch
        atime = mtime
        times = (atime, mtime)

        os.utime(os.path.join(root,file), times)

