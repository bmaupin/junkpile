#!/usr/bin/env python

import json
import sys


def main():
    if len(sys.argv) < 3:
        print('Usage: {} INFILE OUTFILE'.format(sys.argv[0]))
        sys.exit()
    
    with open(sys.argv[1], 'r') as infile, open(sys.argv[2], 'w') as outfile:
        outfile.write(
            json.dumps(
                json.loads(
                    infile.read()
                ),
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )
        )


if __name__ == '__main__':
    main()