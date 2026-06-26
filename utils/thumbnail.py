#yt-dlp --write-thumbnail --skip-download "VIDEO_URL"

import shlex, subprocess, platform, os
def main(url,ytdlp_bin):
    print(os.getcwd())
    system = platform.system()
    if system == "Linux":
        user_name = subprocess.run(['whoami'], capture_output=True, text=True).stdout.strip()
        img_path = str(f"/home/{user_name}/Images/")
        print ("System: Linux")
    elif system == "Windows":
        user_name = os.environ['USERNAME']
        img_path= str(f"C:\\Users\\{user_name}\\Pictures\\")
        print ("System: Windows")
    
    print("By default the file goes to your images directory!")
    combo = str(f"{ytdlp_bin} --write-thumbnail --skip-download --convert-thumbnails png {url} -P {img_path}")
    try: # fix for running shlex on windows due to the backslash thing
        if system == "Linux":
            args = shlex.split(combo, posix=True)
        elif system == "Windows":
            args = shlex.split(combo, posix=False)
        a=' '.join(args)
        print(f"Running as: {a}")
        # note: the subprocess method should be better here, however it creates some problems with yt-dlp due to the
        # way it runs, so I replaced it with the following command using shlex, that, although it is said to be 
        # less secure due to potential shell injection vulnerabilities, it is the only way to make 
        # yt-dlp work without spilling errors
        # or corrupting the files in the download process
        os.system(a)
    except:
        print ("A error ocurred in the shlex process")
    input("Press Enter to continue...")
    
