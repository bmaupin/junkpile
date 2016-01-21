#!/usr/bin/env python

'''
TODO: 
- Get episode names, numbers, seasons from URL
- Get thetvdb url from stdin
'''

import argparse
import os
import os.path
import sys


def main():
    def depunctuate(s):
        punctuation = [',', '.', "'", '!', '?', '-', ':']
        for symbol in punctuation:
            s = s.replace(symbol, '')
        return s
    
    args = parse_args()
    
    # Get episode names, numbers, seasons
    episodes = {}
    with open(args.input_path) as infile:
        for line in infile:
            episode_name = line.split('\t')[1]
            season = line.split('\t')[0].split()[0]
            episode_number = line.split('\t')[0].split()[2]
            
            episodes[episode_name] = {}
            episodes[episode_name]['season'] = season
            episodes[episode_name]['episode_number'] = episode_number
    
    # Rename local episodes and move them into season subfolders
    for (dirpath, dirnames, filenames) in os.walk(args.video_path):
        if filenames != []:
            for filename in filenames:
                for episode_name in episodes:
                    if depunctuate(filename).lower().find(depunctuate(episode_name).lower()) != -1:
                        basename, extension = os.path.splitext(filename)
                        newpath = os.path.join(
                            args.video_path,
                            'Season {:02d}'.format(
                                int(episodes[episode_name]['season'])
                                )
                            )
                        
                        if not os.path.exists(newpath):
                            os.makedirs(newpath)
                        
                        os.rename(
                            os.path.join(
                                dirpath,
                                filename
                                ),
                            os.path.join(
                                newpath,
                                'S{:02d}E{:02d} - {}{}'.format(
                                    int(episodes[episode_name]['season']),
                                    int(episodes[episode_name]['episode_number']),
                                    episode_name,
                                    extension
                                    )
                                )
                            )


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        'video_path',
        help='Full path to video files to rename',
        )
    p.add_argument(
        'input_path',
        help='Full path to thetvdb.com input file',
        )
    
    args = p.parse_args()
    
    return args


if __name__ == '__main__':
    main()