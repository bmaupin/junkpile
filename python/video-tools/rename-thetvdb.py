#!/usr/bin/env python

import argparse
import difflib
import os
import os.path
import re
import sys
import unicodedata
import urllib.request

import lxml.etree
import lxml.html


def main():
    args = parse_args()
    
    thetvdb_episodes = parse_html(args.url)
    
    # Rename local episodes and move them into season subfolders
    for (dirpath, dirnames, filenames) in os.walk(args.video_path):
        if filenames != []:
            for filename in filenames:
                match_filename(args, filename, dirpath, thetvdb_episodes)


def construct_newname(args, filename, thetvdb_episode_name, thetvdb_episodes):
    match = re.search('S\d+E\d+', filename)
    if not match:
        return None
        
    newpath = os.path.join(
        args.video_path,
        'Season {:02d}'.format(
            int(thetvdb_episodes[thetvdb_episode_name]['season'])
            )
        )
    
    old_season_episode = match.group()
    
    new_season_episode = 'S{:02d}E{:02d}'.format(
        int(thetvdb_episodes[thetvdb_episode_name]['season']),
        int(thetvdb_episodes[thetvdb_episode_name]['episode_number']),
        )
    
    newname = filename.replace(old_season_episode, new_season_episode)
    
    return os.path.join(newpath, newname)


def match_filename(args, filename, dirpath, thetvdb_episodes):
    # First try to find a match using prep_for_compare()
    for thetvdb_episode_name in thetvdb_episodes:
        if prep_for_compare(filename).lower().find(prep_for_compare(thetvdb_episode_name).lower()) != -1:
            if rename_file(args, filename, dirpath, thetvdb_episode_name, thetvdb_episodes):
                del thetvdb_episodes[thetvdb_episode_name]
                return
    
    # If no matches found, try difflib.get_close_matches()
    basename, extension = os.path.splitext(filename)
    if basename.find('-') == -1:
        print('Warning: "-" not found in file name. Results may be incomplete: {}'.format(filename))
    file_episode_name = basename.split('-')[-1].strip()
    
    for thetvdb_episode_name in thetvdb_episodes:
        if len(difflib.get_close_matches(file_episode_name, [thetvdb_episode_name])) == 1:
            if rename_file(args, filename, dirpath, thetvdb_episode_name, thetvdb_episodes):
                del thetvdb_episodes[thetvdb_episode_name]
                return


def matched_file_output(oldname, newname, thetvdb_episode_name):
    return str(
        'File: {}\n'
        '\tMatch: {}\n'
        '\tProposed new name: {}'.format(
            os.path.basename(oldname),
            thetvdb_episode_name,
            os.path.basename(newname)),
        )


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
    # Iterate through each episode
    for tr in table.iter('tr'):
        if 'class' in tr[0].attrib and tr[0].attrib['class'] == 'head':
            continue
        
        if len(tr[0]) == 0:
            sys.exit('Error: no episodes found. Try escaping any special characters or quoting the URL.')
        
        if tr[0][0].text == 'Special':
            # TODO
            sys.stderr.write('Warning: special episodes not yet implemented\n')
            continue
        
        episode_name = tr[1][0].text
        season, episode_number = tr[0][0].text.split(' x ')
        
        episodes[episode_name] = {}
        episodes[episode_name]['season'] = season
        episodes[episode_name]['episode_number'] = episode_number
        
    return episodes


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


def rename_file(args, filename, dirpath, thetvdb_episode_name, thetvdb_episodes):
    oldname = os.path.join(dirpath, filename)
    newname = construct_newname(args, filename, thetvdb_episode_name, thetvdb_episodes)
    
    if newname == None:
        sys.stderr.write(
            'Warning: unable to find season and episode in filename: {}\n'.format(
                oldname))
        return False
    
    if oldname == newname:
        return True
    
    if os.path.exists(newname):
        sys.stderr.write(
            'Warning: file already exists. Not overwriting:\n\t{}\n'.format(
                matched_file_output(oldname, newname, thetvdb_episode_name)))
        return False
    
    print(matched_file_output(oldname, newname, thetvdb_episode_name))
    response = input('Rename files? (y/n) ')
    if response == 'y':
        os.renames(oldname, newname)
        return True
    
    return False


if __name__ == '__main__':
    main()
