import platform
import shlex
import subprocess
import os

# VARIABLES, FLAGS and CHECKS
# ______________
browser_cookie_check = False
metadata_check = False
subs_check = False
folder_check = False

video_link = str("")
browser_name = str("")
format_name = str("none")

metadata_flag = str(" --embed-metadata --embed-thumbnail")
subs_flag = str(" --all-subs")
cookies_flag = str(" --cookies from browser")
folder_path_flag = str(" -P")

ytdlp_bin = ""

# check for OS and change the yt-dlp binary name accordingly
system = platform.system()
if system == "Linux":
    ytdlp_bin = "./yt-dlp"
    print ("System: Linux")
elif system == "Windows":
    ytdlp_bin = "yt-dlp.exe"
    print ("System: Windows")

download_combo = ""

# setup for where the downloaded files go, it reads a .txt file named "yt-dlp-path.txt" and sets the path as the first line of the document
try:
    f = open('ytdlp-path.txt','x')
except FileExistsError:
    print("File for path read already created as ytdlp-path.txt")
with open('ytdlp-path.txt') as f:
    folder_path = f.read()

# cool logo :)
print(r"""
__               __            ____    
\ \       __  __/ /_      ____/ / /___ 
 \ \     / / / / __/_____/ __  / / __ \
 / /    / /_/ / /_/_____/ /_/ / / /_/ /
/_/_____\__, /\__/      \__,_/_/ .___/ 
 /_____/____/      simple CLI /_/
 version 0.0.1 - by MxEmexis    
""")

# process for URL download
def set_combo():
    global download_combo, cookies_flag, folder_path
    download_combo = ytdlp_bin + formato + (" ") + video_link + (" --no-part --restrict-filenames")

    if metadata_check == True:
        download_combo+=metadata_flag
    elif subs_check == True:
        download_combo+=subs_flag
    elif browser_cookie_check == True:
        cookies_flag+=str(" ")+browser_name
        download_combo+=cookies_flag

    args = shlex.split(download_combo)
    a=' '.join(args)
    print(a)

    # note: the subprocess method should be better here, however it create some problems with yt-dlp due to the
    # way it runs, so I replaced it with the following command, that, although it is said to be less secure due to
    # potential shell injection vulnerabilities, it is the only way to make yt-dlp work without spilling errors
    # or corrupting the files in the download process
    os.system(a)

# main loop
while True:
    print("____________________________")
    print("i) to insert URL | f) media formats\nb) set browser cookies | p) set folder path\nr) reset parameters | q) to quit")
    print("----------------------------")
    print(f"Format: {format_name}")
    print(f"Mp3 Metadata: {metadata_check} | Video Subtitles: {subs_check}")
    print(f"Browser Cookies: {browser_name} | Folder path: {folder_path}")
    print("____________________________")
    comando=str(input("Select a option: "))

    try:
        if comando == "i":
            video_link=str(input("Insert URL: "))
            set_combo()

        elif comando == "f":
            print("Please select the media format:")
            print("1) mp4 | 2) mp3")
            formato_sel = str(input(": "))
            if formato_sel == "1":
                print("Format set to Mp4")
                formato = str(" -t mp4") # preset alias from yt-dlp
                format_name = str("Mp4")
                sub_check = str(input("save subtitles? (y) or (n)?"))
                if sub_check == "y":
                    subs_check = True
                elif sub_check == "n":
                    subs_check = False
                else:
                    print("Invalid command, setting subtitles check to False")
                    subs_check = False
            elif formato_sel == "2":
                print("Format set to Mp3")
                formato = str(" -t mp3")  # preset alias from yt-dlp
                meta_check = str(input("save metadata? (y) or (n)?"))
                if meta_check == "y":
                    metadata_check = True
                elif meta_check == "n":
                    metadata_check = False
                else:
                    print("Invalid command, setting metadata check to False")
                    metadata_check = False
                format_name = str("Mp3")
            else:
                print("Invalid command, try again...")

        elif comando == "b":
            browser_name = str(input("Select Browser name...\nSupported browsers are: brave, chrome, chromium, edge,\nfirefox, opera, safari, vivaldi, whale.\nYou must be logged in on the targeted website.\n:"))
            browser_cookie_check = True

        elif comando == "p":
            path_confirm = str(input("do you want to use the default folder or set another? (default is /Videos)\n(d) for default, (y) for set a new one, (n) for none: "))
            if path_confirm == "y":
                p=str(input("Please set the new folder path: "))
                with open('ytdlp-path.txt','w') as f:
                    f.write(p)
                with open('ytdlp-path.txt') as f:
                    folder_path = f.read()
                folder_check = True
            elif path_confirm == "d":
                with open('ytdlp-path.txt','w') as f:
                    f.write("/Videos")
                with open('ytdlp-path.txt') as f:
                    folder_path = f.read()
                folder_check = True
            elif path_confirm == "n":
                folder_check = False
            else:
                print("Not a recognized command.")

        elif comando == "r":
            print("1) browser cookies | 2) metadata | 3) subtitles")
            reset_choice = str(input("Select which parameter to reset: "))
            if reset_choice == "1":
                browser_cookie_check = False
            elif reset_choice == "2":
                metadata_check = False
            elif reset_choice == "3":
                subs_check = False
            else:
                print("Invalid command.")

        elif comando == "q":
            print("Bye bye!")
            break
        else:
            print("Not a recognized command, try again...")

    except ValueError:
        print("Invalid option, try again...")


