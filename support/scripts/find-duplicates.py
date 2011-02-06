#!/usr/bin/env python

# $Id$

'''Use this script to find possible duplicates in the primary arabic words 
source (currently arabic-words.csv)
'''


infile_name = '../words/arabic-words.csv'


def main():
    words = {}
    infile = open(infile_name)
    
    index = 0
    for line in infile:
        index += 1
        line = line.strip()
        english, arabic, arabic2, part, category, gender, aws_chapter = \
            line.split('|')
        words[index] = {}
        words[index]['english'] = english
        words[index]['arabic'] = arabic
        words[index]['arabic2'] = arabic2
        words[index]['gender'] = gender

        for this_index in words:
            if this_index == index:
                continue
            if (english != '' and english == words[this_index]['english']) or \
                (arabic != '' and arabic == words[this_index]['arabic']) or \
                (arabic2 != '' and arabic2 != '\xd9\x88\xd9\x86' and arabic2 != '\xd8\xa7\xd8\xaa' and \
                arabic2 == words[this_index]['arabic2']):
#                if (words[this_index]['gender'] == '' or gender == '') or \
#                    words[this_index]['gender'] == gender:
                print '%s possible duplicate of %s' % (index, this_index)

    infile.close()


if __name__ == '__main__':
    main()
