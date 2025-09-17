# yt-dlp simpleCLI

```markdown
__               __            ____    
\ \       __  __/ /_      ____/ / /___ 
 \ \     / / / / __/_____/ __  / / __ \
 / /    / /_/ / /_/_____/ /_/ / / /_/ /
/_/_____\__, /\__/      \__,_/_/ .___/ 
 /_____/____/     simple CLI  /_/
                           
```

Command-line utility to interact with yt-dlp

The goal is to do a even simpler approach to interact with the yt-dlp binary via terminal.

This program is originally set to work with both the standalone `yt-dlp` binary that is available [here](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp) or with the version from your package manager. Since it is not recommended to use the binaries from your distro repo or pip as they generally are outdated (at least on Debian-based distros anyway), you can put this file in `.local/share/applications/` in order for it to be called via shell, you can do something similar in Windows using [Cmder](https://cmder.app).

## Funcionalities

- specify between mp4 and mp3 downloads, with or without subtitles and metadata, respectively
- stream online media (using mpv)
- saves history of downloaded links in a csv file

## Libraries

- `platform`
- `shlex`
- `os`
- `subprocess`
- `time`

## Python

- `Python 3.8+`

## Packages needed in PATH

- mpv (or any other MPlayer fork)

## Build
You can simply run the code via the python interpreter, because building a executable via `pyinstaller` may lead to some permission errors when downloading in some situations, since it runs shell commands in the end of the day. The build scripts are included for those who want to try.

## Install
### Linux
Use the `linux_install.sh` script, this creates a copy of the included .desktop file so that the program can be launched from a application menu. It uses the folder path from where you unzip/clone the files as reference.

If you move the folder to somewhere else, run `linux_uninstall.sh` to remove the old file before running the install script again.

### Windows
*WIP*

***
At the moment, the focus is working in Linux (more specifically, Arch, Ubuntu and Debian based distros), tests on Windows have been few at least for the time being.
