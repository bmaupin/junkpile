#!/usr/bin/env python

# Much of this is from here:
# https://github.com/bvanheu/pytoutv/blob/master/toutvcli/app.py

# Copyright (c) 2012, Benjamin Vanheuverzwijn <bvanheu@gmail.com>
# Copyright (c) 2014, Philippe Proulx <eepp.ca>
# All rights reserved.
#
# Thanks to Marc-Etienne M. Leveille
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of pytoutv nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Benjamin Vanheuverzwijn OR Philippe Proulx
# BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import argparse
import datetime
import json
import locale
import os
import platform
import sys

import toutv.dl
import toutv.exceptions
import toutvcli.app


# The maximum number of times an emission will be listed as new
MAX_NEW_COUNT = 3
# The maximum number of times timeout errors will be ignored
MAX_TIMEOUTS = 10


def main():
    app = AppPlus(sys.argv[1:])
    app.run()

def retry_function(function, *args, **kwargs):
    # The name of this exception was changed at some point
    if hasattr(toutv.exceptions, 'RequestTimeout'):
        TOUTV_REQUESTTIMEOUT = toutv.exceptions.RequestTimeout
    else:
        TOUTV_REQUESTTIMEOUT = toutv.exceptions.RequestTimeoutError
    
    for n in range(MAX_TIMEOUTS):
        try:
            result = function(*args, **kwargs)
            break
        except TOUTV_REQUESTTIMEOUT:
            pass
        
        if n == MAX_TIMEOUTS - 1:
            sys.exit('Error: max timeout attempts reached\n')
    
    return result


