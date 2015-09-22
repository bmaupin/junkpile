#!/usr/bin/env python
import datetime
import os
import os.path
import re
import sys
import time

import EXIF

source = sys.argv[1]
non_decimal = re.compile(r'[^\d]*')

while not os.path.exists(source):
    source = raw_input('Enter a valid source directory\n')


for root, dirs, files in os.walk(source, topdown=False):
    for file in files:
        print file
        f = open(os.path.join(root, file), 'rb')
        tags = EXIF.process_file(f)

        if 'EXIF DateTimeOriginal' in tags:
            dt = datetime.datetime.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
        elif 'Image DateTime' in tags:
            dt = datetime.datetime.strptime(str(tags['Image DateTime']), '%Y:%m:%d %H:%M:%S')

        '''
        # get the timestamp using the file name
        else:
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
        '''

        '''
        if 'Image Make' in tags:
            if tags['Image Make'].lower() == 'samsung':
                # rename the file using samsung's pattern
                new_filename = '%s.jpg' % (dt.strftime('%Y%m%d_%H%M%S'))
            elif tags['Image Make'].lower() == 'motorola':
                # rename the file using motorola's pattern
                new_filename = 'IMG_%s.jpg' % (dt.strftime('%Y%m%d_%H%M%S'))
            elif tags['Image Make'].lower() == 'htc':
                # rename the file using HTC's pattern
                new_filename = '%s.jpg' % (dt.strftime('%Y-%m-%d_%H.%M.%S'))

            os.rename(os.path.join(root, file), os.path.join(root, new_filename))
        '''

        new_filename = 'IMG_%s.jpg' % (dt.strftime('%Y%m%d_%H%M%S'))
        os.rename(os.path.join(root, file), os.path.join(root, new_filename))
        file = new_filename

        # convert to epoch/unix time
        epoch = time.mktime(dt.timetuple())

        mtime = epoch
        atime = mtime
        times = (atime, mtime)

        os.utime(os.path.join(root,file), times)

