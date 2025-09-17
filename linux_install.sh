#!/bin/sh

# Makes a copy of the .desktop file to .local/share/applications

location=$(pwd)
username=$(whoami)
desktop_file="/home/$username/.local/share/applications/ytdlp-menu.desktop"

cp ytdlp-menu.desktop $desktop_file
chmod u+x $desktop_file

# checks if "Path = " already exists in the .desktop file

if ! grep -q "Path =" "$desktop_file"; then
    echo "Path = $location" >> "$desktop_file"
else
    echo "Path already exists on $desktop_file."
fi

echo "A desktop file was created in .local/share/applications, launch as ytdlp Menu!"