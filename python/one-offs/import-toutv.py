#!/usr/bin/env python

import os
import os.path
import re
import sys

# Ugly hack so we can import pytoutv_plus
lib_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'video-tools'))
sys.path.append(lib_path)

import pytoutv_plus

def main():
    filenames = []
    for (dirpath, dirnames, dirfilenames) in os.walk(os.getcwd()):
        if dirfilenames != []:
            filenames.extend(dirfilenames)
    
    data = pytoutv_plus.Data()
    
    filename_chars = 'àÀâÂçÇéÉèÈêÊëîÎôÔ\w\-\'\.\(\)'
    pattern = re.compile('([{0}]+)\.(S([\d]+)E[\d]+)\.([{0}]+)\.([\d]+)kbps\.ts'.format(filename_chars))
    
    for filename in filenames:
        # Skip anything not ending in .ts
        if not filename.endswith('.ts'):
            continue
        
        match = pattern.search(filename)
        if match:
            emission_title = match.group(1).replace('.', ' ')
            episode_sae = match.group(2)
            episode_season = match.group(3)
            episode_title = match.group(4).replace('.', ' ')
            episode_bitrate = int(match.group(5)) * 1000
        
        else:
            sys.stderr.write('Warning: no match for file {}\n'.format(filename))
            # Go to the next file
            continue
        
        for emission in data.emissions:
            if emission_title.lower() == emission.title.lower():
                break
            
        else:
            sys.stderr.write('Warning: no match for emission {}\n'.format(emission_title))
            # Go to the next file
            continue

        for episode in emission.episodes:
            if episode_title.lower() == episode.title.lower():
                print('Skipping {} - {} - {}'.format(
                    emission_title,
                    episode_sae,
                    episode_title))
                # Episode match, go to next file
                break
            
        else:
            # If we've had an emission match but no episode match, add the episode to the emission
            print('Importing {} - {} - {}'.format(
                emission_title,
                episode_sae,
                episode_title))
            ep = pytoutv_plus.Episode()
            ep.title = episode_title
            ep.bitrate = episode_bitrate
            
            emission.episodes.append(ep)
        
    data.write()
                

if __name__ == '__main__':
    main()
