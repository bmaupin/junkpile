#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: `basename $0` input.[mp3/wav] output.[mp3/wav]"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Error: input file doesn't exist: $1"
    exit 1
fi

if [ -f "$2" ]; then
    echo "Error: output file already exists: $2"
    exit 1
fi

infilepath="$1"
outfilepath="$2"
inextension="${infilepath##*.}"
outextension="${outfilepath##*.}"

if [ "$inextension" != "$outextension" ]; then
    echo "Error: input file extension must match output file extension"
    exit 1
fi

if [ "$inextension" == "wav" ]; then
    inwavpath="$infilepath"
    outwavpath="$outfilepath"

elif [ "$inextension" == "mp3" ]; then
    echo "Please wait..."

    inwavpath="${infilepath%.*}".wav
    outwavpath="${outfilepath%.*}".wav

    # Convert mp3 to wav
    ffmpeg -loglevel error -i "$infilepath" "$inwavpath"

else
    echo "Error: input file must be mp3 or wav"
    exit 1
fi

/opt/Levelator-1.3.0-Python2.5/levelator "$inwavpath" "$outwavpath"

if [ "$inextension" == "mp3" ]; then
    # Create a temp file
    tempfile=`mktemp /tmp/XXXXXXXXXX.mp3`

    # Convert wav to mp3
    ffmpeg -loglevel error -y -i "$outwavpath" "$tempfile"

    # If the input file contains a video stream (album art, etc)
    if ffprobe "$infilepath" 2>&1 | grep -q "Stream.*Video"; then
        # Copy metadata and any video streams from the original file to the final output file
        ffmpeg -loglevel error -i "$infilepath" -i "$tempfile" -map_metadata 0 -map 1:a -c:a copy -map 0:v -c:v copy "$outfilepath"

    else
        # Copy metadata from the original file to the final output file
        ffmpeg -loglevel error -i "$infilepath" -i "$tempfile" -map_metadata 0 -map 1:a -c:a copy "$outfilepath"
    fi

    # Cleanup
    rm "$inwavpath" "$outwavpath" "$tempfile"
fi
