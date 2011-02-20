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

        # find all variations of standalone lam-alef character
        if '\xef\xbb\xb9' in arabic or '\xef\xbb\xb9' in arabic2 \
            or '\xef\xbb\xb7' in arabic or '\xef\xbb\xb7' in arabic2 \
            or '\xef\xbb\xb5' in arabic or '\xef\xbb\xb5' in arabic2 \
            or '\xef\xbb\xbb' in arabic or '\xef\xbb\xbb' in arabic2:
        # find words with standalone hamza character
#        if '\xd8\xa1' in arabic or '\xd8\xa1' in arabic2:
        # find words with dash (prefixes)
#        if '\xd9\x80\xd9\x80' in arabic2:
        # find words less than a certain length
#        if len(arabic) < 7:
            print '%s:\t%s' % (index, line)

    infile.close()


if __name__ == '__main__':
    main()
