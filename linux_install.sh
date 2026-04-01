#!/bin/sh

# Makes a copy of the .desktop file to .local/share/applications

location=$(pwd)
username=$(whoami)
desktop_file="/home/$username/.local/share/applications/ytdlp-menu.desktop"
image_file="/home/$username/.local/share/applications/yt-dlp.png"

# first check if the applications directory in .local/share exists
localshare="/home/$username/.local/share/applications/"
if [ -d "$localshare" ]; then
    echo "applications directory already created..."
else
    echo "Creating applications directory in .local/share/ ..."
    mkdir $localshare
fi

cp ytdlp-menu.desktop $desktop_file
cp yt-dlp.png $image_file
echo "Icon=$image_file" >> $desktop_file
chmod u+x $desktop_file

# checks if "Path = " already exists in the .desktop file

if ! grep -q "Path =" "$desktop_file"; then
    echo "Path = $location" >> "$desktop_file"
else
    echo "Path already exists on $desktop_file."
fi

if [ -f "$desktop_file" ]; then
	echo ".destop file already at $localshare"
else
	echo "A desktop file was created in .local/share/applications, launch as ytdlp Menu!"
fi
