- fix-srt-subtitle.py
  - Fixes the following issues with SRT subtitle files:

    1. Adds a blank subtitle to the beginning of the file. Otherwise, when importing SRT subtitle files with avconv for some reason the subtitles start immediately instead of when they're supposed to, making the subtitles appear early for the rest of the entire video.
    2. Makes sure subtitle numbering starts with 1. If it starts with 0, avconv will give the following error:
      > Invalid data found when processing input

    3. Optionally reencodes latin1-encoded SRT subtitle files as utf8. Avconv seems to handle latin1 encoded files just fine, but it's nice to have it as utf8 just in case.

    Run the script to get syntax and options.
