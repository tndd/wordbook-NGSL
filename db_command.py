import csv
import sqlite3
import uuid
import os

# consts
DB_PATH = 'db.sqlite'

# util methods
def read_values(category):
  values = []
  with open(f'./resource/{category}.csv', 'r') as f:
    render = csv.reader(f)
    for row in list(render)[1:]:
      if category == 'bsl':
        values.append((category, row[0], row[1], row[3], row[4], row[5], row[2], ''))
      else:
        values.append((category, row[0], row[1], row[4], row[5], row[6], row[2], row[3]))
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
  with open('sql/insert/version.sql', 'r') as f:
    q['INSERT']['VERSION'] = f.read()
  with open('sql/insert/version_relation.sql', 'r') as f:
    q['INSERT']['VERSION_RELATION'] = f.read()
  with open('sql/insert/test.sql', 'r') as f:
    q['INSERT']['TEST'] = f.read()
  with open('sql/select/unanswered.sql', 'r') as f:
    q['SELECT']['UNANSWERED'] = f.read()
  with open('sql/select/incorrect.sql', 'r') as f:
    q['SELECT']['INCORRECT'] = f.read()
  return q

def get_connection():
  return sqlite3.connect(DB_PATH)

# execute query methods
def init_db():
  if os.path.exists(DB_PATH):
    print('Reset DB')
    os.remove(DB_PATH)
  connection = get_connection()
  cur = connection.cursor()
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
    connection.commit()
  except Exception as e:
    print(e)
    connection.rollback()
  finally:
    connection.close()

def select_unanswered(version_id, category):
  connection = get_connection()
  cur = connection.cursor()
  q = get_queries()
  response = cur.execute(q['SELECT']['UNANSWERED'], (version_id, category)).fetchall()
  connection.close()
  return response

def select_incorrect(version_id, category):
  connection = get_connection()
  cur = connection.cursor()
  q = get_queries()
  response = cur.execute(q['SELECT']['INCORRECT'], (version_id, category)).fetchall()
  connection.close()
  return response

def insert_new_version(name):
  connection = get_connection()
  cur = connection.cursor()
  q = get_queries()
  v_id = str(uuid.uuid4())
  cur.execute(q['INSERT']['VERSION'], (v_id, name))
  connection.commit()
  cur.close()

def insert_child_version(parent_id, name):
  connection = get_connection()
  cur = connection.cursor()
  q = get_queries()
  v_id = str(uuid.uuid4())
  try:
    cur.execute(q['INSERT']['VERSION'], (v_id, name))
    cur.execute(q['INSERT']['VERSION_RELATION'], (v_id, parent_id))
    connection.commit()
  except Exception as e:
    print(e)
    connection.rollback()
  finally:
    connection.close()

def insert_test_result(version_id, word_id, collect):
  connection = get_connection()
  cur = connection.cursor()
  q = get_queries()
  cur.execute(q['INSERT']['TEST'], (version_id, word_id, collect))
  connection.commit()
  connection.close()


if __name__ == "__main__":
  init_db()
  # resp = select_incorrect('6027924c-419f-40ae-8b83-454dfa6cd21a', 'ngsl')
  # print(resp)
  # insert_new_version('v1')
  # insert_child_version('1ea22bbb-76e7-44a2-90e0-67ed4ae195b1', 'v1_1')
  # insert_test_result('6027924c-419f-40ae-8b83-454dfa6cd21a', 3, 0)
