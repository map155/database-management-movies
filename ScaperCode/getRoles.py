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

    with open("title.principals.tsv/data.tsv", encoding="utf8") as f:
        csv_reader = csv.reader(f, delimiter='\t')
        i = 0
        for row in csv_reader:
            if i == 0:
                i += 1
                continue
            if i%1000 == 0:
                print(i)
            i += 1
            tID = int(row[0][2:]) + 100
            nID = int(row[2][2:]) + 100
            try:
                cur.execute(f"insert into movie_role(movie_id, person_id, role_code) value ({tID}, '{nID}', {1});")
                con.commit()
            except:
                pass
