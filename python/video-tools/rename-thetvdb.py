#!/usr/bin/env python

'''
TODO: 
- Get episode names, numbers, seasons from URL
- Get path to rename from stdin
- Get thetvdb url from stdin
'''

import os
import os.path

PATH_TO_RENAME = '/path/to/episodes'
INFILE_NAME = '/path/to/episodes.txt'


def main():
    episodes = {}
    
    # Get episode names, numbers, seasons
    with open(INFILE_NAME) as infile:
        for line in infile:
            episode_name = line.split('\t')[1]
            season = line.split('\t')[0].split()[0]
            episode_number = line.split('\t')[0].split()[2]
            
            episodes[episode_name] = {}
            episodes[episode_name]['season'] = season
            episodes[episode_name]['episode_number'] = episode_number
    
    # Rename local episodes and move them into season subfolders
    for (dirpath, dirnames, filenames) in os.walk(PATH_TO_RENAME):
        if filenames != []:
            for filename in filenames:
                for episode_name in episodes:
                    if filename.lower().find(episode_name.lower()) != -1:
                        basename, extension = os.path.splitext(filename)
                        newpath = os.path.join(
                            PATH_TO_RENAME,
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
                                'S{:02d}E{:02d} - {}.{}'.format(
                                    int(episodes[episode_name]['season']),
                                    int(episodes[episode_name]['episode_number']),
                                    episode_name,
                                    extension
                                    )
                                )
                            )

if __name__ == '__main__':
    main()