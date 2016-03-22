#!/usr/bin/env python
import os
import os.path
import shutil
import sys

import EXIF

source = sys.argv[1]
#destination = sys.argv[2]

while not os.path.exists(source):
    source = raw_input('Enter a valid source directory\n')
#while not os.path.exists(destination):
#    destination = raw_input('Enter a valid destination directory\n')

for root, dirs, files in os.walk(source, topdown=False):
     for file in files:
         #extension = os.path.splitext(file)[1][1:].upper()
         
         f = open(os.path.join(root,file), 'rb')
         tags = EXIF.process_file(f)
         
         if 'Image Make' in tags:
             destination_dir = str(tags['Image Make'])
         else:
             destination_dir = 'unknown'
         
         if 'Image Model' in tags:
             destination_subdir = str(tags['Image Model'])
         else:
             destination_subdir = 'unknown'
         
         destination_path = os.path.join(source, destination_dir, destination_subdir)
         
         if not os.path.exists(os.path.join(source, destination_dir)):
             os.mkdir(os.path.join(source, destination_dir))
         
         if not os.path.exists(destination_path):
             os.mkdir(destination_path)
         if os.path.exists(os.path.join(destination_path,file)):
             pass
         else:
             shutil.move(os.path.join(root,file), destination_path)
