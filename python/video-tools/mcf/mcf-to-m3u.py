#!/usr/bin/env python3

''' Convert MCF files (https://www.moviecontentfilter.com/specification) to M3U playlists for previewing
'''

import sys

import mcf


def main():
    if len(sys.argv) < 4:
        sys.exit('USAGE: %s /path/to/filter.mcf /path/to/video /path/to/playlist.m3u' % (sys.argv[0]))

    mcf_filename = sys.argv[1]
    video_filename = sys.argv[2]
    m3u_filename = sys.argv[3]

    segments_to_omit = mcf.Mcf.fromfile(mcf_filename).segments

    segments_to_play = get_segments_to_play(segments_to_omit)

    write_m3u(segments_to_play, video_filename, m3u_filename)


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


def write_m3u(segments_to_play, video_filename, m3u_filename):
    with open(m3u_filename, 'w') as m3u_file:
        for segment in segments_to_play:
            m3u_file.write('#EXTVLCOPT:start-time={}\n'.format(
                mcftiming_to_m3u_timestamp(segment.start)))
            m3u_file.write('#EXTVLCOPT:stop-time={}\n'.format(
                mcftiming_to_m3u_timestamp(segment.end)))
            m3u_file.write('{}\n\n'.format(video_filename))


def mcftiming_to_m3u_timestamp(mcf_timing):
    return ('{}.{}'.format(
        str(mcf_timing.seconds),
        '{:06d}'.format(mcf_timing.microseconds)[0:3],
    ))


if __name__ == '__main__':
    main()
