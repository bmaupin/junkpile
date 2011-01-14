#!/usr/bin/env python

# $Id$

import sys


infile_name = 'arabic-words.txt'
debug = True

diacritics = [u'\u064e',  # fatha, short a
              u'\u064b',  # double fatha
              u'\u0650',  # kasra, short i
              u'\u064d',  # double kasra
              u'\u064f',  # damma, short u
              u'\u064c',  # double damma
              u'\u0652',  # sukkun, nothing
              u'\u0651',  # shedda, double
             ]

# alif = u'\u0627'
# yaa = u'\u064a'
# main arabic block: u'\u0600' - u'\u06ff'
# arabic forms block: u'\ufe70' = u'\ufeff'


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
    '''see here for alternative options:
    http://pythonconquerstheuniverse.wordpress.com/2009/11/12/how-do-i-reverse-a-string-in-python-3/
    like:
    def rev(s): return s[::-1]
    def rev(s): ''.join(reversed(s))
    
    see also:
    http://pyright.blogspot.com/
    
    or google:
    python arabic rtl
    python arabic bidi
    '''
    word = ''
    # convert to raw unicode
    line = line.decode('utf8')
    # go through the line backwards and store it in the word
    while len(line) > 0:
        word += line[-1]
        line = line[:-1]
    return word


def strip_arabic_vowels(line):
    word = ''
    line = line.decode('utf8')
    for char in line:
        if char not in diacritics:
            word += char
    
    return word.encode('utf8')


this_lang = 'arabic'
count = 1
index = 0
words = {}

'''
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
        if line == '' or ( ord(line[0]) < 128 and line[0] != '(' ):
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
        

    if debug:
        print 'line: %s' % (line)
        print 'index: %s' % (index)
        print 'count: %s' % (count)
        print 'this_lang: %s' % (this_lang)
        print 'this_word: %s' % (this_word)
        print

#   DEBUG
    if index == 25:
        break
'''

for line in infile:
    line = line.strip()

    '''
    if line[0] != '(':
        
    
    if line[0] != '(':
        if count > 10:
            count = 1
            if this_lang == 'arabic':
                this_lang = 'english'
                index -= 10
            else:
                this_lang = 'arabic'
    '''
    

    if count > 10:
        if line[0] != '(':
            count = 1
            if this_lang == 'arabic':
                this_lang = 'english'
                index -= 10
            else:
                this_lang = 'arabic'

    if debug:
        print 'line: %s' % (line)
        print 'index: %s' % (index)
        print 'count: %s' % (count)
        print 'this_lang: %s' % (this_lang)
        print

    '''
    if this_lang == 'arabic':
        if line == '' or ord(line[0]) > 127:
            this_word = get_arabic_word(line)
            words[index] = {}
            words[index]['arabic'] = this_word
            count += 1
            index += 1
        elif line[0] == '(':
            if count != 0:
                # drop the parentheses and get the Arabic
                this_word = get_arabic_word(line[1:-1])
                # add the parentheses back
                words[index - 1]['arabic2'] = '(%s)' % (this_word)
        else:
            print 'Error: supposed to be Arabic. line: %s' % (line)
            break
    '''
    
    if this_lang == 'arabic':
        if line == '' or ord(line[0]) > 127:
            words[index] = {}
            words[index]['arabic'] = strip_arabic_vowels(line)
            count += 1
            index += 1
        elif line[0] == '(':
            if count != 0:
                words[index - 1]['arabic2'] = strip_arabic_vowels(line)
        else:
            print 'Error: supposed to be Arabic. line: %s' % (line)
            break

    elif this_lang == 'english':
        if line == '' or ( ord(line[0]) < 128 and line[0] != '(' ):
            if count % 2 == 1:  # count is odd
                words[index + 1]['english'] = line
            else:  # count is even
                words[index - 1]['english'] = line
            count += 1
            index += 1
        elif ord(line[0]) > 127:
            print 'Error: supposed to be English. line: %s' % (line)
            break
        elif line[0] == '(':
            if count % 2 == 1:  # count is odd
                words[index - 2]['english2'] = line
            else:  # count is even
                words[index]['english2'] = line

#   DEBUG
    if index == 111:
        break
 

for index in words:
    sys.stdout.write('%s\t' % (words[index]['arabic']))
    if 'arabic2' in words[index]:
        sys.stdout.write('%s\t' % (words[index]['arabic2']))
    
    if 'english' in words[index]:
        sys.stdout.write('%s\t' % (words[index]['english']))

    if 'english2' in words[index]:
        sys.stdout.write('%s\t' % (words[index]['english2']))
    sys.stdout.write('\n')
print words

# DEBUG
count = 0
for index in words:
#   DEBUG
    count += 1
    if count == 10:
        break
    
    # skip blank words
    if words[index]['english'] == '' and words[index]['arabic'] == '':
        sys.stderr.write('Error: missing translation for word:'
                         '%s' % (words[index]))
    
    if 'english2' in words[index]:
        if words[index]['english2'] == '(m)':
            gender = 'm'
        elif words[index]['english2'] == '(f)':
            gender = 'f'
        else:
            gender = ''
    else:
        gender = ''            
    print '%s|%s|%s' % (words[index]['english'], 
                                words[index]['arabic'],
                                gender)



    
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

'''
TODO:
handle (pl), (m), (f)
handle empty words
    either don't add them to the dict of words, or don't process them later 
    when writing outfile
    clean up augmenting count and index
'''
