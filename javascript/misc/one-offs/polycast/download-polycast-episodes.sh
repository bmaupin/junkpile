#!/usr/bin/env bash

dest_dir="/home/$USER/Downloads/polycast"
start_at_episode="episode255.mp3"
script_dir=$(pwd)

mkdir -p "$dest_dir"
cd "$dest_dir"

started=false
for url in $(grep '<guid>' "${script_dir}/polycast-modcast.xml" | cut -d '>' -f 2 | cut -d '<' -f 1 | sort -V); do
    filename=$(basename "$url")
    if [ "$started" = false ]; then
        if [ "$filename" = "$start_at_episode" ]; then
            started=true
        else
            continue
        fi
    fi
    if [ -f "$filename" ]; then
        continue
    fi
    while ! wget "$url"; do
        echo "Failed to download $url. Retrying in 1 minute..."
        sleep 60
    done
done
