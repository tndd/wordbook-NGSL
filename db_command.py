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
  q = {}
  with open('sql/create/word.sql', 'r') as f:
    q['CREATE_WORD'] = f.read()
  with open('sql/create/test.sql') as f:
    q['CREATE_TEST'] = f.read()
  with open('sql/create/version_relation.sql') as f:
    q['VERSION_RELATION'] = f.read()
  with open('sql/create/version.sql', 'r') as f:
    q['CREATE_VERSION'] = f.read()
  with open('sql/insert/word.sql', 'r') as f:
    q['INSERTS_WORD'] = f.read()
  return q

def init_db(connection, q):
  cur = connection.cursor()
  try:
    cur.execute(q['CREATE_WORD'])
    cur.execute(q['CREATE_TEST'])
    cur.execute(q['CREATE_VERSION'])
    cur.execute(q['CREATE_VERSION_RELATION'])
    cur.executemany(q['INSERTS_WORD'], read_values('ngsl'))
    cur.executemany(q['INSERTS_WORD'], read_values('nawl'))
    cur.executemany(q['INSERTS_WORD'], read_values('tsl'))
    cur.executemany(q['INSERTS_WORD'], read_values('bsl'))
  except Exception as e:
    print(e)
    connection.rollback()
  finally:
    connection.commit()

if __name__ == "__main__":
  q = get_queries()
  db_path = 'db.sqlite'
  connection = sqlite3.connect(db_path, isolation_level='EXCLUSIVE')
  init_db(connection, q)
