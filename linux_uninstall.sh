#!/bin/sh

desktop_file="$HOME/.local/share/applications/ytdlp-menu.desktop"

if [ -f "$desktop_file" ]; then
    rm "$desktop_file"
    echo "The file $desktop_file was sucessfully removed."
else
    echo "$desktop_file does not exist."
fi