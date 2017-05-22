#!/usr/bin/env python

import argparse
import datetime
import sys


def main():
    args = parse_arguments()

    srt = Srt.fromfile(args.infile_name)

    if args.adjust == True:
        adjust_timecodes(srt)

    srt.write(args.outfile_name)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile_name', metavar='/path/to/input.srt')
    parser.add_argument('outfile_name', metavar='/path/to/output.srt')

    parser.add_argument('-a', '--adjust', action='store_true', help='Adjust subtitle timecodes')

    args = parser.parse_args()
    return args


def adjust_timecodes(srt):
    choice = input('Do you wish to manually specify the old subtitle timecodes? (y/n) ')

    if choice.lower() == 'y':
        old_start_timecode_first_subtitle = input('Please enter old start timecode of first spoken subtitle: ')
    else:
        old_start_timecode_first_subtitle = srt.subtitles[0].start
    new_start_timecode_first_subtitle = input('Please enter new start timecode of first subtitle: ')

    if choice.lower() == 'y':
        old_start_timecode_last_subtitle = input('Please enter old start timecode of last spoken subtitle: ')
    else:
        old_start_timecode_last_subtitle = srt.subtitles[-1].start
    new_start_timecode_last_subtitle = input('Please enter new start timecode of last subtitle: ')

    srt.adjust_timecodes(
        old_start_timecode_first_subtitle,
        old_start_timecode_last_subtitle,
        new_start_timecode_first_subtitle,
        new_start_timecode_last_subtitle)


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

            # Remove Windows BOM :/
            line = line.replace('\ufeff', '')

            if prev_line == '' and subtitle_text != []:
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
            elif line != '...':
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

        srt.__remove_opensubtitles_ads()

        return srt


    def __remove_opensubtitles_ads(self):
        for text_line in self.subtitles[0].text:
            if text_line.lower().find('opensubtitles') != -1:
                del self.subtitles[0]
                break

        for text_line in self.subtitles[-1].text:
            if text_line.lower().find('opensubtitles') != -1:
                del self.subtitles[-1]
                break


    def adjust_timecodes(
            self,
            old_start_timecode_first_subtitle,
            old_start_timecode_last_subtitle,
            new_start_timecode_first_subtitle,
            new_start_timecode_last_subtitle):

        for subtitle in self.subtitles:
            subtitle.start = self.__adjust_timecode(
                old_start_timecode_first_subtitle,
                old_start_timecode_last_subtitle,
                new_start_timecode_first_subtitle,
                new_start_timecode_last_subtitle,
                subtitle.start)
            subtitle.end = self.__adjust_timecode(
                old_start_timecode_first_subtitle,
                old_start_timecode_last_subtitle,
                new_start_timecode_first_subtitle,
                new_start_timecode_last_subtitle,
                subtitle.end)


    def __adjust_timecode(
            self,
            old_start_timecode_first_subtitle,
            old_start_timecode_last_subtitle,
            new_start_timecode_first_subtitle,
            new_start_timecode_last_subtitle,
            old_subtitle_timecode):

        old_start_timecode_first_subtitle = SrtTimecode(old_start_timecode_first_subtitle)
        old_start_timecode_last_subtitle = SrtTimecode(old_start_timecode_last_subtitle)
        new_start_timecode_first_subtitle = SrtTimecode(new_start_timecode_first_subtitle)
        new_start_timecode_last_subtitle = SrtTimecode(new_start_timecode_last_subtitle)

        old_adjusted_subtitle_timecode = old_subtitle_timecode - old_start_timecode_first_subtitle
        old_duration = old_start_timecode_last_subtitle - old_start_timecode_first_subtitle
        new_duration = new_start_timecode_last_subtitle - new_start_timecode_first_subtitle

        new_adjusted_subtitle_timecode = old_adjusted_subtitle_timecode * (new_duration / old_duration)
        new_subtitle_timecode = new_adjusted_subtitle_timecode + new_start_timecode_first_subtitle

        return new_subtitle_timecode


    def write(self, filename):
        with open(filename, 'w') as file:
            for subtitle_index, subtitle in enumerate(self.subtitles):
                # Subtitle numbering should start with 1 (https://en.wikipedia.org/wiki/SubRip#SubRip_text_file_format)
                file.write('{}\n'.format(subtitle_index + 1))
                file.write('{} --> {}\n'.format(subtitle.start, subtitle.end))
                file.write('{}\n'.format('\n'.join(subtitle.text)))
                if subtitle_index != len(self.subtitles) - 1:
                    file.write('\n')


class SrtSubtitle:
    def __init__(self, start, end, text):
        self.start = SrtTimecode(start)
        self.end = SrtTimecode(end)
        self.text = text


class SrtTimecode():
    def __init__(self, timecode):
        if isinstance(timecode, str):
            self.timedelta = SrtTimecode.timecode_to_timedelta(timecode)
        elif isinstance(timecode, datetime.timedelta):
            self.timedelta = timecode
        elif isinstance(timecode, SrtTimecode):
            self.timedelta = timecode.timedelta
        else:
            sys.exit('ERROR: timecode is neither a string nor a datetime.timedelta nor an SrtTimecode')

    @property
    def microseconds(self):
        return self.timedelta.microseconds

    @property
    def seconds(self):
        return self.timedelta.seconds

    def __add__(self, other):
        return SrtTimecode(self.timedelta + other.timedelta)

    def __mul__(self, other):
        return SrtTimecode(self.timedelta * other)

    def __sub__(self, other):
        return SrtTimecode(self.timedelta - other.timedelta)

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
    def timecode_to_timedelta(timecode_string):
        # hh:mm:ss,ttt
        if timecode_string.count(':') == 2:
            hours, minutes, seconds_milliseconds = timecode_string.split(':')
        else:
            sys.exit('ERROR: invalid timecode ({})\n'.format(timecode_string))

        seconds, milliseconds = seconds_milliseconds.split(',')

        return datetime.timedelta(
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds),
            milliseconds=int(milliseconds)
        )


if __name__ == '__main__':
    main()
