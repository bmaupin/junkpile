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
Generates a password of a specified length given specific character classes
'''


# enables true division; not avaliable until Python 3.0
from __future__ import division

import bisect 
import random
import sys


# change these as necessary:
# minimum password length
min_password_length = 12
# maximum password length
max_password_length = 15
# minimum number of character classes
min_classes = 3
# character classes
# l, I, 1, O, 0 removed for those who still haven't figured out how to copy
# and paste
char_classes = {'lower': 'abcdefghijkmnopqrstuvwxyz',
                'upper': 'ABCDEFGHJKLMNPQRSTUVWXYZ',
                'numbers': '23456789',
                'symbols': '@#$%',
                }
# probabilities that a given character class will be used
class_probs = {'lower': 0.75,
               'upper': 0.05,
               'numbers': 0.1,
               'symbols': 0.1,
               }


def main():
    if min_classes > len(char_classes):
        sys.exit('Error: minimum classes cannot be greater than number of '
                 'available classes')
    if min_classes > max_password_length:
        sys.exit('Error: minimum classes cannot be greater than maximum '
                 'password length')
    
    classes = []
    probabilities = []
    # split the class_probs dict into lists for easier processing
    for class_name in class_probs:
        classes.append(class_name)
        probabilities.append(class_probs[class_name])

    wrg = WeightedRandomGenerator(classes, probabilities)
    
    # use a random password length for more randomness
    password_length = min_password_length + \
        random.choice(range(max_password_length - min_password_length + 1))
    
    password = build_password(wrg, password_length)

    print password


def build_password(wrg, password_length):
    password_chars = []
    used_classes = []
    
    # get all of the characters, leaving a few to make sure we get the minimum
    # number of classes
    for n in range(password_length - min_classes):
        char_class = wrg.next()
        if char_class not in used_classes:
            used_classes.append(char_class)
        
        password_chars.append(random.choice(char_classes[char_class]))
    
    # go through the last few characters
    for n in range(min_classes):
        # if we haven't used the number of minimum classes
        if len(used_classes) < min_classes:
            # go through all the classes
            for char_class in char_classes:
                # find one we haven't used
                if char_class not in used_classes:
                    used_classes.append(char_class)
                    break
        else:
            char_class = wrg.next()
            
        password_chars.append(random.choice(char_classes[char_class]))
    
    # now shuffle it all up for good measure
    random.shuffle(password_chars)
    # and put it all together in a string
    password = ''.join(password_chars)
    
    return password


# based on code from
# http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python
class WeightedRandomGenerator(object):
    def __init__(self, names, weights):
        self.names = names
        self.totals = []
        running_total = 0
        
        for w in weights:
            running_total += w
            self.totals.append(running_total)
    
    def next(self):
        rnd = random.random() * self.totals[-1]
        index = bisect.bisect_right(self.totals, rnd)
        return self.names[index]


# calls the main() function
if __name__=='__main__':
    main()
