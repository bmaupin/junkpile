#!/usr/bin/env python
# coding=utf8

import os
import os.path
import re
import sys

if sys.version_info < (3, 4):
    sys.exit('ERROR: Requires Python 3.4')

from enum import Enum

def main():
    VideoTypes = Enum('VideoType', 'emission film miniserie')
    filename_chars = 'àÀâÂçÇéÉèÈêÊëîÎôÔ\w\-\'\.\(\)'
    pattern = re.compile('([{0}]+)\.(S([\d]+)E[\d]+)\.([{0}]+)\.[\d]+kbps\.ts'.format(filename_chars))
#    pattern = re.compile('([{0}]+)\.(S[\d]+E[\d]+)\.([{0}]+)'.format(filename_chars))
    
    files_to_rename = {}
    video_type = None

    def parse_filename(filename):
        nonlocal video_type
    
        match = pattern.search(filename)
        if match:
            show = match.group(1).replace('.', ' ')
            episode = match.group(2)
            season = match.group(3)
            title = match.group(4).replace('.', ' ')
            
            if show.lower() == title.lower():
                video_type = VideoTypes.film
            
            if (len(season) == 4) and (video_type != VideoTypes.film):
                while True:
                    response = input('Is this a miniseries? (y/n) ')
                    if response.lower() == 'y':
                        video_type = VideoTypes.miniserie
                        break
                    elif response.lower() == 'n':
                        video_type = VideoTypes.film
                        break
            
            if video_type == VideoTypes.miniserie:
                episode = 'Partie {0}'.format(episode[episode.find('E') + 1:])

            return show, episode, season, title
        else:
            sys.exit('ERROR: Unrecognized character in {0}\n'.format(filename))

    for filename in sorted(os.listdir(os.getcwd())):
        if not filename.endswith('.ts'):
            continue
        show, episode, season, title = parse_filename(filename)
        
        if video_type == VideoTypes.film:
            renamed_filename = '{} ({}).mp4'.format(title, season)
        else:
            renamed_filename = '{} - {} - {}.mp4'.format(show, episode, title)
        
        print(filename)
        print('\t{}'.format(renamed_filename))
        files_to_rename[filename] = renamed_filename
            
    response = input('Rename files? (y/n) ')
    if response == 'y':
        for filename in files_to_rename:
            os.rename(
                os.path.join(
                    os.getcwd(), 
                    filename
                ),
                os.path.join(
                    os.getcwd(),
                    files_to_rename[filename]
                )
            )


if __name__ == '__main__':
    main()
