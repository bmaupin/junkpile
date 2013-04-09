#!/usr/bin/env python

'''
 Copyright (C) 2012 Bryan Maupin <bmaupincode@gmail.com>
 
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

''' Takes an input text file and spits out an html table
'''

import sys


# whether or not the first row in the input file is a table header row
header_row = False
# separator between table cells
cell_separator = '\t'


def main():
    table_contents = []
    
    if len(sys.argv) < 2:
        sys.exit('USAGE: %s input_file' % (sys.argv[0]))
        
    infile = open(sys.argv[1])
    
    for line in infile:
        # remove newline
        line = line.strip()
        # skip blank lines
        if line == '':
            continue
        table_contents.append(line.split(cell_separator))
    
    infile.close()
    
#    print table_contents
    
    print to_table(table_contents)


def to_table(table_contents):
    table_html = '<table>\n'
    
    if header_row:
        table_html += '  <tr>\n'
        for cell in table_contents.pop(0):
            table_html += '    <th>%s</th>\n' % (cell)
        table_html += '  </tr>\n'
    
    while len(table_contents) > 0:
        table_html += '  <tr>\n'
        for cell in table_contents.pop(0):
            table_html += '    <td>%s</td>\n' % (cell)
        table_html += '  </tr>\n'
    
    table_html += '</table>\n'
    
    return table_html


# calls the main() function when the script runs
if __name__ == '__main__':
    main()
