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

    with open("title.basics.tsv/data.tsv", encoding="utf8") as f:
        csv_reader = csv.reader(f, delimiter='\t')
        i = 0
        for row in csv_reader:
            if i%1000 == 0:
                print(i)
            i += 1
            try:
                if row[1] == 'movie':
                    tID = int(row[0][2:]) + 100
                    titleName = row[2]
                    startYear = int(row[5])
                    try:
                        cur.execute(f"insert into movies(movie_id, title, release_year) value ({tID}, '{titleName}', {startYear});")
                        con.commit()
                    except:
                        pass
            except:
                pass
