import csv
import pymysql
import re
import string
pattern = re.compile('[\W_]+')


con = pymysql.connect('25.9.255.51', 'DBMMoviesAdmin',
                      'DBMMov1es', 'dbmmovies')

with con:

    cur = con.cursor()
    cur.execute("SELECT VERSION()")

    with open("data.tsv", encoding="utf8") as f:
        csv_reader = csv.reader(f, delimiter='\t')
        i = 0
        for row in csv_reader:
            if i%1000 == 0:
                print(i)
            i += 1
            try:
                if 'actor' in row[4] or 'actress' in row[4]:
                    aID = int(row[0][2:]) + 100
                    firstName = pattern.sub('', row[1].rsplit(' ', 1)[0])
                    lastName = pattern.sub('', row[1].split(' ')[-1])
                    try:
                        cur.execute(f"insert into actors(actor_id, first_name, last_name) value ({aID}, '{firstName}', '{lastName}');")
                        con.commit()
                    except:
                        pass
                elif 'director' in row[4]:
                    dID = int(row[0][2:]) + 100
                    firstName = pattern.sub('', row[1].rsplit(' ', 1)[0])
                    lastName = pattern.sub('', row[1].split(' ')[-1])
                    try:
                        cur.execute(f"insert into directors(dir_id, first_name, last_name) value ({dID}, '{firstName}', '{lastName}');")
                        con.commit()
                    except:
                        pass
            except:
                pass
