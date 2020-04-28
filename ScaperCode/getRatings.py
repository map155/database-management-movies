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

    with open("title.ratings.tsv/data.tsv", encoding="utf8") as f:
        csv_reader = csv.reader(f, delimiter='\t')
        i = 0
        for row in csv_reader:
            if i == 0:
                i += 1
                continue
            if i % 1000 == 0:
                print(i)
            i += 1
            tID = int(row[0][2:]) + 100
            Rating = row[1]
            try:
                cur.execute(f"UPDATE movies SET rating = {Rating} where movie_id = {tID};")
                con.commit()
            except:
                pass
