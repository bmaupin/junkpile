#!/usr/bin/env python

import datetime
import optparse
import sys


def main():
    parser, infile_name, outfile_name = parse_options()

    srt = Srt.fromfile(infile_name)
    print(len(srt.subtitles))
    srt.write(outfile_name)


def parse_options():
    ''' set up and parse command line arguments
    '''

    # define a custom usage message
    usage = ('usage: %prog INPUT_FILE OUTPUT_FILE [options]\n'
    '\tWhere INPUT_FILE = path to SRT input file\n'
    '\tand OUTPUT_FILE = path to SRT output file')

    parser = optparse.OptionParser(usage=usage)

    # parse the arguments
    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.print_help()
        sys.exit('Error: INPUT_FILE and OUTPUT_FILE are required')
    infile_name = args[0]
    outfile_name = args[1]

    return parser, infile_name, outfile_name


class Srt():
    @classmethod
    def fromfile(cls, filename):
        file = open(filename)
        try:
            file.read()
            file.seek(0)
        except UnicodeDecodeError:
            file = open(filename, encoding='latin1')

        srt = cls()
        srt.subtitles = []
        subtitle_text = []
        prev_line = None

        for line in file:
            line = line.strip()

            if prev_line == '':
                srt_subtitle = SrtSubtitle(
                    subtitle_start,
                    subtitle_end,
                    subtitle_text)
                srt.subtitles.append(srt_subtitle)

                subtitle_text = []

            if line == '':
                pass
            # We'll manage subtitle numbers ourselves
            elif prev_line == None or prev_line == '' and line.isdigit():
                pass
            elif prev_line != None and prev_line.isdigit():
                subtitle_start, subtitle_end = line.split(' --> ')
            else:
                subtitle_text.append(line)

            prev_line = line

        # Get the last subtitle
        if subtitle_text != []:
            srt_subtitle = SrtSubtitle(
                subtitle_start,
                subtitle_end,
                subtitle_text)
            srt.subtitles.append(srt_subtitle)

        file.close()

        return srt


    def write(self, filename):
        with open(filename, 'w') as file:
            for subtitle_index, subtitle in enumerate(self.subtitles):
                # Subtitle numbering should start with 1 (https://en.wikipedia.org/wiki/SubRip#SubRip_text_file_format)
                file.write('{}\n'.format(subtitle_index + 1))
                file.write('{} --> {}\n'.format(subtitle.start, subtitle.end))
                file.write('{}\n'.format('\n'.join(subtitle.text)))
                file.write('\n')


class SrtSubtitle:
    def __init__(self, start, end, text):
        self.start = SrtTiming(start)
        self.end = SrtTiming(end)
        self.text = text


class SrtTiming():
    def __init__(self, timestamp):
        if isinstance(timestamp, str):
            self.timedelta = SrtTiming.timestamp_to_timedelta(timestamp)
        elif isinstance(timestamp, datetime.timedelta):
            self.timedelta = timestamp
        elif isinstance(timestamp, SrtTiming):
            self.timedelta = timestamp.timedelta
        else:
            sys.exit('ERROR: timing is neither a string nor a datetime.timestamp nor an SrtTiming')

    @property
    def microseconds(self):
        return self.timedelta.microseconds

    @property
    def seconds(self):
        return self.timedelta.seconds

    def __add__(self, other):
        return SrtTiming(self.timedelta + other.timedelta)

    def __mul__(self, other):
        return SrtTiming(self.timedelta * other)

    def __sub__(self, other):
        return SrtTiming(self.timedelta - other.timedelta)

    def __truediv__(self, other):
        return self.timedelta / other.timedelta

    # Output as hh:mm:ss,ttt
    def __str__(self):
        hours, remainder = divmod(self.timedelta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        microseconds = self.timedelta.microseconds

        return '{:02d}:{:02d}:{:02d},{}'.format(
            int(hours),
            int(minutes),
            int(seconds),
            str('{:06d}'.format(self.timedelta.microseconds))[0:3]
        )

    # Timestamp spec: https://en.wikipedia.org/wiki/SubRip#SubRip_text_file_format
    @staticmethod
    def timestamp_to_timedelta(timestamp_string):
        # hh:mm:ss,ttt
        if timestamp_string.count(':') == 2:
            hours, minutes, seconds_milliseconds = timestamp_string.split(':')
        else:
            sys.exit('ERROR: invalid timestamp ({})\n'.format(timestamp_string))

        seconds, milliseconds = seconds_milliseconds.split(',')

        return datetime.timedelta(
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds),
            milliseconds=int(milliseconds)
        )


if __name__ == '__main__':
    main()
