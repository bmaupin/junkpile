#!/usr/bin/env python

# $Id$

'''Use this script to remove vowels/diacritics from the primary arabic words 
source (currently arabic-words.csv)
'''


infile_name = '../words/arabic-words.csv'
outfile_name = '../words/arabic-novowels.csv'


def main():
    infile = open(infile_name)
    outfile = open(outfile_name, 'w')
    
    for line in infile:
        line_without_vowels = strip_arabic_vowels(line)
        outfile.write(line_without_vowels)
    
    outfile.close()
    infile.close()


def strip_arabic_vowels(line_with_vowels):
    diacritics = [u'\u064e',  # fatha, short a
                  u'\u064b',  # double fatha
                  u'\u0650',  # kasra, short i
                  u'\u064d',  # double kasra
                  u'\u064f',  # damma, short u
                  u'\u064c',  # double damma
                  u'\u0652',  # sukkun, nothing
                  u'\u0651',  # shedda, double
                 ]
    
    line_without_vowels = ''
    line_with_vowels = line_with_vowels.decode('utf8')
    for char in line_with_vowels:
        if char not in diacritics:
            line_without_vowels += char
    
    return line_without_vowels.encode('utf8')


if __name__ == '__main__':
    main()

