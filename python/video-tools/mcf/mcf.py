import datetime
import sys


''' Simplistic module for manipulating MCF files (https://www.moviecontentfilter.com/specification)
'''


class Mcf():
    def __init__(self, start, end):
        self.start = McfTiming(start)
        self.end = McfTiming(end)
        self.segments = []

    @classmethod
    def fromfile(cls, filename):
        with open(filename) as file:
            for line in file:
                if line.startswith('NOTE') or line.startswith('WEBVTT') or len(line.strip()) == 0:
                    continue

                elif line.startswith('START'):
                    mcf_start = line.split()[1]

                elif line.startswith('END'):
                    mcf_end = line.split()[1]

                    mcf = cls(mcf_start, mcf_end)

                elif line[0].isdigit():
                    segment_start_timestamp = line.strip().split()[0]
                    segment_end_timestamp = line.strip().split()[2]

                else:
                    assert line.find('=') != -1

                    mcf.segments.append(
                        McfSegment(
                            segment_start_timestamp,
                            segment_end_timestamp,
                            line.strip()
                        )
                    )

        return mcf

    def write(self, filename):
        with open(filename, 'w') as file:
            file.write('WEBVTT MovieContentFilter 1.0.0\n\n')

            file.write('NOTE\n')
            file.write('START {}\n'.format(self.start))
            file.write('END {}\n'.format(self.end))

            for segment in self.segments:
                file.write('\n{} --> {}\n'.format(segment.start, segment.end))
                file.write('{}\n'.format(segment.text))


class McfSegment():
    def __init__(self, *args):
        self.start = McfTiming(args[0])
        self.end = McfTiming(args[1])
        if len(args) > 2:
            self.text = args[2]


class McfTiming():
    def __init__(self, timestamp):
        if isinstance(timestamp, str):
            self.timedelta = McfTiming.timestamp_to_timedelta(timestamp)
        elif isinstance(timestamp, datetime.timedelta):
            self.timedelta = timestamp
        elif isinstance(timestamp, McfTiming):
            self.timedelta = timestamp.timedelta
        else:
            sys.exit('ERROR: timing is neither a string nor a datetime.timestamp')

    @property
    def microseconds(self):
        return self.timedelta.microseconds

    @property
    def seconds(self):
        return self.timedelta.seconds

    def __add__(self, other):
        return McfTiming(self.timedelta + other.timedelta)

    def __eq__(self, other):
        return self.timedelta == other

    def __mul__(self, other):
        return McfTiming(self.timedelta * other)

    def __sub__(self, other):
        return McfTiming(self.timedelta - other.timedelta)

    def __truediv__(self, other):
        return self.timedelta / other.timedelta

    # Output as hh:mm:ss.ttt
    def __str__(self):
        hours, remainder = divmod(self.timedelta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        microseconds = self.timedelta.microseconds

        return '{:02d}:{:02d}:{:02d}.{}'.format(
            int(hours),
            int(minutes),
            int(seconds),
            str('{:06d}'.format(self.timedelta.microseconds))[0:3]
        )

    # Timestamp spec: https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API#Cue_timings
    @staticmethod
    def timestamp_to_timedelta(timestamp_string):
        # hh:mm:ss.ttt
        if timestamp_string.count(':') == 2:
            hours, minutes, seconds_milliseconds = timestamp_string.split(':')
        # mm:ss.ttt
        elif timestamp_string.count(':') == 1:
            hours = 0
            minutes, seconds_milliseconds = timestamp_string.split(':')
        else:
            sys.exit('ERROR: invalid timestamp ({})\n'.format(timestamp_string))

        seconds, milliseconds = seconds_milliseconds.split('.')

        return datetime.timedelta(
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds),
            milliseconds=int(milliseconds)
        )
