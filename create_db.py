import sqlite3

SQL_CREATE_TABLE = '''
CREATE TABLE word(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type STRING,
  word STRING,
  translation STRING,
  explanation STRING,
  example STRING,
  example_translation STRING,
  pronunciation STRING,
  meaning_in_english STRING
)
'''

db_path = 'db.sqlite'
con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute(SQL_CREATE_TABLE)
con.close()