#!/usr/bin/env python

import argparse
import os
import os.path
import sys
import urllib.request

import lxml.etree
import lxml.html


def main():
    def depunctuate(s):
        punctuation = [',', '.', "'", '!', '?', '-', ':']
        for symbol in punctuation:
            s = s.replace(symbol, '')
        return s
    
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
                for episode_name in episodes_ordered:
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
                        
                        oldname = os.path.join(dirpath, filename)
                        newname = os.path.join(
                            newpath,
                            'S{:02d}E{:02d} - {}{}'.format(
                                int(episodes[episode_name]['season']),
                                int(episodes[episode_name]['episode_number']),
                                episode_name,
                                extension
                                )
                            )
                        
                        if newname in files_to_rename.values():
                            sys.stderr.write('Warning: not renaming file to avoid duplicate\n'
                                '\tOld name: {}\n'
                                '\tProposed new name: {}\n'.format(
                                    os.path.basename(oldname),
                                    os.path.basename(newname)))
                            
                        else:
                            print(os.path.basename(oldname))
                            print('\t{}'.format(os.path.basename(newname)))
                            files_to_rename[oldname] = newname

    response = input('Rename files? (y/n) ')
    if response == 'y':
        for oldname in files_to_rename:
            os.rename(oldname, files_to_rename[oldname])


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


if __name__ == '__main__':
    main()
