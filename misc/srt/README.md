Cleaning up subtitles:

1. Run ../../python/video-tools/fix-srt-subtitle.py
    - Converts Windows line endings to Unix
    - Converts encoding to UTF8
    - Makes sure file ends with a newline
    - Optionally adjusts timestamps as desired

2. Fix OCR errors
    - English
        - Search: `([^\w])l([^\w])`
          Replace: `\1I\2`
