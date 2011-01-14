#!/usr/bin/env python

# $Id$

import sys


infile_name = 'arabic-words.txt'

infile = open(infile_name)

'''
index = 0
count = 0
this_lang = None
this_word = None
words = {}

for line in infile:
    # drop the newline character
    line = line.strip()
    
    if line[0] == '(':
        if this_lang == 'arabic':
            # drop the parentheses and get the Arabic
            this_word = get_arabic_word(line[1:-1])
            # add the parentheses back
            words[index]['arabic2'] = '(%s)' % (this_word)
        elif this_lang == 'english':
            words[index]['english2'] = line
            
        index += 1
    if ord(line[0]) > 127:
        this_lang = 'arabic'
        this_word = get_arabic_word(line)
        words[index] = {}
        words[index]['arabic'] = this_word
    else:
        this_lang = 'english'
        this_word = get_english_word(line)
    
    
#   DEBUG
    if count == 10:
        break
'''

def get_arabic_word(line):
#def gaw(line):
    word = ''
    # convert to raw unicode
    line = line.decode('utf8')
    # go through the line backwards and store it in the word
    while len(line) > 0:
        word += line[-1]
        line = line[:-1]
    return word

this_lang = 'arabic'
count = 1
index = 0
words = {}

for line in infile:
    line = line.strip()

    if this_lang == 'arabic':
        if line == '' or ord(line[0]) > 127:
            this_word = get_arabic_word(line)
            words[index] = {}
            words[index]['arabic'] = this_word
            count += 1
            index += 1
            if count > 10:
                count = 1
                this_lang = 'english'
                index -= 10
        elif line[0] == '(':
            # drop the parentheses and get the Arabic
            this_word = get_arabic_word(line[1:-1])
            # add the parentheses back
            words[index - 1]['arabic2'] = '(%s)' % (this_word)
        else:
            print 'Error: supposed to be Arabic. line: %s' % (line)
            break

    elif this_lang == 'english':
        if line == '' or ( ord(line[0]) < 128 and line != '(' ):
            this_word = line
            if count % 2 == 1:  # count is odd
                words[index + 1]['english'] = this_word
            else:  # count is even
                words[index - 1]['english'] = this_word
            count += 1
            index += 1
            if count > 10:
                count = 1
                this_lang = 'arabic'
        elif ord(line[0]) > 127:
            print 'Error: supposed to be English. line: %s' % (line)
            break
        elif line[0] == '(':
            if count % 2 == 1:  # count is odd
                words[index - 2]['english2'] = line
            else:  # count is even
                words[index]['english2'] = line
        '''
        else:
            this_word = line
            if count % 2 == 1:  # count is odd
                words[index + 1]['english'] = this_word
            else:  # count is even
                words[index - 1]['english'] = this_word
            count += 1
            index += 1
            if count > 10:
                count = 1
                this_lang = 'arabic'
        '''

#   DEBUG
    if index == 25:
        break

for index in words:
    sys.stdout.write('%s\t' % (words[index]['arabic'].encode('utf8')))
    if 'arabic2' in words[index]:
        sys.stdout.write('%s\t' % (words[index]['arabic2'].encode('utf8')))
    
    if 'english' in words[index]:
        sys.stdout.write('%s\t' % (words[index]['english']))

    if 'english2' in words[index]:
        sys.stdout.write('%s\t' % (words[index]['english2']))
    sys.stdout.write('\n')
print words



    
'''
class Word(object):
    def __init__(self, text):
        self.text = text
'''

'''
def main():
    
    

if __name__ == '__main__':
    main()
'''
