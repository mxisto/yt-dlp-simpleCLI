import platform
import shlex
import subprocess
import os

# VARIABLES, FLAGS and CHECKS
# ______________
os.environ['TERM'] = 'xterm'

browser_cookie_check = False
metadata_check = False
subs_check = False
folder_check = True
mpv_custom_flag = False

video_link = str("")
browser_name = str("")
format_name = str("none")

metadata_flag = str(" --embed-metadata --embed-thumbnail")
subs_flag = str(" --all-subs")
cookies_flag = str(" --cookies from browser")
folder_path_flag = str(" -P")

ytdlp_bin = ""
mpv_bin="mpv"
#folder_path = ""
user_name= ""

# check for OS and change the yt-dlp binary name and folder path accordingly, also the username
system = platform.system()
if system == "Linux":
    ytdlp_bin = "yt-dlp"
    user_name = subprocess.run(['whoami'], capture_output=True, text=True).stdout.strip()
    folder_path = str(f"/home/{user_name}/Videos/")
    print ("System: Linux")
elif system == "Windows":
    ytdlp_bin = "yt-dlp.exe"
    user_name = os.environ['USERNAME']
    folder_path= str(fr"C:\Users\{user_name}\Videos")
    print ("System: Windows")

download_combo = ""

# cool logo :)
cool_logo=str(r"""
__               __            ____    
\ \       __  __/ /_      ____/ / /___ 
 \ \     / / / / __/_____/ __  / / __ \
 / /    / /_/ / /_/_____/ /_/ / / /_/ /
/_/_____\__, /\__/      \__,_/_/ .___/ 
 /_____/____/      simple CLI /_/
 
 version 0.0.5   
""")

print(cool_logo)
print(f"Hello, {user_name}! What we are going to download today? :3")

#______________________________________________________________________________

# FUNCTIONS

# process for URL download
def set_combo():
    global download_combo, cookies_flag, folder_path
    download_combo = ytdlp_bin + formato + (" ") + video_link + (" --no-part --restrict-filenames")

    if metadata_check == True:
        download_combo+=metadata_flag
            
    if subs_check == True:
        download_combo+=subs_flag
            
    if browser_cookie_check == True:
        cookies_flag+=str(" ")+browser_name
        download_combo+=cookies_flag
        
    if folder_check == True:
        download_combo+=str(" -P ")+folder_path

    try: # fix for running shlex on windows due to the backslash thing
        if system == "Linux":
            args = shlex.split(download_combo, posix=True)
        elif system == "Windows":
            args = shlex.split(download_combo, posix=False)
        a=' '.join(args)
    except:
        print ("A error ocurred in the shlex process")
    
    print(f"Running as: {a}")

    # note: the subprocess method should be better here, however it creates some problems with yt-dlp due to the
    # way it runs, so I replaced it with the following command, that, although it is said to be less secure due to
    # potential shell injection vulnerabilities, it is the only way to make yt-dlp work without spilling errors
    # or corrupting the files in the download process
    os.system(a)

# function to clear the screen, it is used in a lot of places in the code
def clrscreen():
    os.system('cls' if os.name == 'nt' else 'clear')  # clears the last operation from the shell

# command for update the yt-dlp binary from inside the program
def ytdlp_update():
	os.system('yt-dlp -U')
# selection of custom mpv frontend
def mpv_sel():
        global mpv_custom_flag, mpv_bin
        
        print("Are you using a mpv frontend? MPV is set as default.\nDo you want to set another one? (ex. Celluloid, Haruna, SMPlayer, etc...)")
        a=input("Yes (y) - Use custom | No - Use default MPV (n): ")

        try:
            if a == "y":
                mpv_bin=str(input("Type the name: "))
                mpv_bin=mpv_bin.lower()
                mpv_custom_flag = True
    
            elif a == "n":
                if system == "Linux":
                    mpv_bin = "mpv"
                elif system == "Windows":
                    mpv_bin = "mpv.exe"
                    
                mpv_custom_flag = False
            mpv_play()
        except NameError:
            print("Invalid name. Check your options again!")
        except ValueError:
            print("Invalid option, try again...")
            

