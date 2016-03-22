#!/usr/bin/env python
import os
import os.path
import shutil
import sys

import EXIF

source = sys.argv[1]

if not os.path.exists(source):
    sys.exit('Enter a valid source directory\n')

for root, dirs, files in os.walk(source, topdown=False):
    for file in files:
        # only process duplicates
        if file.rsplit('.', 1)[0][-3:] == '(2)':
            original = file.replace('(2)', '', 1)

            d = open(os.path.join(root,file), 'rb')
            dup_tags = EXIF.process_file(d)  
            o = open(os.path.join(root,original), 'rb')
            org_tags = EXIF.process_file(o)          

            if len(dup_tags) == 0:
                print 'deleting duplicate: no tags'
                os.remove(os.path.join(root, file))
                continue
            if len(org_tags) == 0:
                print 'deleting original: no tags'
                os.remove(os.path.join(root, original))
                os.rename(os.path.join(root, file), os.path.join(root, original))
                continue
            if 'EXIF DateTimeOriginal' not in dup_tags and 'Image DateTime' not in dup_tags:
                print 'deleting duplicate: no EXIF DateTimeOriginal and no Image DateTime'
                os.remove(os.path.join(root, file))
                continue
            if 'EXIF DateTimeOriginal' not in org_tags and 'Image DateTime' not in org_tags:
                print 'deleting original: no EXIF DateTimeOriginal and no Image DateTime'
                os.remove(os.path.join(root, original))
                os.rename(os.path.join(root, file), os.path.join(root, original))
                continue
            if 'EXIF DateTimeOriginal' not in dup_tags:
                print 'deleting duplicate: no EXIF DateTimeOriginal'
                os.remove(os.path.join(root, file))
                continue
            if 'EXIF DateTimeOriginal' not in org_tags:
                print 'deleting original: no EXIF DateTimeOriginal'
                os.remove(os.path.join(root, original))
                os.rename(os.path.join(root, file), os.path.join(root, original))
                continue
            if 'Image DateTime' not in dup_tags:
                print 'deleting duplicate: no Image DateTime'
                os.remove(os.path.join(root, file))
                continue
            if 'Image DateTime' not in org_tags:
                print 'deleting original: no Image DateTime'
                os.remove(os.path.join(root, original))
                os.rename(os.path.join(root, file), os.path.join(root, original))
                continue
            if 'Image DateTime' in dup_tags and str(dup_tags['Image DateTime']).find('201') == -1:
                print 'deleting duplicate: Image DateTime improperly formatted'
                os.remove(os.path.join(root, file))
                continue
            if 'Image DateTime' in org_tags and str(org_tags['Image DateTime']).find('201') == -1:
                print 'deleting original: Image DateTime improperly formatted'
                os.remove(os.path.join(root, original))
                os.rename(os.path.join(root, file), os.path.join(root, original))
                continue

            print('duplicate %s still exists' % (file))             


