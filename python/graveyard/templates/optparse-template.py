#!/usr/bin/env python

from optparse import OptionParser
import sys

def main():
    parse_options()
    
    # this is how you check whether an option has been set
    if parser.values.log_file_name != None:
        sys.stdout = Logger(parser.values.log_file_name)


def parse_options():
    ''' Set up and parse command line arguments
    Requires: nothing
    Returns: nothing
    '''
    
    global infile_name, parser
    
    # define a custom usage message
    usage = ('usage: %prog INPUT_FILE [options]\n'
    'Where INPUT_FILE = full path to input file')
    
    # create the parser, using the custom usage message
    parser = OptionParser(usage=usage)
    # use parser = OptionParser() if you don't have a custom usage message
    
    # command line options to parse
    parser.add_option('--debug', action='store_true', dest='debug',
            default=False, help='show debugging messages')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
            default=False, help='verbose logging')
    parser.add_option('-l', '--log', dest='log_file_name',
            help='also write output to log file (will still output to screen)')
    
    # parse the arguments
    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        parser.print_help()
        sys.exit('Error: INPUT_FILE is required')
    infile_name = args[0]


# calls the main() function when the script runs
if __name__ == '__main__':
    main()