class AppPlus(toutvcli.app.App):
    # TODO: put data in its own class
    DATA_DOWNLOADED = 'downloaded'
    DATA_EMISSIONS = 'emissions'
    DATA_FIRST_SEEN = 'first_seen'
    DATA_LAST_RUN = 'last_run'
    DATA_LAST_SEEN = 'last_seen'
    DATA_NEW_EMISSIONS = 'new_emissions'
    DATA_NEW_COUNT = 'new_count'
    DATA_TITLE = 'title'
    
    # Override
    def run(self):
        locale.setlocale(locale.LC_ALL, '')
        
        # Override help messages
        for action in self._argparser._actions[1]._choices_actions:
            if action.dest == 'list':
                action.help = 'List new emissions or episodes since last run'
        
        for action in self._argparser._actions[1].choices['list']._actions:
            if action.dest == 'all':
                action.help = 'List all emissions or episodes'
        
        super().run()
    
    # Override
    def _command_fetch(self, args):
        if args.emission is not None:
            emission = retry_function(self._toutvclient.get_emission_by_name, args.emission)
        else:
            sys.exit('Error: please provide name of emission to download')
        
        data = self._get_data()
        
        # Download single episode
        if args.episode is not None:
            episode = retry_function(self._toutvclient.get_episode_by_name, emission, args.episode)
            self._fetch_episode(episode, output_dir=args.directory, bitrate=args.bitrate, quality=args.quality, overwrite=False)
        
        # Download all episodes
        else:
            episodes = retry_function(self._toutvclient.get_emission_episodes, emission)
            for episode_id in eposides:
                if (emission.Id in data[self.DATA_EMISSIONS] and
                        self.DATA_DOWNLOADED in data[self.DATA_EMISSIONS][emission.Id]):
                    # TODO: do the comparison
                    sys.exit('Error: not yet implemented')
                
                else:
                    sys.exit('Error: not yet implemented')
    
    # Override
    def _fetch_episode(self, episode, output_dir, bitrate, quality, overwrite):
        # Get available bitrates for episode
        qualities = retry_function(episode.get_available_qualities)

        # Choose bitrate
        if bitrate is None:
            if quality == toutvcli.app.App.QUALITY_MIN:
                bitrate = qualities[0].bitrate
            elif quality == toutvcli.app.App.QUALITY_MAX:
                bitrate = qualities[-1].bitrate
            elif quality == toutvcli.app.App.QUALITY_AVG:
                bitrate = toutvcli.app.App._get_average_bitrate(qualities)

        # Create downloader
        opu = self._on_dl_progress_update
        self._dl = DownloaderPlus(episode, bitrate=bitrate,
                                       output_dir=output_dir,
                                       on_dl_start=self._on_dl_start,
                                       on_progress_update=opu,
                                       overwrite=overwrite)

        # Start download
        self._dl.download()

        # Finished
        self._dl = None
    
    # Override
    def _print_list_emissions(self, arg_all=False):
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
        
        def title_sort_func(ekey):
            return locale.strxfrm(repertoire_emissions[ekey].get_title())

        # Get the list of current emissions
        repertoire = retry_function(self._toutvclient.get_page_repertoire)
        repertoire_emissions = retry_function(repertoire.get_emissions)

        # For some reason the emission ID is an int, but JSON converts int keys to
        # strings, so just make them strings so we don't have to worry about it
        repertoire_emissions = {str(k):v for k, v in repertoire_emissions.items()}

        today = datetime.datetime.now().strftime('%Y-%m-%d')
        data = self._get_data()

        # If this is the first run ever or the first run of the day
        if self.DATA_LAST_RUN not in data or data[self.DATA_LAST_RUN] != today:
            # If this is the first run ever
            if self.DATA_LAST_RUN not in data:
                data[self.DATA_LAST_RUN] = today
                data[self.DATA_EMISSIONS] = {}
            
            # Start with a fresh list of new emissions
            data[self.DATA_NEW_EMISSIONS] = []
            
            for emission_id in repertoire_emissions:
                # If this is a completely new emission
                if emission_id not in data[self.DATA_EMISSIONS]:
                    data[self.DATA_NEW_EMISSIONS].append(emission_id)
                    
                    data[self.DATA_EMISSIONS][emission_id] = {}
                    data[self.DATA_EMISSIONS][emission_id][self.DATA_TITLE] = repertoire_emissions[emission_id].Title
                    data[self.DATA_EMISSIONS][emission_id][self.DATA_FIRST_SEEN] = today
                    data[self.DATA_EMISSIONS][emission_id][self.DATA_NEW_COUNT] = 1
                
                # If this is a new emission since the last run
                if self.DATA_LAST_SEEN in data[self.DATA_EMISSIONS][emission_id] and \
                        data[self.DATA_EMISSIONS][emission_id][self.DATA_LAST_SEEN] != \
                        data[self.DATA_LAST_RUN]:
                    data[self.DATA_EMISSIONS][emission_id][self.DATA_NEW_COUNT] += 1
                    
                    if data[self.DATA_EMISSIONS][emission_id][self.DATA_NEW_COUNT] <= \
                            MAX_NEW_COUNT:
                        data[self.DATA_NEW_EMISSIONS].append(emission_id)
                
                data[self.DATA_EMISSIONS][emission_id][self.DATA_LAST_SEEN] = today
                
                # Basic sanity check if title of an emission has changed
                if repertoire_emissions[emission_id].Title.lower() != \
                        data[self.DATA_EMISSIONS][emission_id][self.DATA_TITLE].lower():
                    sys.stderr.write(
                        'Warning: title mismatch\n'
                        '\tId: {}\n'
                        '\tTou.tv title: {}\n'
                        '\tData file title: {}\n'.format(
                            emission_id,
                            repertoire_emissions[emission_id].Title,
                            data[self.DATA_EMISSIONS][emission_id][self.DATA_TITLE]
                            )
                        )
            
            # Sort the list of new emissions alphabetically
            data[self.DATA_NEW_EMISSIONS].sort(key=title_sort_func)

            data[self.DATA_LAST_RUN] = today
            
            self._write_data(data)
        
        # List all emissions
        if arg_all:
            emissions_keys = list(repertoire_emissions.keys())
            emissions_keys.sort(key=title_sort_func)
            
            list_emissions(repertoire_emissions, emissions_keys)
            
        # List only new emissions
        else:
            if len(data[self.DATA_NEW_EMISSIONS]) == 0:
                print('No new emissions since last run')
                print('To list all emissions, see: {} list --help\n'.format(
                    sys.argv[0]))
                
            else:
                list_emissions(repertoire_emissions, data[self.DATA_NEW_EMISSIONS])
    
    def _get_data(self):
        data_path = self._get_data_file_path()
        if not os.path.exists(data_path):
            return {}
        else:
            with open(data_path, 'r') as data_file:
                return json.loads(data_file.read())

    def _get_data_file_path(self):
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

    def _write_data(self, data):
        data_path = self._get_data_file_path()
        with open(data_path, 'w') as data_file:
            data_file.write(
                json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
            )


class DownloaderPlus(toutv.dl.Downloader):
    # Override
    def _do_request(self, *args, **kwargs):
        return retry_function(super()._do_request, *args, **kwargs)


if __name__ == '__main__':
    main()
