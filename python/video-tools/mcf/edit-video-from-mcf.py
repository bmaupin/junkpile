#!/usr/bin/env python3

''' Edit videos based on MCF files (https://www.moviecontentfilter.com/specification)
'''

import argparse
import datetime
import os
import subprocess
import tempfile

import mcf


FADE_IN_DURATION_IN_SECONDS = 1
FADE_OUT_DURATION_IN_SECONDS = 3
# Amount of time to add on either end of preview cuts
PREVIEW_SEGMENT_DURATION_IN_SECONDS = 5


def main():
    args = parse_arguments()

    segments_to_omit = mcf.Mcf.fromfile(args.mcf_filename).segments

    segments_to_play = get_segments_to_play(segments_to_omit, args.preview)

    segment_filenames = edit_video(segments_to_play, args.input_filename, args.output_filename, args.fade, args.preview)

    join_segments(segment_filenames, args.output_filename)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('mcf_filename', metavar='/path/to/filter.mcf')
    parser.add_argument('input_filename', metavar='/path/to/input-video')
    parser.add_argument('output_filename', metavar='/path/to/output-video')

    parser.add_argument('-f', '--fade', action='store_true', help='Fade audio in/out where cuts are made')
    parser.add_argument('-p', '--preview', action='store_true', help='Create a preview of cuts to be made')

    args = parser.parse_args()
    return args


def get_segments_to_play(segments_to_omit, preview):
    if preview == True:
        return get_preview_segments_to_play(segments_to_omit)
    else:
        return get_normal_segments_to_play(segments_to_omit)


def get_preview_segments_to_play(segments_to_omit):
    segments_to_play = []

    # TODO: This won't handle if segments are less than PREVIEW_SEGMENT_DURATION_IN_SECONDS apart
    for i, segment_to_omit in enumerate(segments_to_omit):
        # Skip back-to-back segments
        if i == 0 or segments_to_omit[i].start != segments_to_omit[i - 1].end:
            segments_to_play.append(
                mcf.McfSegment(
                    segment_to_omit.start - mcf.McfTiming(datetime.timedelta(seconds=PREVIEW_SEGMENT_DURATION_IN_SECONDS)),
                    segment_to_omit.start
                )
            )

        if i == len(segments_to_omit) - 1 or segments_to_omit[i].end != segments_to_omit[i + 1].start:
            segments_to_play.append(
                mcf.McfSegment(
                    segment_to_omit.end,
                    segment_to_omit.end + mcf.McfTiming(datetime.timedelta(seconds=PREVIEW_SEGMENT_DURATION_IN_SECONDS))
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


def edit_video(segments_to_play, input_filename, output_filename, fade, preview):
    segment_filenames = []
    video_parameters = ''

    for i, segment in enumerate(segments_to_play):
        segment_filename = '{}-{}{}'.format(
            os.path.splitext(output_filename)[0],
            i,
            os.path.splitext(output_filename)[1])
        segment_filenames.append(segment_filename)

        fade_in = False
        fade_out = False

        if fade == True:
            if preview == True:
                if is_even(i):
                    fade_out = True
                else:
                    fade_in = True

            else:
                if segment.start != mcf.McfTiming('00:00:00.000'):
                    fade_in = True
                if segment.end != mcf.McfTiming('00:00:00.000'):
                    fade_out = True

        video_parameters += get_segment_parameters(segment.start, segment.end, segment_filename, fade_in, fade_out)

    run_command('ffmpeg -v quiet -stats -i "{}" {}'.format(input_filename, video_parameters))

    return segment_filenames


def is_even(integer):
    return integer % 2 == 0


def get_segment_parameters(start, end, segment_filename, fade_in, fade_out):
    if end == mcf.McfTiming('00:00:00.000'):
        cut_duration = ''
    else:
        cut_duration = ' -t {} '.format(end - start)

    if fade_in == True and fade_out == True:
        audio_parameter = (' -c:a aac -ac 2 -af "afade=t=in:curve=qua:st={}:d={},'
            'afade=out:curve=cbr:st={}:d={}" -strict -2 '.format(
                mcf_timing_to_afade_timestamp(start),
                FADE_IN_DURATION_IN_SECONDS,
                mcf_timing_to_afade_timestamp(end - mcf.McfTiming(datetime.timedelta(seconds=FADE_OUT_DURATION_IN_SECONDS))),
                FADE_OUT_DURATION_IN_SECONDS))
    elif fade_in == True:
        audio_parameter = ' -c:a aac -ac 2 -af "afade=t=in:curve=qua:st={}:d={}" -strict -2 '.format(
            mcf_timing_to_afade_timestamp(start),
            FADE_IN_DURATION_IN_SECONDS)
    elif fade_out == True:
        audio_parameter = ' -c:a aac -ac 2 -af afade=out:curve=cbr:st={}:d={} -strict -2 '.format(
            mcf_timing_to_afade_timestamp(end - mcf.McfTiming(datetime.timedelta(seconds=FADE_OUT_DURATION_IN_SECONDS))),
            FADE_OUT_DURATION_IN_SECONDS)
    else:
        audio_parameter = ' -c:a copy '

    return ' -ss {} {} -map 0 -c:v libx264 {} -c:s copy "{}" '.format(
        start,
        cut_duration,
        audio_parameter,
        segment_filename)


def mcf_timing_to_afade_timestamp(mcf_timing):
    return str(mcf_timing.timedelta.total_seconds())


def run_command(command):
    print(command)
    p = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True)
    for line in p.stdout:
        if line.startswith('frame'):
            line = '\r{}'.format(line.strip())
        print(line, end='', flush=True)
    print()


def join_segments(segment_filenames, output_filename):
    segments_file_path = create_segments_file(segment_filenames)

    run_command('ffmpeg -v quiet -stats -f concat -safe 0 -i "{}" -map 0 -c copy "{}"'.format(
        segments_file_path, output_filename))

    # TODO: remove segment files
    os.remove(segments_file_path)


def create_segments_file(segment_filenames):
    segments_file_handle, segments_file_path = tempfile.mkstemp(dir=os.getcwd())

    with open(segments_file_path, 'w') as segments_file:
        for segment_filename in segment_filenames:
            segments_file.write("file '{}'\n".format(segment_filename))

    os.close(segments_file_handle)

    return segments_file_path


if __name__ == '__main__':
    main()
