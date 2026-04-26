'''adds the current link to the database, getting the title too'''
import sqlite3, time, subprocess, os

print(os.getcwd())

conector = sqlite3.connect('history.db')
cursor = conector.cursor()

try:
    sql = """
        create table youtube
        (date text, title text, url text,
        primary key (date))
        """ 
    cursor.execute(sql)
    conector.commit()
    
    sql = """
        create table twitter
        (date text, title text, url text,
        primary key (date))
        """
    cursor.execute(sql)
    conector.commit()
    
    sql = """
        create table other
        (date text, title text, url text,
        primary key (date))
        """
    cursor.execute(sql)
    conector.commit()
    
    print("\nTrying to create a new table...\n")
        
except sqlite3.OperationalError:
    print("Database file already created...\n")
    
cursor.close()
conector.close()

def add(link, ytdlp_bin):
    print("Getting URL info, please wait...")
    data = []
    
    print(os.getcwd())

    conector = sqlite3.connect('history.db')
    cursor = conector.cursor()
    
    # date
    day = time.asctime()
    day = day[:-8]
    data.append(str(day))
    
    # title
    get_title=str(f"{ytdlp_bin} --get-title {link}")
    get_title=subprocess.run(get_title,shell=True, capture_output=True, text=True)
    title=get_title.stdout.strip()
    data.append(str(title))
    
    data.append(str(link))
    
    # url treatment based on the contents from the url
    
    if 'youtube.com' in link or 'youtu.be' in link:
        sql = """
            insert into youtube
            (date, title, url)
            values (?, ?, ?)
            """
        cursor.execute(sql, data)
        conector.commit()
    
    elif 'x.com' in link:
        sql = """
            insert into twitter
            (date, title, url)
            values (?, ?, ?)
            """
        cursor.execute(sql, data)
        conector.commit()
        
    else:
        
        sql = """
            insert into other
            (date, title, url)
            values (?, ?, ?)
            """
        cursor.execute(sql, data)
        conector.commit()

    cursor.close()
    conector.close()
