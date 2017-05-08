#!/usr/bin/env python3

''' Edit videos based on MCF files (https://www.moviecontentfilter.com/specification)
'''

import os
import subprocess
import sys

import mcf


def main():
    if len(sys.argv) < 4:
        sys.exit('USAGE: %s /path/to/filter.mcf /path/to/input-video /path/to/output-video' % (sys.argv[0]))

    mcf_filename = sys.argv[1]
    input_filename = sys.argv[2]
    output_filename = sys.argv[3]

    segments_to_omit = mcf.Mcf.fromfile(mcf_filename).segments

    segments_to_play = get_segments_to_play(segments_to_omit)

    cut_video(segments_to_play, input_filename, output_filename)

    # TODO: join segments


def cut_video(segments_to_play, input_filename, output_filename):
    for i, segment in enumerate(segments_to_play):
        segment_filename = '{}-{}{}'.format(
            os.path.splitext(output_filename)[0],
            i,
            os.path.splitext(output_filename)[1])

        if i != len(segments_to_play) - 1:
            cut_segment(segment.start, segment.end, input_filename, segment_filename)
        else:
            cut_last_segment(segment.start, input_filename, segment_filename)


def get_segments_to_play(segments_to_omit):
    segments_to_play = []
    skip_next_segment = False

    for i in range(len(segments_to_omit)):
        if i == 0:
            segments_to_play.append(
                mcf.McfSegment(
                    mcf.McfTiming('00:00:00.000'),
                    segments_to_omit[i].start
                )
            )

        else:
            # TODO: this will only handle up to 2 back-to-back filters
            if skip_next_segment == True:
                skip_next_segment = False
                continue

            else:
                if i != len(segments_to_omit) - 1 and segments_to_omit[i].end == segments_to_omit[i + 1].start:
                    skip_next_segment = True

                segments_to_play.append(
                    mcf.McfSegment(
                        segments_to_omit[i - 1].end,
                        segments_to_omit[i].start
                    )
                )

    segments_to_play.append(
        mcf.McfSegment(
            segments_to_omit[-1].end,
            mcf.McfTiming('00:00:00.000')
            )
        )

    return segments_to_play


def cut_segment(start, end, input_filename, segment_filename):
    run_command('ffmpeg -i {} -ss {} -t {} -c:v libx264 -q:v 1 -c:a copy -c:s copy {}'.format(
        input_filename,
        start,
        end - start,
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
        start,
        segment_filename))


if __name__ == '__main__':
    main()
