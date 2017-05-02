import datetime
import sys


''' Simplistic module for manipulating MCF files (https://www.moviecontentfilter.com/specification)
'''


class McfSegment():
    def __init__(self, start, end, text):
        if isinstance(start, str):
            self.start = McfUtil.timestamp_to_timedelta(start)
        elif isinstance(start, datetime.timedelta):
            self.start = start
        else:
            sys.exit('ERROR: start timing is neither a string nor a datetime.timestamp')

        if isinstance(end, str):
            self.end = McfUtil.timestamp_to_timedelta(end)
        elif isinstance(end, datetime.timedelta):
            self.end = end
        else:
            sys.exit('ERROR: end timing is neither a string nor a datetime.timestamp')

        self.text = text


class Mcf():
    def __init__(self, start, end):
        self.start = McfUtil.timestamp_to_timedelta(start)
        self.end = McfUtil.timestamp_to_timedelta(end)
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


class McfUtil():
    @staticmethod
    # Timestamp spec: https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API#Cue_timings
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

    @staticmethod
    def timedelta_to_timestamp(timedelta):
        hours, remainder = divmod(timedelta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        microseconds = timedelta.microseconds

        return '{:02d}:{:02d}:{:02d}:{}'.format(
            int(hours),
            int(minutes),
            int(seconds),
            str('{:06d}'.format(timedelta.microseconds))[0:3]
        )
