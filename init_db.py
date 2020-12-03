import csv
import sqlite3

with open('sql/create/word.sql', 'r') as f:
  SQL_CREATE_TABLE = f.read()
with open('sql/insert/word.sql', 'r') as f:
  SQL_INSERTS = f.read()

def read_values(d_type):
  values = []
  with open(f'./resource/{d_type}.csv', 'r') as f:
    render = csv.reader(f)
    for row in list(render)[1:]:
      if d_type == 'bsl':
        values.append((d_type, row[0], row[1], row[3], row[4], row[5], row[2], ''))
      else:
        values.append((d_type, row[0], row[1], row[4], row[5], row[6], row[2], row[3]))
  return values

db_path = 'db.sqlite'
con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute(SQL_CREATE_TABLE)
cur.executemany(SQL_INSERTS, read_values('ngsl'))
cur.executemany(SQL_INSERTS, read_values('nawl'))
cur.executemany(SQL_INSERTS, read_values('tsl'))
cur.executemany(SQL_INSERTS, read_values('bsl'))
con.commit()
con.close()