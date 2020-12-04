import csv
import sqlite3

# utils
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

def get_queries():
  q = {
    'CREATE': {},
    'INSERT': {},
    'SELECT': {},
    'DELETE': {}
  }
  with open('sql/create/word.sql', 'r') as f:
    q['CREATE']['WORD'] = f.read()
  with open('sql/create/test.sql') as f:
    q['CREATE']['TEST'] = f.read()
  with open('sql/create/version_relation.sql') as f:
    q['CREATE']['VERSION_RELATION'] = f.read()
  with open('sql/create/version.sql', 'r') as f:
    q['CREATE']['VERSION'] = f.read()
  with open('sql/insert/word.sql', 'r') as f:
    q['INSERT']['WORD'] = f.read()
  return q

def get_connection_exclusive():
  db_path = 'db.sqlite'
  return sqlite3.connect(db_path, isolation_level='EXCLUSIVE')

# execute query
def init_db():
  conn_exclusive = get_connection_exclusive()
  cur = conn_exclusive.cursor()
  q = get_queries()
  try:
    cur.execute(q['CREATE']['WORD'])
    cur.execute(q['CREATE']['TEST'])
    cur.execute(q['CREATE']['VERSION'])
    cur.execute(q['CREATE']['VERSION_RELATION'])
    cur.executemany(q['INSERT']['WORD'], read_values('ngsl'))
    cur.executemany(q['INSERT']['WORD'], read_values('nawl'))
    cur.executemany(q['INSERT']['WORD'], read_values('tsl'))
    cur.executemany(q['INSERT']['WORD'], read_values('bsl'))
    conn_exclusive.commit()
  except Exception as e:
    print(e)
    conn_exclusive.rollback()
  finally:
    conn_exclusive.close()

if __name__ == "__main__":
  init_db()
