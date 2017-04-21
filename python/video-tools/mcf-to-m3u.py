#!/usr/bin/env python3

''' Convert MCF files (https://www.moviecontentfilter.com/specification) to M3U playlists for previewing
'''

import datetime
import sys


class VideoSegment():
    def __init__(self, start, end):
        self.start = start
        self.end = end


def main():
    if len(sys.argv) < 4:
        sys.exit('USAGE: %s /path/to/filter.mcf /path/to/video /path/to/playlist.m3u' % (sys.argv[0]))

    mcf_filename = sys.argv[1]
    video_filename = sys.argv[2]
    m3u_filename = sys.argv[3]

    segments_to_omit = parse_mcf_file(mcf_filename)

    segments_to_play = get_segments_to_play(segments_to_omit)

    write_m3u(segments_to_play, video_filename, m3u_filename)


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


def get_segments_to_play(segments_to_omit):
    segments_to_play = []
    skip_next_segment = False

    for i in range(len(segments_to_omit)):
        if i == 0:
            segments_to_play.append(
                VideoSegment(
                    datetime.timedelta(0),
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
                    VideoSegment(
                        segments_to_omit[i - 1].end,
                        segments_to_omit[i].start
                    )
                )

    segments_to_play.append(
        VideoSegment(
            segments_to_omit[-1].end,
            datetime.timedelta(0)
            )
        )

    return segments_to_play


def write_m3u(segments_to_play, video_filename, m3u_filename):
    with open(m3u_filename, 'w') as m3u_file:
        for segment in segments_to_play:
            m3u_file.write('#EXTVLCOPT:start-time={}\n'.format(
                timedelta_to_m3u_timestamp(segment.start)))
            m3u_file.write('#EXTVLCOPT:stop-time={}\n'.format(
                timedelta_to_m3u_timestamp(segment.end)))
            m3u_file.write('{}\n\n'.format(video_filename))


def timedelta_to_m3u_timestamp(timedelta):
    return ('{}.{}'.format(
        str(timedelta.seconds),
        '{:06d}'.format(timedelta.microseconds)[0:3],
    ))


if __name__ == '__main__':
    main()
