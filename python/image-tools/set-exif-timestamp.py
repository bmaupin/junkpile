#!/usr/bin/env python

import datetime
import optparse
import os
import os.path
import struct
import sys

# sudo pip3 install piexif
import piexif


def main():
    def set_exif_timestamp(dt_to_set):
        print('Setting Exif timestamp to {}'.format(dt_to_set))
        
        exif_data[exif_dt_location][piexif.ImageIFD.DateTime] = dt_to_set.strftime(EXIF_TIME_FORMAT).encode('utf8')
        exif_data['Exif'][piexif.ExifIFD.DateTimeDigitized] = dt_to_set.strftime(EXIF_TIME_FORMAT).encode('utf8')
        exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal] = dt_to_set.strftime(EXIF_TIME_FORMAT).encode('utf8')
        
        # Write the changes to the file
        piexif.insert(piexif.dump(exif_data), infile_name)

        # Set the atime and mtime of the file back to their original values
        os.utime(infile_name, (infile_mtime_original, infile_mtime_original))
    
    
    EXIF_TIME_FORMAT = '%Y:%m:%d %H:%M:%S'
    EXIF_UNSET = 'unset'
    
    infile_name = parse_options()

    # Get the mtime of the file
    infile_mtime_original = os.path.getmtime(infile_name)
    # Drop the microsecond because it won't be stored in Exif and the comparison won't be accurate
    infile_mtime = datetime.datetime.fromtimestamp(infile_mtime_original).replace(microsecond=0)
    
    print('File mtime is {}'.format(infile_mtime))

    try:
        exif_data = piexif.load(infile_name)
    except struct.error:
        exif_data = {'0th': {}, '1st': {}, 'Exif': {}}
    
    exif_dt_location = None
    if piexif.ImageIFD.DateTime in exif_data['0th']:
        exif_dt_location = '0th'
    elif piexif.ImageIFD.DateTime in exif_data['1st']:
        exif_dt_location = '1st'
    
    # DateTime is when the image was last changed
    exif_dt = EXIF_UNSET
    if exif_dt_location != None:
        # I've seen timestamp values that look like this: '    :  :     :  :  '
        try:
            exif_dt = datetime.datetime.strptime(exif_data[exif_dt_location][piexif.ImageIFD.DateTime].decode('utf8'), EXIF_TIME_FORMAT)
        except ValueError as e:
            sys.stderr.write('WARNING: Malformed DateTime\n')
            sys.stderr.write('\tValueError: {}\n'.format(e))
    else:
        exif_dt_location = '0th'
    
    # DateTimeDigitized is when the image was stored digitally (may be different from DateTimeOriginal if image was scanned)
    exif_dtd = EXIF_UNSET
    if piexif.ExifIFD.DateTimeDigitized in exif_data['Exif']:
        try:
            exif_dtd = datetime.datetime.strptime(exif_data['Exif'][piexif.ExifIFD.DateTimeDigitized].decode('utf8'), EXIF_TIME_FORMAT)
        except ValueError as e:
            sys.stderr.write('WARNING: Malformed DateTimeDigitized\n')
            sys.stderr.write('\tValueError: {}\n'.format(e))
    
    # DateTimeOriginal is when the image was taken
    exif_dto = EXIF_UNSET
    if piexif.ExifIFD.DateTimeOriginal in exif_data['Exif']:
        try:
            exif_dto = datetime.datetime.strptime(exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf8'), EXIF_TIME_FORMAT)
        except ValueError as e:
            sys.stderr.write('WARNING: Malformed DateTimeOriginal\n')
            sys.stderr.write('\tValueError: {}\n'.format(e))
    
    # If only the Exif DateTime isn't set, set it based on DateTimeOriginal
    if exif_dt == EXIF_UNSET and exif_dtd != EXIF_UNSET and exif_dto != EXIF_UNSET and exif_dtd == exif_dto:
        set_exif_timestamp(exif_dto)
        exif_dt = exif_dto
    
    print('Exif DateTime is {}'.format(exif_dt))
    print('Exif DateTimeDigitized is {}'.format(exif_dtd))
    print('Exif DateTimeOriginal is {}'.format(exif_dto))

    if parser.values.set is not None:
        user_dt = datetime.datetime.strptime(parser.values.set, '%Y-%m-%d %H:%M:%S')
        set_exif_timestamp(user_dt)
        sys.exit()

    if parser.values.force == False:
        # If all the Exif values are the same and the mtime difference is within a day, don't do anything
        if exif_dto != EXIF_UNSET and exif_dt == exif_dtd and exif_dtd == exif_dto and \
            abs((infile_mtime - exif_dto).total_seconds()) < 86400:
                sys.exit()

    if parser.values.force == True or \
            exif_dt == EXIF_UNSET or exif_dtd == EXIF_UNSET or exif_dto == EXIF_UNSET or \
            infile_mtime < exif_dt or infile_mtime < exif_dtd or infile_mtime < exif_dto:
        if parser.values.force == False:
            print('Mismatch between mtime and Exif data.')
        
        print('\t1. Set Exif timestamp to mtime\n'
            '\t2. Specify date/time')
        
        # If any of the Exif timestamps aren't set
        for exif_timestamp in [exif_dto, exif_dt, exif_dtd]:
            if exif_timestamp != EXIF_UNSET:
                break

        if exif_timestamp != EXIF_UNSET:
            print('\t3. Set all Exif timestamps to {}'.format(exif_timestamp))
            
        response = input('\tChoice? (press Enter to do nothing) ')
        
        if response == '1':
            set_exif_timestamp(infile_mtime)
            
        elif response == '2':
            user_dt_string = input('Please enter a timestamp (YYYY-mm-dd HH:MM:SS): ')
            user_dt = datetime.datetime.strptime(user_dt_string, '%Y-%m-%d %H:%M:%S')
            
            set_exif_timestamp(user_dt)
        
        elif response == '3':
            if exif_timestamp != EXIF_UNSET:
                set_exif_timestamp(exif_timestamp)


def parse_options():
    ''' set up and parse command line arguments
    '''

    global parser
    
    usage = ('Usage: %prog FILE [options]\n'
            'Where FILE = full path to jpeg file to remove EXIF tags from')
    
    parser = optparse.OptionParser(usage=usage)
    
    # command line options to parse
    parser.add_option('--force', action='store_true', dest='force',
            default=False, help='Force update of Exif timestamp')
    parser.add_option('-s', '--set', dest='set',
            help='Set Exif timestamps to a specific time (YYYY-mm-dd HH:MM:SS)')
    
    # parse the arguments
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        sys.exit('Error: FILE is required')
    
    return args[0]


if __name__ == '__main__':
    main()