#!/bin/bash

# Define mappings for directory names to system names and cheat directories
declare -A SYSTEM_MAP=(
    ["FC"]="Nintendo - Nintendo Entertainment System"
    ["GB"]="Nintendo - Game Boy"
    ["GBA"]="Nintendo - Game Boy Advance"
    ["GBC"]="Nintendo - Game Boy Color"
    ["MD"]="Sega - Mega Drive - Genesis"
    ["SFC"]="Nintendo - Super Nintendo Entertainment System"
)

declare -A CHEAT_DIR_MAP=(
    ["FC"]="FCEUmm"
    ["GB"]="Gambatte"
    ["GBA"]="mGBA"
    ["GBC"]="Gambatte"
    ["MD"]="PicoDrive"
    ["SFC"]="Supafaust"
)

# Base paths
ROM_BASE="/media/$USER/Roms/Roms"
# ROM_BASE="/media/$USER/Roms/Roms/FROZEN"
CHEAT_DEST_BASE="/media/$USER/Roms/CFW/retroarch/.retroarch/cheats"
# Uncomment to test first
# CHEAT_DEST_BASE="/tmp/cheats"

# Function to URL-encode strings using jq
urlencode() {
    local STRING="$1"
    echo -n "$STRING" | jq -sRr @uri
}

# Iterate through each directory in the ROM base path
for DIR in "$ROM_BASE"/*; do
    if [ -d "$DIR" ]; then
        DIR_NAME=$(basename "$DIR")

        # Check if the directory name is in the system map
        if [[ -n "${SYSTEM_MAP[$DIR_NAME]}" ]]; then
            SYSTEM_NAME="${SYSTEM_MAP[$DIR_NAME]}"
            CHEAT_DIR="${CHEAT_DIR_MAP[$DIR_NAME]}"

            # URL-encode the system name
            ENCODED_SYSTEM_NAME=$(urlencode "$SYSTEM_NAME")

            # Iterate through each ROM in the directory
            for ROM in "$DIR"/*; do
                if [ -f "$ROM" ]; then
                    ROM_NAME=$(basename "$ROM")
                    ROM_NAME_NO_EXT="${ROM_NAME%.*}"

                    # URL-encode the ROM name
                    ENCODED_ROM_NAME_NO_EXT=$(urlencode "$ROM_NAME_NO_EXT")

                    # Construct the cheat file URL
                    CHEAT_URL="https://raw.githubusercontent.com/libretro/libretro-database/refs/heads/master/cht/${ENCODED_SYSTEM_NAME}/${ENCODED_ROM_NAME_NO_EXT}.cht"

                    # Destination path for the cheat file
                    DEST_DIR="$CHEAT_DEST_BASE/$CHEAT_DIR"
                    mkdir -p "$DEST_DIR"
                    DEST_FILE="$DEST_DIR/${ROM_NAME_NO_EXT}.cht"

                    # Download the cheat file
                    echo "Downloading cheat file for $ROM_NAME..."
                    curl -s -o "$DEST_FILE" "$CHEAT_URL"

                    if [ $? -eq 0 ]; then
                        echo "Cheat file saved to $DEST_FILE"
                    else
                        echo "Failed to download cheat file for $ROM_NAME"
                    fi
                fi
            done
        else
            echo "No system mapping found for directory: $DIR_NAME"
        fi
    fi
done