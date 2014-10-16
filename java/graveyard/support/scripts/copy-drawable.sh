#!/bin/bash

SOURCE=~/workspace/git/android/platform/packages/apps/Mms
DEST=~/workspace/git/android-sms-merge/android_sms_merge

drawable_folders="drawable-hdpi drawable-mdpi drawable-xhdpi drawable-xxhdpi"

if [ -z "$1" ]; then
    echo "Must provide filename"
    exit 1
fi

for folder in $drawable_folders; do
    if [ -f "$SOURCE/res/$folder/$1" ]; then
        cp "$SOURCE/res/$folder/$1" "$DEST/res/$folder"
    else
        echo "$SOURCE/res/$folder/$1 doesn't exist"
    fi
done

