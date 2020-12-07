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
  with open('sql/create/version.sql', 'r') as f:
    q['CREATE']['VERSION'] = f.read()
  with open('sql/insert/word.sql', 'r') as f:
    q['INSERT']['WORD'] = f.read()
  with open('sql/insert/version.sql', 'r') as f:
    q['INSERT']['VERSION'] = f.read()
  with open('sql/insert/test.sql', 'r') as f:
    q['INSERT']['TEST'] = f.read()
  with open('sql/select/unanswered.sql', 'r') as f:
    q['SELECT']['UNANSWERED'] = f.read()
  with open('sql/select/incorrect.sql', 'r') as f:
    q['SELECT']['INCORRECT'] = f.read()
  with open('sql/select/version_category.sql', 'r') as f:
    q['SELECT']['VERSION_CATEGORY'] = f.read()
  with open('sql/select/parent_version_id.sql', 'r') as f:
    q['SELECT']['PARENT_VERSION'] = f.read()
  with open('sql/select/versions.sql', 'r') as f:
    q['SELECT']['VERSIONS'] = f.read()
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

def select_unanswered(version_id):
  connection = get_connection()
  cur = connection.cursor()
  q = get_queries()
  category = cur.execute(q['SELECT']['VERSION_CATEGORY'], (version_id,)).fetchone()[0]
  response = cur.execute(q['SELECT']['UNANSWERED'], (version_id, category)).fetchall()
  connection.close()
  return response

def select_incorrect(version_id):
  connection = get_connection()
  cur = connection.cursor()
  q = get_queries()
  category = cur.execute(q['SELECT']['VERSION_CATEGORY'], (version_id,)).fetchone()[0]
  response = cur.execute(q['SELECT']['INCORRECT'], (version_id, category)).fetchall()
  connection.close()
  return response

def select_parent_version(version_id):
  connection = get_connection()
  cur = connection.cursor()
  q = get_queries()
  response = cur.execute(q['SELECT']['PARENT_VERSION'], (version_id,)).fetchone()
  parent_version_id = None
  if response:
    parent_version_id = response[0]
  connection.close()
  return parent_version_id

def select_versions():
  connection = get_connection()
  cur = connection.cursor()
  q = get_queries()
  response = cur.execute(q['SELECT']['VERSIONS']).fetchall()
  connection.close()
  return response

def insert_new_version(name, category):
  connection = get_connection()
  cur = connection.cursor()
  q = get_queries()
  v_id = str(uuid.uuid4())
  try:
    cur.execute(q['INSERT']['VERSION'], (v_id, None, name, category))
    connection.commit()
  except Exception as e:
    print(e)
    connection.rollback()
  finally:
    connection.close()

def insert_child_version(parent_id, name):
  connection = get_connection()
  cur = connection.cursor()
  q = get_queries()
  v_id = str(uuid.uuid4())
  try:
    category = cur.execute(q['SELECT']['VERSION_CATEGORY'], (parent_id,)).fetchone()[0]
    cur.execute(q['INSERT']['VERSION'], (v_id, parent_id, name, category))
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
  try:
    cur.execute(q['INSERT']['TEST'], (version_id, word_id, collect))
    connection.commit()
  except Exception as e:
    print(e)
    connection.rollback()
  finally:
    connection.close()


if __name__ == "__main__":
  # init_db()
  # print(select_incorrect('6027924c-419f-40ae-8b83-454dfa6cd21a_')[:10])
  print(select_unanswered('6027924c-419f-40ae-8b83-454dfa6cd21')[:10])
  # insert_new_version('v3', 'ngsl')
  # insert_child_version('bf53ec0b-b463-4969-b7cd-3e04766f7cdf', 'v1_2')
  # insert_test_result('6027924c-419f-40ae-8b83-454dfa6cd21a', 3, 0)
  # print(select_parent_version('8c12360b-7598-4579-81d1-07658e56c2cb_'))
  # print(select_versions())
