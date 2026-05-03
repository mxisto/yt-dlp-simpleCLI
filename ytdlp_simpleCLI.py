#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#______________________________________________________________________________
# standard libraries import
import platform, shlex, subprocess, os, time

# custom libraries import
import utils.helpinfo, utils.browser, utils.database

# VARIABLES, FLAGS and CHECKS
# ______________
os.environ['TERM'] = 'xterm'

browser_cookie_check = False
metadata_check = False
subs_check = False
folder_check = True
custom_filename_check = False

video_link = str("")
browser_name = str("")
format_name = str("none")

metadata_flag = str(" --embed-metadata --embed-thumbnail")
subs_flag = str(" --all-subs")
folder_path_flag = str(" -P")
custom_filename_flag = str(" -o ")

ytdlp_bin = ""
user_name= ""

custom_filename = ""

videos={}

# check for OS and change the yt-dlp binary name and folder path accordingly, also the username
system = platform.system()
if system == "Linux":
    if os.path.isfile("yt-dlp"):
        print("yt-dlp binary in same directory as program")
        ytdlp_bin = "./yt-dlp" #for using the executable from the same folder instead of the system path one
    else:
        ytdlp_bin = "yt-dlp"
    user_name = subprocess.run(['whoami'], capture_output=True, text=True).stdout.strip()
    folder_path = str(f"/home/{user_name}/Videos/")
    print ("System: Linux")

elif system == "Windows":
    if os.path.isfile("yt-dlp.exe"):
        print("yt-dlp binary in same directory as program")
    ytdlp_bin = "yt-dlp.exe"
    user_name = os.environ['USERNAME']
    folder_path= str(f"C:\\Users\\{user_name}\\Videos\\")
    print ("System: Windows")

download_combo = ""

#______________________________________________________________________________

# FUNCTIONS

def set_combo():
    '''process for URL download, it combines the strings into a command to execute in the shell'''
    global download_combo, cookies_flag, folder_path, custom_filename
    
    download_combo = ytdlp_bin + formato + (" ") + video_link #+ (" --restrict-filenames")

    if metadata_check == True:
        download_combo+=metadata_flag
            
    if subs_check == True:
        download_combo+=subs_flag
            
    if browser_cookie_check == True:
        download_combo+=cookies_flag
        
    if custom_filename_check == True:
        if system == "Linux":
            download_combo+=custom_filename_flag+str(f' \\"{custom_filename}.%(ext)s\\" ')
        elif system == "Windows":
            download_combo+=custom_filename_flag+str(f' \"{custom_filename}.%(ext)s\" ')
            # fix for the backslash escaping in Windows
        
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
    # way it runs, so I replaced it with the following command using shlex, that, although it is said to be 
    # less secure due to potential shell injection vulnerabilities, it is the only way to make 
    # yt-dlp work without spilling errors
    # or corrupting the files in the download process
    os.system(a)

def clrscreen():
    '''function to clear the screen, it is used in a lot of places in the code'''
    os.system('cls' if os.name == 'nt' else 'clear')  # clears the last operation from the shell

def ytdlp_update():
    '''command to update the yt-dlp binary from inside the program'''
    os.system(f'{ytdlp_bin} -U')

def format_sel():
    '''media format selection'''
    global format_sel, formato, format_name, subs_check, metadata_check, metadata_flag
    
    print("Please select the media format:")
    print("1) mp4 | 2) mp3")
    formato_sel = str(input(": "))
    if formato_sel == "1":
        print("Format set to Mp4")
        formato = str(" -t mp4") # preset alias from yt-dlp
        format_name = str("Mp4")
        sub_check = str(input("save subtitles? (y) or (n)?: "))
        if sub_check == "y":
            subs_check = True
            metadata_check = False
        elif sub_check == "n":
            subs_check = False
        else:
            print("Invalid command, setting subtitles check to False")
            subs_check = False
    elif formato_sel == "2":
        print("Format set to Mp3")
        formato = str(" -t mp3")  # preset alias from yt-dlp
        meta_check = str(input("save metadata? (y) or (n)?: "))
        if meta_check == "y":
            metadata_check = True
            subs_check = False
        elif meta_check == "n":
            metadata_check = False
        else:
            print("Invalid command, setting metadata check to False")
            metadata_check = False
        format_name = str("Mp3")
    else:
        print("Invalid command, try again...")
    clrscreen()

