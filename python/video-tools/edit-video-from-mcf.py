#!/usr/bin/env python3

import datetime
import os
import subprocess


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


def timestamp_to_timedelta(timestamp_string):
    return datetime.timedelta(
        hours=int(timestamp_string[0:2]),
        minutes=int(timestamp_string[3:5]),
        seconds=int(timestamp_string[6:8]),
        milliseconds=int(timestamp_string[9:12]))


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


def timedelta_to_timestamp(timedelta):
    return str(timedelta)


if __name__ == '__main__':
    main()
