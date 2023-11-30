#!/usr/bin/env bash

ROM_DIRECTORY="${HOME}/Desktop/RG35XX/SD card/Roms/"

# TODO: parse through different systems

system="GB"

case $system in
    GB)
        base_url="https://raw.githubusercontent.com/libretro-thumbnails/Nintendo_-_Game_Boy/master/Named_Boxarts/"
        ;;

    *)
        echo "Unmatched system directory in Roms: ${system}"
        exit 1
        ;;
esac

# Put all of the ROM filenames into an array
mapfile -t roms <<< $(find "${ROM_DIRECTORY}/${system}" -maxdepth 1 -type f)

for rom_path in "${roms[@]}"; do
    # Strip off the path and the extension
    game_name=$(basename -- "${rom_path}" ".${rom_path##*.}")
    wget "${base_url}/${game_name}.png" -O "${game_name}.png"
    # Get the file type of the downloaded file in case it's not an image
    filetype=$(file "${game_name}.png" | cut -d : -f 2 | xargs)
    # If the file is a text file, it contains the image name we should use
    if [[ "${filetype}" == ASCII\ text* ]]; then
        image_name=$(cat "${game_name}.png")
        # Try the download again
        wget "${base_url}/${image_name}" -O "${game_name}.png"
        # Remove the text file
        rm "${game_name}.png"
    fi
done
