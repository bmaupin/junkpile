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
import toutv.transport
import toutvcli.app


# The maximum number of times an emission will be listed as new
MAX_NEW_COUNT = 3
# The maximum number of times per operation timeout errors will be ignored
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
    def _build_toutv_client(self, *args, **kwargs):
        client = super()._build_toutv_client(*args, **kwargs)
        client._transport = JsonTransportPlus()
        
        return client
    
    
    # Override
    def _command_fetch(self, *args, **kwargs):
        self._data = self._get_data()
        
        super()._command_fetch(*args, **kwargs)
        
        self._write_data(self._data)
    
    '''
        if args.emission is not None:
            emission = self._toutvclient.get_emission_by_name(args.emission)
        else:
            sys.exit('Error: please provide name of emission to download')
        
        data = self._get_data()
        
        # Download single episode
        if args.episode is not None:
            episode = self._toutvclient.get_episode_by_name(emission, args.episode)
            self._fetch_episode(episode, output_dir=args.directory, bitrate=args.bitrate, quality=args.quality, overwrite=False)
        
        # Download all episodes
        else:
            episodes = self._toutvclient.get_emission_episodes(emission)
            for episode_id in episodes:
#                if not any(e for e in data.emissions if e.id == emission.Id):
                if (emission.Id in data[self.DATA_EMISSIONS] and
                        self.DATA_DOWNLOADED in data[self.DATA_EMISSIONS][emission.Id]):
                    # TODO: do the comparison
                    sys.exit('Error: not yet implemented')
                
                else:
                    sys.exit('Error: not yet implemented')
    '''
    
    # Override
    def _fetch_episode(self, episode, output_dir, bitrate, quality, overwrite):
        # Match the emission from the data file
        data_emission = None
        for em in self._data.emissions:
            if em.id == episode._emission.Id:
                if em.title.lower() != episode._emission.Title.lower():
                    sys.stderr.write(
                        'Warning: Emission title mismatch\n'
                        '\tId: {}\n'
                        '\tTou.tv title: {}\n'
                        '\tData file title: {}\n'.format(
                            episode._emission.Id,
                            episode._emission.Title,
                            em.title
                        )
                    )
                
                data_emission = em
                break
            
            elif em.title.lower() == episode._emission.Title.lower():
                if em.id != episode._emission.Id:
                    sys.stderr.write(
                        'Warning: Emission Id mismatch\n'
                        '\tTitle: {}\n'
                        '\tTou.tv Id: {}\n'
                        '\tData file Id: {}\n'.format(
                            episode._emission.Title,
                            episode._emission.Id,
                            em.id
                        )
                    )
                
                data_emission = em
                break
        
        # See if the episode has already been downloaded
        data_episode = None
        if data_emission is not None:
            for ep in data_emission.episodes:
                # Match first by title
                if ep.id == episode.Id:
                    if ep.title.lower() != episode.Title.lower():
                        sys.stderr.write(
                            'Warning: Episode title mismatch\n'
                            '\tId: {}\n'
                            '\tTou.tv title: {}\n'
                            '\tData file title: {}\n'.format(
                                episode.Id,
                                episode.Title,
                                ep.title
                            )
                        )
                    
                    data_episode = ep
                    break
                
                # Otherwise match by Id
                elif ep.title.lower() == episode.Title.lower():
                    if ep.id != episode.Id:
                        sys.stderr.write(
                            'Warning: Episode Id mismatch\n'
                            '\tTitle: {}\n'
                            '\tTou.tv Id: {}\n'
                            '\tData file Id: {}\n'.format(
                                episode.Title,
                                episode.Id,
                                ep.id
                            )
                        )
                    
                    data_episode = ep
                    break
                
        # Don't download if episode already downloaded
        if data_episode is not None:
            print('Already downloaded (use -f to download anyway): {} - {} - {}'.format(
                episode._emission.Title,
                episode.SeasonAndEpisode,
                episode.Title))
            
        else:
            # Handle API change
            if hasattr(episode, 'get_available_qualities'):
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
            
            else:
                # Get available bitrates for episode
                bitrates = retry_function(episode.get_available_bitrates)
                
                # Choose bitrate
                if bitrate is None:
                    if quality == toutvcli.app.App.QUALITY_MIN:
                        bitrate = bitrates[0]
                    elif quality == toutvcli.app.App.QUALITY_MAX:
                        bitrate = bitrates[-1]
                    elif quality == toutvcli.app.App.QUALITY_AVG:
                        bitrate = toutvcli.app.App._get_average_bitrate(bitrates)

            '''
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
            '''
        
        # Save the emission info to the data file if it doesn't exist
        # TODO
        
        # Save the downloaded episode info to the data file
        if data_episode is None:
            data_episode = Episode()
            data_episode.bitrate = bitrate
            data_episode.id = episode.Id
            data_episode.title = episode.Title
            
            data_emission.episodes.append(data_episode)
        
    
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
        repertoire = self._toutvclient.get_page_repertoire()
        repertoire_emissions = repertoire.get_emissions()

        today = datetime.datetime.now().strftime('%Y-%m-%d')
        data = self._get_data()

        # If this is the first run ever or the first run of the day
        if data.last_run != today:
            # If this is the first run ever
            if data.last_run is None:
                data.last_run = today
            
            # Start with a fresh list of new emissions
            data.new_emissions = []
            
            for emission_id in repertoire_emissions:
                emission = None
                
                # Get the emission from the data
                for e in data.emissions:
                    if e.id == emission_id:
                        if emission is not None:
                            sys.stderr.write('Warning: duplicate emission exists in data with id {}\n'.format(emission_id))
                        else:
                            emission = e
                
                # If this is a completely new emission
                if emission is None:
                    data.new_emissions.append(emission_id)
                    
                    emission = Emission()
                    emission.id = emission_id
                    emission.title = repertoire_emissions[emission_id].Title
                    emission.first_seen = today
                    emission.new_count = 1
                    
                    data.emissions.append(emission)
                
                # If this is a new emission since the last run
                if emission.last_seen != None and emission.last_seen != data.last_run:
                    emission.new_count += 1
                    
                    if emission.new_count <= MAX_NEW_COUNT:
                        data.new_emissions.append(emission_id)
                
                emission.last_seen = today
                
                # Basic sanity check if title of an emission has changed
                if repertoire_emissions[emission_id].Title.lower() != \
                        emission.title.lower():
                    sys.stderr.write(
                        'Warning: title mismatch\n'
                        '\tId: {}\n'
                        '\tTou.tv title: {}\n'
                        '\tData file title: {}\n'.format(
                            emission_id,
                            repertoire_emissions[emission_id].Title,
                            emission.title
                            )
                        )
            
            # Sort the list of new emissions alphabetically
            data.new_emissions.sort(key=title_sort_func)

            data.last_run = today
            
            self._write_data(data)
        
        # List all emissions
        if arg_all:
            emissions_keys = list(repertoire_emissions.keys())
            emissions_keys.sort(key=title_sort_func)
            
            list_emissions(repertoire_emissions, emissions_keys)
            
        # List only new emissions
        else:
            if len(data.new_emissions) == 0:
                print('No new emissions since last run')
                print('To list all emissions, see: {} list --help\n'.format(
                    sys.argv[0]))
                
            else:
                list_emissions(repertoire_emissions, data.new_emissions)
    
    def _get_data(self):
        data_path = self._get_data_file_path()
        if not os.path.exists(data_path):
            return Data()
            
        else:
            with open(data_path, 'r') as data_file:
                json_data = json.loads(data_file.read())
                data = Data()
                
                for data_key in json_data.keys():
                    if data_key == 'emissions':
                        for json_emission in json_data[data_key]:
                            emission = Emission()
                            
                            for emission_key in json_emission.keys():
                                if emission_key == 'episodes':
                                    for json_episode in json_emission[emission_key]:
                                        episode = Episode()
                                    
                                        for episode_key in json_episode.keys():
                                            episode.__setattr__(episode_key, json_episode[episode_key])
                                            
                                        emission.episodes.append(episode)
                                
                                else:
                                    emission.__setattr__(emission_key, json_emission[emission_key])
                            
                            data.emissions.append(emission)
                    else:
                        data.__setattr__(data_key, json_data[data_key])

                return data

    def _get_data_file_path(self):
        DATA_FILE_NAME = 'toutv_data-test.json'
        
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
                json.dumps(
                    data, 
                    cls=JsonObjectEncoder,
                    sort_keys=True, 
                    indent=4, 
                    ensure_ascii=False,
                )
            )


class Data():
    def __init__(self):
        self.emissions = []
        self.last_run = None


class DownloaderPlus(toutv.dl.Downloader):
    # Override
    def _do_request(self, *args, **kwargs):
        return retry_function(super()._do_request, *args, **kwargs)


class Emission:
    def __init__(self):
        self.episodes = []
        self.last_seen = None


class Episode:
    pass


class JsonObjectEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class JsonTransportPlus(toutv.transport.JsonTransport):
    # Override
    def _do_query(self, *args, **kwargs):
        return retry_function(super()._do_query, *args, **kwargs)


if __name__ == '__main__':
    main()
