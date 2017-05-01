import datetime
import sys


''' Simplistic library for manipulating MCF files (https://www.moviecontentfilter.com/specification)
'''


class McfSegment():
    def __init__(self, start, end, text):
        self.start = start
        self.end = end
        self.text = text


class Mcf():
    def __init__(self):
        self.start = None
        self.end = None
        self.segments = []

    @classmethod
    def fromfile(cls, filename):
        mcf = cls()

        with open(filename) as file:
            for line in file:
                if line.startswith('NOTE') or line.startswith('WEBVTT') or len(line.strip()) == 0:
                    continue

                elif line.startswith('START'):
                    mcf.start = Mcf.timestamp_to_timedelta(line.split()[1])

                elif line.startswith('END'):
                    mcf.end = Mcf.timestamp_to_timedelta(line.split()[1])

                elif line[0].isdigit():
                    segment_start_timestamp = line.strip().split()[0]
                    segment_end_timestamp = line.strip().split()[2]

                else:
                    assert line.find('=') != -1

                    mcf.segments.append(
                        McfSegment(
                            Mcf.timestamp_to_timedelta(segment_start_timestamp),
                            Mcf.timestamp_to_timedelta(segment_end_timestamp),
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