def path_sel():
    '''folder path selection - simpler approach'''
    global folder_check, folder_path, folder_path_flag, system
    
    path_confirm = str(input(f"do you want to use the default folder or set another?\nDefault: {folder_path}\n(d) for default, (y) for set a new one, (n) for none, save in the same path as executable\n: "))
    if path_confirm == "y":
        if system == "Linux":
            print(f"Tip: you can use ~/[...] in place of /home/{user_name}/[...]")
            
        p=str(input("Please set the new folder path: "))
        if "~/" in p:
            p=p.replace("~/",f"/home/{user_name}/")
        if not p.endswith("/"):
            p+="/"
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
    
def reset_all():
    '''resets all the configurations and flags'''
    global browser_cookie_check, metadata_check, subs_check, folder_check, video_link, browser_name, format_name, custom_filename, custom_filename_check
    choice = str(input("Do you really want to reset ALL set parameter for this session?\n (Y)es or (N)o?: "))
    choice = choice.lower()
    if choice == "y":
        browser_cookie_check = False
        metadata_check = False
        subs_check = False
        folder_check = True
        custom_filename_check = False

        video_link = str("")
        browser_name = str("")
        format_name = str("none")
        custom_filename = str("")
    elif choice == "n":
        clrscreen()
    else:
        print("Invalid command.")

#______________________________________________________________________________

# MAIN LOOP
utils.helpinfo.cool_logo()
print(f"Hello, {user_name}! What we are going to download today? :3")

while True:
    print("----------------------------")
    print(f"Format: {format_name}")
    print(f"Mp3 Metadata: {metadata_check}") if metadata_check else None
    print(f"Video Subtitles: {subs_check}") if subs_check else None
    print(f"Browser Cookies: {browser_name}") if browser_name else None
    print(f"Folder path: {folder_path}")
    
    print(r"""
----------------------------
    
i) to insert URL    |   f) media format
b) browser cookies  |   p) set folder path
r) reset            |   c) clear screen
u) update yt-dlp    |   
h) help             |   q) quit
____________________________
""")
    comando=str(input("Select a option: "))

    try:
        if comando == "i":
            if format_name == 'none':
                print('\nPlease select a file format first...')
            else:
            
                clrscreen()
                print("Insert the video URL...\n| c + space before link to enter a custom filename\n| d + space to add the link to the local database\n| Enter nothing to cancel")
                video_link=str(input(">> "))
                if video_link == (''):
                    clrscreen()
                else:
                    if video_link[0] == str('c') or video_link[0] == str('C'):
                        video_link = video_link[1:].strip(" ")
                        custom_filename = str(input("Type the name for the file >> "))
                        custom_filename_check = True
                    
                    if video_link[0] == str('d') or video_link[0] == str('D'):
                        video_link = video_link[1:].strip(" ")
                        utils.database.add(video_link, ytdlp_bin)
                    
                    print(video_link)
                    set_combo()
                    # resets the custom filename for the next iteration
                    custom_filename = str("")
                    custom_filename_check = False
                    input("Press Enter to continue...")

        elif comando == "f":
            format_sel()

        elif comando == "b":
            browser_name = str(utils.browser.name())
            cookies_flag = str(utils.browser.flag(browser_name))
            browser_cookie_check = True
            clrscreen()

        elif comando == "p":
            path_sel()

        elif comando == "r":
            reset_all()

        elif comando == "c":
            clrscreen()
            
        elif comando == "u":
            ytdlp_update()
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
            
        elif comando == "h":
            clrscreen()
            utils.helpinfo.show()
            clrscreen()
        
        elif comando == "q":
            print("Bye bye! (^.^)/")
            time.sleep(1)
            break
        else:
            print("\nNot a recognized command, try again...")

    except NameError as nme:
        print("\nError -->", nme)
    
    except ValueError:
        print("Invalid option, try again...")
