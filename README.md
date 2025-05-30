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

This is a rewrite of another program that I've made called [yt-dlp simpleGUI](https://github.com/MxEmexis/yt-dlp-simpleGUI). 

The goal is to do a even simpler approach to interact with the yt-dlp binary via terminal.

## To be used with the standalone yt-dlp binary
This program is set to work with the standalone `yt-dlp` binary that is available [here](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp). Since it is not recommended to use the binaries from your distro repo or pip, I generally put this file in my script folder that is set as PATH `.bash.rc`, you can do something similar in Windows using [Cmder](https://cmder.app).

## Libraries used

- `platform`
- `shlex`
- `os`

## Build
You simply run the code via python, building a executable via `pyinstaller` may lead to some permission errors when downloading in some situations.

It is the same build method, using `pyinstaller`. If any doubt check the yt-dlp simpleGUI readme for more info.

***
At the moment, the focus is working in Linux, tests on Windows haven't been made yet... 