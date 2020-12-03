import sqlite3

def get_words_unanswered(cur, cls, version, type):
  with open('sql/select/unanswered.sql', 'r') as f:
    query = f.read()
  r = cur.execute(query, (cls, version, type))
  return list(r)

db_path = 'db.sqlite'
con = sqlite3.connect(db_path)
cur = con.cursor()
print(get_words_unanswered(cur,1,1,'ngsl'))