#!/usr/bin/env python3

''' Adjust timestamps in MCF files (https://www.moviecontentfilter.com/specification) for new releases
'''

import sys

import mcf


class VideoSegment():
    def __init__(self, start, end):
        self.start = start
        self.end = end


def main():
    if len(sys.argv) < 3:
        sys.exit('USAGE: %s /path/to/input-filter.mcf /path/to/output-filter.mcf' % (sys.argv[0]))

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    old_mcf = mcf.Mcf.fromfile(input_filename)

    old_offset = old_mcf.start

    new_mcf_start = input('Please enter start timestamp of new release: ')
    new_mcf_end = input('Please enter end timestamp of new release: ')

    new_mcf = mcf.Mcf(new_mcf_start, new_mcf_end)

    for old_segment in old_mcf.segments:
        new_segment_start = adjust_segment_timing(old_mcf, new_mcf, old_segment.start)
        new_segment_end = adjust_segment_timing(old_mcf, new_mcf, old_segment.end)

        new_mcf.segments.append(mcf.McfSegment(new_segment_start, new_segment_end, old_segment.text))

    new_mcf.write(output_filename)


def adjust_segment_timing(old_mcf, new_mcf, old_segment_timing):
    old_adjusted_segment_timing = old_segment_timing - old_mcf.start
    old_duration = old_mcf.end - old_mcf.start
    new_duration = new_mcf.end - new_mcf.start

    new_adjusted_segment_timing = old_adjusted_segment_timing * (new_duration / old_duration)
    new_segment_timing = new_adjusted_segment_timing + new_mcf.start

    return new_segment_timing


if __name__ == '__main__':
    main()
