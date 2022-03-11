#!/usr/bin/env python3

import subprocess

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
        #print('\r{}'.format(line.strip()), end='', flush=True)
        #print(line.replace('\n', '\r'), end='', flush=True)
        # else:
        #     print(line, end='', flush=True)
    print()


run_command('/usr/bin/ffmpeg  -i "/home/user/Desktop/temp-edit/abs/The Extraordinary Adventures Of Adele Blanc-Sec 2010 720p BRRip x264 (mkv) [stb.rg].mkv" -ss 0 -t 00:00:05.000 -c:v libx264 -c:s copy -c:a copy /home/user/Desktop/temp-edit/abs/test-ffmpeg.mkv')
#run_command('ffmpeg --help')

#run_command(['/usr/bin/ffmpeg', '-i', '/home/bmaupin/Desktop/temp-edit/abs/The Extraordinary Adventures Of Adele Blanc-Sec 2010 720p BRRip x264 (mkv) [stb.rg].mkv', '-ss', '0', '-t', '00:00:05.000', '-c:v', 'libx264', '-c:s', 'copy', '-c:a', 'copy', '/home/bmaupin/Desktop/temp-edit/abs/test-ffmpeg.mkv'])