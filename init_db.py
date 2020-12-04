import csv
import sqlite3

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


if __name__ == "__main__":
  # read sqls
  with open('sql/create/word.sql', 'r') as f:
    SQL_CREATE_WORD = f.read()
  with open('sql/create/test.sql') as f:
    SQL_CREATE_TEST = f.read()
  with open('sql/create/version_relation.sql') as f:
    SQL_CREATE_VERSION_RELATION = f.read()
  with open('sql/create/version.sql', 'r') as f:
    SQL_CREATE_VERSION = f.read()
  with open('sql/insert/word.sql', 'r') as f:
    SQL_INSERTS_WORD = f.read()

  # execute queries
  db_path = 'db.sqlite'
  connection = sqlite3.connect(db_path, isolation_level='EXCLUSIVE')
  cur = connection.cursor()
  try:
    cur.execute(SQL_CREATE_WORD)
    cur.execute(SQL_CREATE_TEST)
    cur.execute(SQL_CREATE_VERSION)
    cur.execute(SQL_CREATE_VERSION_RELATION)
    cur.executemany(SQL_INSERTS_WORD, read_values('ngsl'))
    cur.executemany(SQL_INSERTS_WORD, read_values('nawl'))
    cur.executemany(SQL_INSERTS_WORD, read_values('tsl'))
    cur.executemany(SQL_INSERTS_WORD, read_values('bsl'))
  except Exception as e:
    print(e)
    connection.rollback()
  finally:
    connection.commit()
