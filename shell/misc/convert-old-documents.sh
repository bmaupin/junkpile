#!/bin/bash

if ps -ef | grep [s]office -q; then
    echo "Warning: LibreOffice is open and document conversion may fail"
fi

declare -A extensions

extensions=(
    # MS Word document
    #["doc"]="odt"
    # MS Works database
    ["wdb"]="ods"
    # MS Works spreadsheet
    ["wks"]="ods"
    # MS Works document
    ["wps"]="odt"
    # MS Write document
    ["wri"]="odt"
)

for old_extension in "${!extensions[@]}"; do
    for old_filepath in `find . | grep -i ".$old_extension$"`; do
        current_directory=`pwd`
        file_directory=`dirname $old_filepath`
        old_actual_extension="${old_filepath##*.}"
        new_extension=${extensions[$old_extension]}
        old_filename=`basename $old_filepath`
        new_filename="${old_filename%.$old_actual_extension}.$new_extension"

        pushd "$file_directory" > /dev/null

        # Make sure the new file hasn't been created yet
        if [ ! -f $new_filename ]; then
            echo "Converting $current_directory/$file_directory/$old_filename to $new_filename"

            original_timestamp=`stat -c "%Y" "$old_filename"`

            soffice --headless --convert-to $new_extension "$old_filename"

            # Set the timestamp of the converted file to the timestamp of the original file
            touch -d @$original_timestamp "$new_filename"
        fi

        popd > /dev/null
    done
done
