#!/usr/bin/env python

import argparse
import datetime
import json
import locale
import os
import platform
import sys

import toutv.exceptions
import toutvcli.app


# The maximum number of times an emission will be listed as new
MAX_NEW_COUNT = 3
MAX_TIMEOUTS = 10

# Don't change these
DATA_EMISSIONS = 'emissions'
DATA_FIRST_SEEN = 'first_seen'
DATA_LAST_RUN = 'last_run'
DATA_LAST_SEEN = 'last_seen'
DATA_NEW_EMISSIONS = 'new_emissions'
DATA_NEW_COUNT = 'new_count'
DATA_TITLE = 'title'


def main():
    # Set the locale for improved sorting of non-ASCII characters
    locale.setlocale(locale.LC_ALL, "")
    
    args = parse_args()
    args.func(args)


def parse_args():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest='command', help='Commands help')
    
    pl = sp.add_parser(
        'list', 
        help='List new emissions or episodes since last run')
    pl.add_argument(
        '-a', 
        '--all', 
        action='store_true', 
        help='List all emissions or episodes')
    pl.set_defaults(func=command_list)
    
    args = p.parse_args()
    
    if args.command is None:
        p.print_help()
        sys.exit()
    
    return args


def get_data_file_path():
    DATA_FILE_NAME = 'toutv_data.json'
    
    if 'XDG_DATA_HOME' in os.environ:
        data_dir = os.environ['XDG_DATA_HOME']
        xdg_data_path = os.path.join(data_dir, 'toutv')
        if not os.path.exists(xdg_data_path):
            os.makedirs(xdg_data_path)
        data_path = os.path.join(xdg_data_path, DATA_FILE_NAME)
    else:
        home_dir = os.environ['HOME']
        home_data_path = os.path.join(home_dir, '.local', 'share', 'toutv')
        if not os.path.exists(home_data_path):
            os.makedirs(home_data_path)
        data_path = os.path.join(home_data_path, DATA_FILE_NAME)
        
    return data_path


def get_data():
    data_path = get_data_file_path()
    if not os.path.exists(data_path):
        return {}
    else:
        with open(data_path, 'r') as data_file:
            return json.loads(data_file.read())


def write_data(data):
    data_path = get_data_file_path()
    with open(data_path, 'w') as data_file:
        data_file.write(
            json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
        )


def command_list(args):
    def title_sort_func(ekey):
        return locale.strxfrm(repertoire_emissions[ekey].get_title())
    
    print('Please wait...\n')
    
    app = toutvcli.app.App(None)
    client = app._build_toutv_client(no_cache=False)

    # The name of this exception was changed
    if hasattr(toutv.exceptions, 'RequestTimeout'):
        toutv_requesttimeout = toutv.exceptions.RequestTimeout
    else:
        toutv_requesttimeout = toutv.exceptions.RequestTimeoutError

    # Get the list of current emissions
    for n in range(MAX_TIMEOUTS):
        try:
            repertoire = client.get_page_repertoire()
            repertoire_emissions = repertoire.get_emissions()
            break
        except toutv_requesttimeout:
            pass
        
        if n == MAX_TIMEOUTS - 1:
            sys.exit('Error: max timeout attempts reached getting emissions\n')

    # For some reason the emission ID is an int, but JSON converts int keys to
    # strings, so just make them strings so we don't have to worry about it
    repertoire_emissions = {str(k):v for k, v in repertoire_emissions.items()}

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    data = get_data()

    # If this is the first run ever or the first run of the day
    if DATA_LAST_RUN not in data or data[DATA_LAST_RUN] != today:
        # If this is the first run ever
        if DATA_LAST_RUN not in data:
            data[DATA_LAST_RUN] = today
            data[DATA_EMISSIONS] = {}
        
        # Start with a fresh list of new emissions
        data[DATA_NEW_EMISSIONS] = []
        
        for emission_id in repertoire_emissions:
            # If this is a completely new emission
            if emission_id not in data[DATA_EMISSIONS]:
                data[DATA_NEW_EMISSIONS].append(emission_id)
                
                data[DATA_EMISSIONS][emission_id] = {}
                data[DATA_EMISSIONS][emission_id][DATA_TITLE] = repertoire_emissions[emission_id].Title
                data[DATA_EMISSIONS][emission_id][DATA_FIRST_SEEN] = today
                data[DATA_EMISSIONS][emission_id][DATA_NEW_COUNT] = 1
            
            # If this is a new emission since the last run
            if DATA_LAST_SEEN in data[DATA_EMISSIONS][emission_id] and \
                    data[DATA_EMISSIONS][emission_id][DATA_LAST_SEEN] != \
                    data[DATA_LAST_RUN]:
                data[DATA_EMISSIONS][emission_id][DATA_NEW_COUNT] += 1
                
                if data[DATA_EMISSIONS][emission_id][DATA_NEW_COUNT] <= \
                        MAX_NEW_COUNT:
                    data[DATA_NEW_EMISSIONS].append(emission_id)
            
            data[DATA_EMISSIONS][emission_id][DATA_LAST_SEEN] = today
            
            # Basic sanity check if title of an emission has changed
            if repertoire_emissions[emission_id].Title != \
                    data[DATA_EMISSIONS][emission_id][DATA_TITLE]:
                sys.stderr.write(
                    'Warning: title mismatch\n'
                    '\tId: {}'
                    '\tTou.tv title: {}'
                    '\tData file title: {}'.format(
                        emission_id,
                        repertoire_emissions[emission_id].Title,
                        data[DATA_EMISSIONS][emission_id][DATA_TITLE]
                        )
                    )
        
        # Sort the list of new emissions alphabetically
        data[DATA_NEW_EMISSIONS].sort(key=title_sort_func)

        data[DATA_LAST_RUN] = today
        
        write_data(data)
    
    # List all emissions
    if args.all:
        emissions_keys = list(repertoire_emissions.keys())
        emissions_keys.sort(key=title_sort_func)
        
        list_emissions(repertoire_emissions, emissions_keys)
        
    # List only new emissions
    else:
        if len(data[DATA_NEW_EMISSIONS]) == 0:
            print('No new emissions since last run')
            
        else:
            list_emissions(repertoire_emissions, data[DATA_NEW_EMISSIONS])


def list_emissions(all_emissions, emissions_to_list):
    for emission_id in emissions_to_list:
        emission = all_emissions[emission_id]
        emission_string = ('{}\n\t{}\n\t{}'.format(
            emission.Title,
            emission.get_url(),
            emission.Genre.Title,
        ))
        if emission.Country is not None:
            emission_string += '\n\t{}'.format(emission.Country)
        print(emission_string)


if __name__ == '__main__':
    main()
