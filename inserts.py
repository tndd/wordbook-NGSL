import csv
import sqlite3

SQL_INSERTS = 'INSERT INTO word ("type", "word", "translation", "explanation", "example", "example_translation", "pronunciation", "meaning_in_english") VALUES(?, ?, ?, ?, ?, ?, ?, ?);'

def read_values(d_type):
  values = []
  with open(f'./resource/{d_type}.csv', 'r') as f:
    render = csv.reader(f)
    for row in list(render)[1:]:
      values.append((d_type, row[0], row[1], row[4], row[5], row[6], row[2], row[3]))
  return values

def read_bsl_values():
  values = []
  with open(f'./resource/bsl.csv', 'r') as f:
    render = csv.reader(f)
    for row in list(render)[1:]:
      values.append(('bsl', row[0], row[1], row[3], row[4], row[5], row[2], ''))
  return values

db_path = 'db.sqlite'
con = sqlite3.connect(db_path)
cur = con.cursor()
cur.executemany(SQL_INSERTS, read_values('ngsl'))
cur.executemany(SQL_INSERTS, read_values('nawl'))
cur.executemany(SQL_INSERTS, read_values('tsl'))
cur.executemany(SQL_INSERTS, read_bsl_values())
con.commit()
con.close()
