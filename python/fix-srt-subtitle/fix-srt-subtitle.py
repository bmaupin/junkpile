#!/usr/bin/env python

import optparse
import sys

def main():
    empty_subtitle = '''1
00:00:00,000 --> 00:00:00,001

'''

    parser, infile_name, outfile_name = parse_options()
    
    #if len(sys.argv) < 3:
    #    sys.exit('USAGE: {0} SRT_INFILE SRT_OUTFILE'.format(sys.argv[0]))
    # TODO: with contextlib.closing(urllib2.urlopen(url)) as u:
    infile = open(infile_name) 
    outfile = open(outfile_name, 'w')
    
    ''' 
    Add an empty subtitle at the beginning of the file to fix avconv subtitle 
    offset issues. Also makes sure subtitle numbering starts at 1. Starting at 0
    causes avconv to fail importing the subtitle.
    '''
    outfile.write(empty_subtitle)
    
    # Renumber remaining subtitles
    subtitle_number = 2
    prev_line = ''
    for line in infile: 
        line = line.strip()
        # Optionally reencode subtitles as utf8
        if parser.values.ensure_utf8 == True:
            try:
                line = line.decode('utf8').encode('utf8')
            except UnicodeDecodeError:
                line = line.decode('latin1').encode('utf8')
        if prev_line == '':
            line = str(subtitle_number)
            subtitle_number += 1
        outfile.write('{0}\n'.format(line)) 
        prev_line = line

    outfile.close() 
    infile.close()


def parse_options():
    ''' set up and parse command line arguments
    '''
    
    # define a custom usage message
    usage = ('usage: %prog INPUT_FILE OUTPUT_FILE [options]\n'
    '\tWhere INPUT_FILE = path to SRT input file\n'
    '\tand OUTPUT_FILE = path to SRT output file')
    
    parser = optparse.OptionParser(usage=usage)
    
    # command line options to parse
    parser.add_option(
        '-u', '--ensure-utf8', action='store_true', dest='ensure_utf8', 
        default=False, help='Try to ensure the output file is UTF8-encoded'
    )
    
    # parse the arguments
    (options, args) = parser.parse_args()
    
    if len(args) < 2:
        parser.print_help()
        sys.exit('Error: INPUT_FILE and OUTPUT_FILE are required')
    infile_name = args[0]
    outfile_name = args[1]
    
    return parser, infile_name, outfile_name


if __name__ == '__main__':
    main()
