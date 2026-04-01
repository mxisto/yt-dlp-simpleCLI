def cool_logo():
    # cool logo :)
    print(str(r"""
    __               __            ____    
   \ \       __  __/ /_      ____/ / /___ 
    \ \     / / / / __/_____/ __  / / __ \
    / /    / /_/ / /_/_____/ /_/ / / /_/ /
   /_/_____\__, /\__/      \__,_/_/ .___/ 
    /_____/____/      simple CLI /_/
    
    version 0.0.10   
    """))

def show():
    '''help and informations about the program'''
    cool_logo()
    print("Command-line utility written in Python to interact with yt-dlp.")
    print("Check me on Github: https://github.com/mxisto/yt-dlp-simpleCLI")
    print("----------------------------")
    input("Press Enter to go back...")
