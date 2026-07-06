'''
This script gets the information from history.db in the main folder
and fetches the selected url for download from the chosen table.
'''
import sqlite3, subprocess, platform, shutil, sys, re

# below is a fix for the lenght of japanese and chinese characthers (uses `re`)
cjk_pattern = re.compile(r'[\u3040-\u30FF\u3400-\u4DBF\u4E00-\u9FFF]')

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
    except IndexError:
        print("Error - Value out of index...")

def show_search(srch, entries):
    '''shows the search result'''
    global cursor, conector
    cont=0
    found_entries=[]
    print('\n')
    for i in entries:
        #sets the string to lowercase in order to search it
        # in this case, cjk characthers can be search normally
        n = str(i[1]).lower()
        if srch in n:
            nm = i[1]
            lnk = str(i[2]) #removes 'https://'
            if 'https' in lnk:
                lnk = lnk[8:-1]
            
            if len(nm) > 30:
                nm = str(nm[0:28]+"...")
            else:
                nm = str(nm+" "*(30-len(nm)))
            print(cont, "-", nm,"\n |-",lnk,"\n","-"*60)
            cont+=1
            found_entries.append(i)
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
            if len(found_entries) > 0:
                return_url(found_entries)
            else:
                return_url(entries)
        elif action == "s":
            srch = str(input("\nSearch for: "))
            show_search(srch, entries)
        else:
            cursor.close()
            conector.close()

def return_url(entries):
    '''sends the selected video url to the clipboard'''
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
    '''shows the entries from the selected table'''
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
            lnk = str(i[2]) #removes 'https://'
            if 'https' in lnk:
                lnk = lnk[8:-1]
                
            cjk_chars = cjk_pattern.findall(nm) #checks if there is any cjk characther in each entry
            if cjk_chars:
                nm = str(nm[0:36]+"...")
            elif len(nm) > 30:
                nm = str(nm[0:60]+"...")
            else:
                nm = str(nm+" "*(33-len(nm)))
            print(cont, "-", nm,"\n |-",lnk,"\n","-"*60)
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
    
