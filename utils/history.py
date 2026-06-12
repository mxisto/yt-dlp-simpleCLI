'''
This script gets the information from history.db in the main folder
and fetches the selected url for download from the chosen table.
'''
import sqlite3, subprocess, platform, shutil, sys
def main():
    global cursor, conector
    x=0
    print("\nConnecting to history.db...\n")

    conector = sqlite3.connect('history.db')
    cursor = conector.cursor()

    cursor.execute("""SELECT name FROM sqlite_master  
      WHERE type='table';""")
    tables = cursor.fetchall()
    
    print("Current tables: ")
    for i in tables:
        print(' |¬',x,' -> ',i[0])
        x+=1
    sel = int(input("Select: "))
    try:
        option = str(tables[sel])
        in_table(option)
    except ValueError:
        print("oops")

def show_search(srch, entries):
    global cursor, conector
    cont=0
    print('\n')
    for i in entries:
        #sets the string to lowercase in order to search it
        n = str(i[1]).lower()
        if srch in n:
            nm = i[1]
            if len(nm) > 25:
                nm = str(nm[0:25]+"...")
            else:
                nm = str(nm+" "*(28-len(nm)))
            print(cont, "-", nm," | ",i[2])
            cont+=1
    if cont == 0:
        print("Nothing here...\n")
        action = str(input("\n(s)earch again | (q)uit\n-> ")).lower()
        if action == "s":
            srch = str(input("\nSearch for: "))
            show_search(srch, entries)
        else:
            cursor.close()
            conector.close()
    else:
        action = str(input("\n(g)et by index | (s)earch again | (q)uit\n-> ")).lower()
        if action == "g":
            return_url(entries)
        elif action == "s":
            srch = str(input("\nSearch for: "))
            show_search(srch, entries)
        else:
            cursor.close()
            conector.close()

def return_url(entries):
    '''this sends the selected video url to the clipboard'''
    try:
        indx = int(input("  : "))
        url = entries[indx]
        url = str(url[2])
        system = platform.system()
        if system == "Windows":
            cpycmd = ["clip"]
        elif system == "Darwin":
            cpycmd = ["pbcopy"]
        else:  # Linux/other
            if shutil.which("xclip"):
                cpycmd = ["xclip", "-selection", "clipboard"]
            elif shutil.which("xsel"):
                cpycmd = ["xsel", "--clipboard", "--input"]
            else:
                sys.exit("No clipboard utility found (install xclip or xsel)")

        # send text to clipboard (text mode)
        subprocess.run(cpycmd, input=url, text=True, check=True)
        print(url,"\nThe URL was sent to your clipboard...")
    except IndexError:
        print("Index out of range...pay attention!")

def in_table(option):
    global cursor, conector
    cont = 0
    try:
        gnm = (f"SELECT * FROM {option[2:-3]}") #cleans the string
        cursor.execute(gnm)
        entries = cursor.fetchall()
        print("\n")
        for i in entries:
            #cuts the title to a smaller string if needed
            nm = i[1]
            if len(nm) > 25:
                nm = str(nm[0:25]+"...")
            else:
                nm = str(nm+" "*(28-len(nm)))
            print(cont, "-", nm," | ",i[2])
            cont+=1
        if cont == 0:
            print("\nNothing here...")
            cursor.close()
            conector.close()
            pass
        else:
            cmd = str(input("\n(g)et by index | (s)earch by name | (q)uit\n--> ")).lower()
            #searches in the entries for the given text
            if cmd == "s":
                srch = str(input("\nSearch for: "))
                show_search(srch, entries)
            elif cmd == "g":
                return_url(entries)
            else:
                cursor.close()
                conector.close()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
