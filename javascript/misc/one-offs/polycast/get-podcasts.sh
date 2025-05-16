#!/usr/bin/env bash

dest_dir="/home/$USER/Downloads/polycast"
script_dir=$(pwd)

mkdir -p "$dest_dir"
cd "$dest_dir"

for url in $(grep '<guid>' "${script_dir}/polycast-modcast.xml" | cut -d '>' -f 2 | cut -d '<' -f 1); do
    filename=$(basename "$url")
    if [ -f "$filename" ]; then
        continue
    fi
    while ! wget "$url"; do
        echo "Failed to download $url. Retrying in 1 minute..."
        sleep 60
    done
done
