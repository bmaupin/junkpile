#!/usr/bin/env python

import argparse
import os
import os.path
import re
import sys
import unicodedata
import urllib.request

import lxml.etree
import lxml.html


def main():
    def match_filename(filename):
        def matched_file_output():
            return str(
                'File: {}\n'
                '\tMatch: {}\n'
                '\tProposed new name: {}'.format(
                    os.path.basename(oldname),
                    episode_name,
                    os.path.basename(newname)),
                )
        
        for episode_name in episodes_ordered:
            if prep_for_compare(filename).lower().find(prep_for_compare(episode_name).lower()) != -1:
                basename, extension = os.path.splitext(filename)
                newpath = os.path.join(
                    args.video_path,
                    'Season {:02d}'.format(
                        int(episodes[episode_name]['season'])
                        )
                    )
                
                oldname = os.path.join(dirpath, filename)
                if args.overwrite == True:
                    new_episode_name = episode_name
                else:
                    new_episode_name = basename.split('-')[-1].strip()

                new_season_episode = 'S{:02d}E{:02d}'.format(
                    int(episodes[episode_name]['season']),
                    int(episodes[episode_name]['episode_number']),
                    )
                
                newname = os.path.join(
                    newpath,
                    '{} - {}{}'.format(
                        new_season_episode,
                        new_episode_name,
                        extension
                        )
                    )
                
                if oldname == newname:
                    return
                
                if os.path.exists(newname):
                    sys.stderr.write(
                        'Warning: file already exists. Not overwriting:\n\t{}\n'.format(
                            matched_file_output()))
                    return
                    
                else:
                    if new_season_episode in files_to_rename:
                        sys.stderr.write(
                            'Warning: not renaming file to avoid duplicate:\n\t{}\n'.format(
                                matched_file_output()))
                        return
                        
                    else:
                        print(matched_file_output())
                        files_to_rename[new_season_episode] = {}
                        files_to_rename[new_season_episode]['oldname'] = oldname
                        files_to_rename[new_season_episode]['newname'] = newname
                        return
    
    args = parse_args()
    
    episodes, episodes_ordered = parse_html(args.url)
    
    # Go through the episodes in reverse order so we can better handle multi-part episodes
    episodes_ordered.reverse()
    
    # Rename local episodes and move them into season subfolders
    files_to_rename = {}
    for (dirpath, dirnames, filenames) in os.walk(args.video_path):
        if filenames != []:
            # Go through the filenames in reverse order as well
            filenames.sort(reverse=True)
            for filename in filenames:
                match_filename(filename)

    if len(files_to_rename) == 0:
        print('No matches found or all files already renamed')
    else:
        response = input('Rename files? (y/n) ')
        if response == 'y':
            for season_episode in files_to_rename:
                os.renames(files_to_rename[season_episode]['oldname'], files_to_rename[season_episode]['newname'])


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        'video_path',
        help='Full path to video files to rename',
        )
    p.add_argument(
        'url',
        help='URL to All Seasons page on thetvdb.com',
        )
    p.add_argument(
        '-o', 
        '--overwrite', 
        action='store_true',
        help='Overwrite the title as well as the season/number')
    
    args = p.parse_args()
    
    return args


def parse_html(url):
    if url.find('seasonall') == -1:
        sys.exit('Error: please provide the URL to the All Seasons page on thetvdb. Ex: http://thetvdb.com/?tab=seasonall&id=72668&lid=17\n')
    
    parser = lxml.etree.HTMLParser()
    with urllib.request.urlopen(url) as f:
        page = lxml.html.parse(f, parser)
    
    # Get the table containing the list of episodes
    for table in page.iter('table'):
        if 'id' in table.attrib:
            if table.attrib['id'] == 'listtable':
                break
    
    episodes = {}
    episodes_ordered = []
    # Iterate through each episode
    for tr in table.iter('tr'):
        if 'class' in tr[0].attrib and tr[0].attrib['class'] == 'head':
            continue
        
        if tr[0][0].text == 'Special':
            # TODO
            sys.stderr.write('Warning: special episodes not yet implemented\n')
            continue
        
        episode_name = tr[1][0].text
        season, episode_number = tr[0][0].text.split(' x ')
        
        episodes[episode_name] = {}
        episodes[episode_name]['season'] = season
        episodes[episode_name]['episode_number'] = episode_number
        
        episodes_ordered.append(episode_name)

    return episodes, episodes_ordered


def prep_for_compare(s):
    # Remove puncuation
    punctuation = [',', '.', "'", '!', '?', '-', ':']
    for symbol in punctuation:
        s = s.replace(symbol, '')
    
    # Compress whitespace
    s = ' '.join(s.split())
    
    # Remove accents
    # http://stackoverflow.com/a/518232/399105
    stripped_string = ''
    for c in unicodedata.normalize('NFD', s):
        if unicodedata.category(c) != 'Mn':
            stripped_string += c
    
    return stripped_string


if __name__ == '__main__':
    main()
