#!/usr/bin/env python3

''' Edit videos based on MCF files (https://www.moviecontentfilter.com/specification)
'''

import argparse
import os
import subprocess

import mcf


def main():
    args = parse_arguments()

    segments_to_omit = mcf.Mcf.fromfile(args.mcf_filename).segments

    segments_to_play = get_segments_to_play(segments_to_omit)

    cut_video(segments_to_play, args.input_filename, args.output_filename)

    # TODO: join segments


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('mcf_filename', metavar='/path/to/filter.mcf')
    parser.add_argument('input_filename', metavar='/path/to/input-video')
    parser.add_argument('output_filename', metavar='/path/to/output-video')

    args = parser.parse_args()
    return args


def cut_video(segments_to_play, input_filename, output_filename):
    for i, segment in enumerate(segments_to_play):
        segment_filename = '{}-{}{}'.format(
            os.path.splitext(output_filename)[0],
            i,
            os.path.splitext(output_filename)[1])

        cut_segment(segment.start, segment.end, input_filename, segment_filename)


def get_segments_to_play(segments_to_omit):
    segments_to_play = []

    segments_to_play.append(
        mcf.McfSegment(
            mcf.McfTiming('00:00:00.000'),
            segments_to_omit[0].start
        )
    )

    for i in range(len(segments_to_omit)):
        if i == len(segments_to_omit) - 1:
            segment_end = mcf.McfTiming('00:00:00.000')
        else:
            if segments_to_omit[i].end == segments_to_omit[i + 1].start:
                continue

            segment_end = segments_to_omit[i + 1].start

        segments_to_play.append(
            mcf.McfSegment(
                segments_to_omit[i].end,
                segment_end
            )
        )

    return segments_to_play


def cut_segment(start, end, input_filename, segment_filename):
    if end == mcf.McfTiming('00:00:00.000'):
        duration = ''
    else:
        duration = ' -t {} '.format(end - start)

    run_command('ffmpeg -i "{}" -ss {} {} -c:v libx264 -c:a copy -c:s copy "{}"'.format(
        input_filename,
        start,
        duration,
        segment_filename))


def run_command(command):
    print(command)
    p = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    output = p.communicate()[0]


if __name__ == '__main__':
    main()
