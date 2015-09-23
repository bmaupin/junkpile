#!/usr/bin/env python

import datetime
import os
import os.path
import struct
import sys

# sudo pip3 install piexif
import piexif


def main():
    EXIF_TIME_FORMAT = '%Y:%m:%d %H:%M:%S'
    EXIF_UNSET = 'unset'
    
    if len(sys.argv) < 2:
        sys.stderr.write('ERROR: Must provide a file to remove EXIF tags from\n')
        sys.exit('Usage: {} FILE'.format(sys.argv[0]))
    
    infile_name = sys.argv[1]

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
    
    exif_dt = EXIF_UNSET
    if exif_dt_location != None:
        exif_dt = datetime.datetime.strptime(exif_data[exif_dt_location][piexif.ImageIFD.DateTime].decode('utf8'), EXIF_TIME_FORMAT)
    else:
        exif_dt_location = '0th'
    
    exif_dtd = EXIF_UNSET
    if piexif.ExifIFD.DateTimeDigitized in exif_data['Exif']:
        exif_dtd = datetime.datetime.strptime(exif_data['Exif'][piexif.ExifIFD.DateTimeDigitized].decode('utf8'), EXIF_TIME_FORMAT)
    
    exif_dto = EXIF_UNSET
    if piexif.ExifIFD.DateTimeOriginal in exif_data['Exif']:
        exif_dto = datetime.datetime.strptime(exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf8'), EXIF_TIME_FORMAT)
    
    print('Exif DateTime is {}'.format(exif_dt))
    print('Exif DateTimeDigitized is {}'.format(exif_dtd))
    print('Exif DateTimeOriginal is {}'.format(exif_dto))

    if infile_mtime != exif_dt or infile_mtime != exif_dtd or infile_mtime != exif_dto:
        response = input('Mismatch between mtime and Exif data. Update Exif (y/n)? ')
        
        if response.lower() == 'y':
            exif_data[exif_dt_location][piexif.ImageIFD.DateTime] = infile_mtime.strftime(EXIF_TIME_FORMAT).encode('utf8')
            exif_data['Exif'][piexif.ExifIFD.DateTimeDigitized] = infile_mtime.strftime(EXIF_TIME_FORMAT).encode('utf8')
            exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal] = infile_mtime.strftime(EXIF_TIME_FORMAT).encode('utf8')
            
            # Write the changes to the file
            piexif.insert(piexif.dump(exif_data), infile_name)

            # Set the atime and mtime of the file back to their original values
            os.utime(infile_name, (infile_mtime_original, infile_mtime_original))


if __name__ == '__main__':
    main()