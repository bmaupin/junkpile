#!/usr/bin/env python3

''' Edit videos based on MCF files (https://www.moviecontentfilter.com/specification)
'''

import argparse
import datetime
import os
import subprocess

import mcf


# Amount of time to add on either end of preview cuts
PREVIEW_LENGTH_IN_SECONDS = 5


def main():
    args = parse_arguments()

    segments_to_omit = mcf.Mcf.fromfile(args.mcf_filename).segments

    segments_to_play = get_segments_to_play(segments_to_omit, args.preview)

    cut_video(segments_to_play, args.input_filename, args.output_filename)

    # TODO: join segments


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('mcf_filename', metavar='/path/to/filter.mcf')
    parser.add_argument('input_filename', metavar='/path/to/input-video')
    parser.add_argument('output_filename', metavar='/path/to/output-video')

    parser.add_argument('-p', '--preview', action='store_true', help='Create a preview of cuts to be made')

    args = parser.parse_args()
    return args


def cut_video(segments_to_play, input_filename, output_filename):
    for i, segment in enumerate(segments_to_play):
        segment_filename = '{}-{}{}'.format(
            os.path.splitext(output_filename)[0],
            i,
            os.path.splitext(output_filename)[1])

        cut_segment(segment.start, segment.end, input_filename, segment_filename)


def get_segments_to_play(segments_to_omit, preview):
    if preview == True:
        return get_preview_segments_to_play(segments_to_omit)
    else:
        return get_normal_segments_to_play(segments_to_omit)


def get_preview_segments_to_play(segments_to_omit):
    segments_to_play = []

    # TODO: This won't handle if segments are less than PREVIEW_LENGTH_IN_SECONDS apart
    for i, segment_to_omit in enumerate(segments_to_omit):
        # Skip back-to-back segments
        if i != len(segments_to_omit) - 1 and segments_to_omit[i].end == segments_to_omit[i + 1].start:
            continue

        segments_to_play.append(
            mcf.McfSegment(
                segment_to_omit.start - mcf.McfTiming(datetime.timedelta(seconds=PREVIEW_LENGTH_IN_SECONDS)),
                segment_to_omit.start
            )
        )

        segments_to_play.append(
            mcf.McfSegment(
                segment_to_omit.end,
                segment_to_omit.end + mcf.McfTiming(datetime.timedelta(seconds=PREVIEW_LENGTH_IN_SECONDS))
            )
        )

    return segments_to_play


def get_normal_segments_to_play(segments_to_omit):
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
