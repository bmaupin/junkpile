#!/usr/bin/env python3

''' Edit videos based on MCF files (https://github.com/delight-im/MovieContentFilter)
'''

import datetime
import os
import subprocess
import sys


class VideoSegment():
    def __init__(self, start, end):
        self.start = start
        self.end = end


def main():
    if len(sys.argv) < 4:
        sys.exit('USAGE: %s /path/to/filter.mcf /path/to/input-video /path/to/output-video' % (sys.argv[0]))

    mcf_filename = sys.argv[1]
    input_filename = sys.argv[2]
    output_filename = sys.argv[3]

    segments_to_omit = parse_mcf_file(mcf_filename)

    cut_video(segments_to_omit, input_filename, output_filename)

    # TODO: join segments


def parse_mcf_file(mcf_filename):
    segments_to_omit = []

    with open(mcf_filename, 'r') as mcf_file:
        for line in mcf_file:
            if len(line) == 0:
                continue

            if line[0].isdigit():
                cut_start_timestamp, cut_end_timestamp = line.strip().split(' --> ')

                segments_to_omit.append(
                    VideoSegment(
                        timestamp_to_timedelta(cut_start_timestamp),
                        timestamp_to_timedelta(cut_end_timestamp)
                    )
                )

    return segments_to_omit


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


def cut_video(segments_to_omit, input_filename, output_filename):
    for i in range(len(segments_to_omit)):
        segment_filename = '{}-{}{}'.format(
            os.path.splitext(output_filename)[0],
            i,
            os.path.splitext(output_filename)[1])

        if i == 0:
            cut_first_segment(segments_to_omit[i].start, input_filename, segment_filename)
        else:
            cut_segment(segments_to_omit[i - 1].end, segments_to_omit[i].start, input_filename, segment_filename)

        segment_filename = '{}-{}{}'.format(
            os.path.splitext(output_filename)[0],
            len(segments_to_omit),
            os.path.splitext(output_filename)[1])

    cut_last_segment(segments_to_omit[-1].end, input_filename, segment_filename)


def cut_first_segment(end, input_filename, segment_filename):
    start = datetime.timedelta(0)
    cut_segment(start, end, input_filename, segment_filename)


def cut_segment(start, end, input_filename, segment_filename):
    run_command('ffmpeg -i {} -ss {} -t {} -c:v libx264 -q:v 1 -c:a copy -c:s copy {}'.format(
        input_filename,
        timedelta_to_timestamp(start),
        timedelta_to_timestamp(end - start),
        segment_filename))


def timedelta_to_timestamp(timedelta):
    return str(timedelta)


def run_command(command):
    print(command)
    p = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    output = p.communicate()[0]


def cut_last_segment(start, input_filename, segment_filename):
    run_command('ffmpeg -i {} -ss {} -c:v libx264 -q:v 1 -c:a copy -c:s copy {}'.format(
        input_filename,
        timedelta_to_timestamp(start),
        segment_filename))


if __name__ == '__main__':
    main()