# command for streaming media using mpv
def mpv_play():
    global mpv_custom_flag, mpv_bin

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Stream online media via {mpv_bin}\ntype m) to set a custom Mplayer | q) to go back to the menu")
    video_link=str(input("Insert URL: "))
    if video_link=="m":
        mpv_sel()
    elif video_link=="q":
        clrscreen()
    else:
        mpv_run=str(f"{mpv_bin} {video_link}")
        print(mpv_run)
        os.system(mpv_run)
        input("Press Enter to continue...")

# media format selection    
def format_sel():
    global format_sel, formato, format_name, subs_check, metadata_check, metadata_flag
    
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
    clrscreen()

# folder path selection - simpler approach    
def path_sel():
    global folder_check, folder_path, folder_path_flag, system
    
    path_confirm = str(input(f"do you want to use the default folder or set another?\nDefault: {folder_path}\n(d) for default, (y) for set a new one, (n) for none, save in the same path as executable\n: "))
    if path_confirm == "y":
        if system == "Linux":
            print(f"Tip: you can use ~/[...] in place of /home/{user_name}/[...]")
            
        p=str(input("Please set the new folder path: "))
        folder_path=p
        folder_check = True
        
    elif path_confirm == "d":
        if system == "Linux":
            folder_path = str(f"/home/{user_name}/Videos/")
        elif system == "Windows":
            folder_path= str(fr"C:\Users\{user_name}\Videos")
        folder_check = True
        
    elif path_confirm == "n":
        folder_path=""
        folder_check = False
    else:
        print("Not a recognized command.")
        input("Press Enter to continue...")
    clrscreen()

# set browser for login cookies and acess to download restricted contend
def browser_sel():
    global browser_name, browser_cookie_check
    browser_name = str(input("Select Browser name...\nSupported browsers are: brave, chrome, chromium, edge,\nfirefox, opera, safari, vivaldi, whale.\nYou must be logged in on the targeted website.\n:"))
    browser_cookie_check = True
    clrscreen()
    
# resets the configurations and flags
def reset_sel():
    print("1) browser cookies | 2) metadata | 3) subtitles\n4) mpv values")
    reset_choice = str(input("Select which parameter to reset: "))
    if reset_choice == "1":
        browser_cookie_check = False
    elif reset_choice == "2":
        metadata_check = False
    elif reset_choice == "3":
        subs_check = False
    elif reset_choice == "4":
        mpv_sel()
    else:
        print("Invalid command.")
    clrscreen()

# help and informations about the program
def helpinfo():
    clrscreen()
    print(cool_logo)
    print("Command-line utility written in Python to interact with yt-dlp.")
    print("Check me on Github: https://github.com/m-xisto/yt-dlp-simpleCLI")
    print("----------------------------")
    input("Press Enter to go back...")
    clrscreen()

#______________________________________________________________________________

# MAIN LOOP
while True:
    print("----------------------------")
    print(f"Format: {format_name}")
    print(f"Mp3 Metadata: {metadata_check} | Video Subtitles: {subs_check}")
    print(f"Browser Cookies: {browser_name} | Folder path: {folder_path}")
    
    print(r"""
----------------------------
    
i) to insert URL    |   f) media format
b) browser cookies  |   p) set folder path
r) reset parameters |   c) clear screen
u) update yt-dlp    |   m) stream media (mpv)
h) help             |   q) quit
____________________________
""")
    
    comando=str(input("Select a option: "))

    try:
        if comando == "i":
            clrscreen()
            video_link=str(input("Insert URL: "))
            set_combo()
            input("Press Enter to continue...")

        elif comando == "f":
            format_sel()

        elif comando == "b":
            browser_sel()

        elif comando == "p":
            path_sel()

        elif comando == "r":
            reset_sel()

        elif comando == "c":
            clrscreen()

        elif comando == "m":
            mpv_play()
            
        elif comando == "u":
            ytdlp_update()
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
			
        elif comando == "h":
            helpinfo()
        
        elif comando == "q":
            print("Bye bye! (^.^)/")
            break
        else:
            print("Not a recognized command, try again...")

    except NameError:
        print("Did you forgot to add something? Check your options again!")
    
    except ValueError:
        print("Invalid option, try again...")
