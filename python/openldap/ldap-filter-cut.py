#!/usr/bin/env python

'''
 Copyright (C) 2011 bmaupin <bmaupin@users.noreply.github.com>
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
Takes an OpenLDAP log file, cuts the filters out of it, and writes the unique
filters to a new file.
'''

import re
import sys


def main():
    filters = []
    
    pattern = re.compile('filter="(.*)"')
    
    # the input file is the first argument to this script
    infile_name = sys.argv[1]
    infile = open(infile_name)
    
    for line in infile:
        match = pattern.search(line)
        if match:
            filter = match.group(1)
            
            if filter not in filters:
                filters.append(filter)
        
    infile.close()

    print '%s filters found' % (len(filters))
    
    # the output file is the second argument to this script
    outfile_name = sys.argv[2]
    outfile = open(outfile_name, 'w')

    for filter in filters:
        outfile.write('%s\n' % (filter))
    
    outfile.close()


# calls the main() function when the script runs
if __name__ == '__main__':
    main()
