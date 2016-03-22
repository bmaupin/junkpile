#!/usr/bin/env python

import datetime
import optparse
import os
import os.path
import struct
import sys

# sudo pip3 install piexif
import piexif


# Make this negative to subtract time, e.g.:
# -datetime.timedelta(hours=5, minutes=9)
#TIME_ADJUSTMENT = datetime.timedelta(hours=5, minutes=9)
#TIME_ADJUSTMENT = datetime.timedelta(days=1)
TIME_ADJUSTMENT = datetime.timedelta(days=788, seconds=13032)


def main():
    EXIF_TIME_FORMAT = '%Y:%m:%d %H:%M:%S'
    EXIF_UNSET = 'unset'
    
    infile_name = parse_options()
    
    # Get the mtime of the file
    infile_mtime_original = os.path.getmtime(infile_name)

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

    new_exif_dt = exif_dt + TIME_ADJUSTMENT
    new_exif_dtd = exif_dtd + TIME_ADJUSTMENT
    new_exif_dto = exif_dto + TIME_ADJUSTMENT

    print('\nNew values:')
    print('Exif DateTime: {}'.format(new_exif_dt))
    print('Exif DateTimeDigitized: {}'.format(new_exif_dtd))
    print('Exif DateTimeOriginal: {}'.format(new_exif_dto))
    
    if parser.values.yes:
        response = 'y'
    else:
        response = input('\nProceed? (y/n) ')
        
    
    if response.lower() == 'y': 
        exif_data[exif_dt_location][piexif.ImageIFD.DateTime] = new_exif_dt.strftime(EXIF_TIME_FORMAT).encode('utf8')
        exif_data['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_exif_dtd.strftime(EXIF_TIME_FORMAT).encode('utf8')
        exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_exif_dto.strftime(EXIF_TIME_FORMAT).encode('utf8')
        
        # Write the changes to the file
        piexif.insert(piexif.dump(exif_data), infile_name)

        # Set the atime and mtime of the file back to their original values
        os.utime(infile_name, (infile_mtime_original, infile_mtime_original))


def parse_options():
    ''' set up and parse command line arguments
    '''

    global parser
    
    usage = ('Usage: %prog FILE [options]\n'
            'Where FILE = full path to jpeg file to adjust EXIF tags')
    
    parser = optparse.OptionParser(usage=usage)
    
    # command line options to parse
    parser.add_option('-y', '--yes', action='store_true', dest='yes',
            default=False, help='Adjust files without asking for confirmation')
    
    # parse the arguments
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        sys.exit('Error: FILE is required')
    
    return args[0]


if __name__ == '__main__':
    main()
