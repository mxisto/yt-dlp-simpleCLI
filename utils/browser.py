def name():
    '''set browser for login cookies and acess to download restricted content'''
    n = str(input("Select Browser name...\nSupported browsers are: brave, chrome, chromium, edge,\nfirefox, opera, safari, vivaldi, whale.\nYou must be logged in on the targeted website.\n>> "))
    return n

def flag(name):
    flag = str(f" --cookies-from-browser {name}")
    return flag
